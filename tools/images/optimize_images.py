"""
Right-size heavy <img> files for the web.

Scans every page for <img> tags pointing at large rasters under assets/images/,
writes 480px and 960px WebP copies to assets/images/thumbs/, and rewrites the tag
to use them via srcset. The original stays where it is (and stays the lightbox
source through data-full), so nothing is lost. Safe to re-run: tags already on
thumbs/ are skipped, and existing thumbs are not regenerated.

    python tools/images/optimize_images.py
"""
import glob
import os
import re

from PIL import Image, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
THUMBS = "assets/images/thumbs"
WIDTHS = (480, 960)
MIN_BYTES = 100 * 1024      # smaller files are left alone
QUALITY = 76

# how wide the image is on screen, per context — lets the browser pick 480 vs 960
SIZES_MASONRY = "(max-width: 480px) 92vw, (max-width: 768px) 46vw, (max-width: 1440px) 30vw, 430px"
SIZES_DEFAULT = "(max-width: 600px) 92vw, 50vw"

IMG_TAG = re.compile(r"<img\b[^>]*>", re.S)


def attr(tag, name):
    m = re.search(r'\s%s="([^"]*)"' % re.escape(name), tag)
    return m.group(1) if m else None


def set_attr(tag, name, value):
    if attr(tag, name) is not None:
        return re.sub(r'(\s%s=")[^"]*(")' % re.escape(name), lambda m: m.group(1) + value + m.group(2), tag, count=1)
    return re.sub(r"\s*/?>$", lambda m: ' %s="%s"%s' % (name, value, m.group(0)), tag, count=1)


def make_thumbs(src):
    """Return {width: web path} for src, creating any missing WebP copies."""
    path = os.path.join(ROOT, src)
    stem = os.path.splitext(os.path.relpath(src, "assets/images"))[0].replace("\\", "/")
    out = {}
    img = None
    for w in WIDTHS:
        web = "%s/%s-%d.webp" % (THUMBS, stem, w)
        dest = os.path.join(ROOT, web)
        if not os.path.exists(dest):
            if img is None:
                img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            copy = img.copy()
            if copy.width > w:
                copy = copy.resize((w, round(copy.height * w / copy.width)), Image.LANCZOS)
            copy.save(dest, "WEBP", quality=QUALITY, method=6)
        out[w] = web
    return out


def needs_work(src):
    if not src or not src.startswith("assets/images/") or src.startswith(THUMBS):
        return False
    if not src.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        return False
    path = os.path.join(ROOT, src)
    return os.path.exists(path) and os.path.getsize(path) >= MIN_BYTES


def main():
    saved = 0
    for page in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        html = open(page, encoding="utf-8").read()
        changed = 0

        def rewrite(m):
            nonlocal changed, saved
            tag = m.group(0)
            start = html.rfind("<div", 0, m.start())
            context = html[start:m.start()]

            # lazily-swapped slideshow frames: point data-src at the 960 copy
            lazy = attr(tag, "data-src")
            if needs_work(lazy):
                thumbs = make_thumbs(lazy)
                saved += os.path.getsize(os.path.join(ROOT, lazy)) - os.path.getsize(os.path.join(ROOT, thumbs[960]))
                changed += 1
                return set_attr(tag, "data-src", thumbs[960])

            src = attr(tag, "src")
            if not needs_work(src):
                return tag
            thumbs = make_thumbs(src)
            saved += os.path.getsize(os.path.join(ROOT, src)) - os.path.getsize(os.path.join(ROOT, thumbs[960]))
            in_masonry = "masonry-item" in context
            if in_masonry and attr(tag, "data-full") is None:
                tag = set_attr(tag, "data-full", src)      # lightbox keeps the full-size original
            tag = set_attr(tag, "src", thumbs[960])
            tag = set_attr(tag, "srcset", "%s 480w, %s 960w" % (thumbs[480], thumbs[960]))
            tag = set_attr(tag, "sizes", SIZES_MASONRY if in_masonry else SIZES_DEFAULT)
            changed += 1
            return tag

        html = IMG_TAG.sub(rewrite, html)
        if changed:
            open(page, "w", encoding="utf-8").write(html)
            print("%-14s %d images" % (os.path.basename(page), changed))
    print("saved ~%.1f MB against the originals (960px copies)" % (saved / 1024 / 1024))


if __name__ == "__main__":
    main()
