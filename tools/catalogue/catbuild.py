# -*- coding: utf-8 -*-
"""FM Trading F.Z.E — catalogue layout engine (A4, brand-matched)."""
import os, io, math
from PIL import Image, ImageFilter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = r"C:/Users/Omar/Desktop/FMZ Trading"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgcache")
os.makedirs(CACHE, exist_ok=True)

# ---------- fonts ----------
F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Disp", F + "georgiab.ttf"))
pdfmetrics.registerFont(TTFont("DispR", F + "georgia.ttf"))
pdfmetrics.registerFont(TTFont("DispI", F + "georgiai.ttf"))
pdfmetrics.registerFont(TTFont("UI", F + "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("UIB", F + "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("UISB", F + "seguisb.ttf"))

# ---------- palette ----------
INK        = "#0C1012"
INK_SOFT   = "#161C1E"
CREAM      = "#F4F0E6"
CREAM_2    = "#EDE7D9"
PAPER_W    = "#FBF9F3"
GOLD       = "#C5964F"
GOLD_BR    = "#E0B873"
GOLD_DK    = "#7A5A2E"
WHITE_P    = "#F7F2E9"
BODY       = "#3E3A33"
MUTED      = "#726B5F"
LINE       = "#D6CDB8"

W, H = 595.276, 841.890
M = 46.0                      # page margin
CW = W - 2 * M                # content width

_footer_note = "FM TRADING F.M.Z  |  INTERIOR DESIGN & DECORATION"


# ============================================================ images
def _src(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def prep(path, w_pt, h_pt, dpi=170, blur=0):
    """Cover-crop `path` to the w:h ratio and cache as JPEG at ~dpi."""
    key = "%s_%dx%d_%d_%d.jpg" % (
        os.path.splitext(os.path.basename(path))[0],
        round(w_pt), round(h_pt), dpi, blur)
    out = os.path.join(CACHE, key)
    if os.path.exists(out):
        return out
    im = Image.open(_src(path)).convert("RGB")
    ratio = w_pt / float(h_pt)
    sw, sh = im.size
    if sw / float(sh) > ratio:           # source too wide — trim the sides
        cw_, ch_ = sh * ratio, float(sh)
    else:                               # source too tall — trim top/bottom
        cw_, ch_ = float(sw), sw / ratio
    left = (sw - cw_) / 2
    top = max(0.0, min((sh - ch_) / 2.35, sh - ch_))   # bias to the upper third
    im = im.crop((round(left), round(top), round(left + cw_), round(top + ch_)))
    max_px = w_pt / 72.0 * dpi
    if im.width > max_px:
        s = max_px / im.width
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                       Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    return out


def logo_png():
    out = os.path.join(CACHE, "logo_mark.png")
    if not os.path.exists(out):
        im = Image.open(os.path.join(ROOT, "assets/logo/logo.png")).convert("RGBA")
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
        s = 420 / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im.save(out, "PNG", optimize=True)
    return out


# ============================================================ primitives
class Cat:
    def __init__(self, path, footer_note=_footer_note):
        self.c = rl_canvas.Canvas(path, pagesize=(W, H))
        self.c.setTitle("")
        self.page = 0
        self.footer_note = footer_note

    # -- text ------------------------------------------------------
    def tw(self, s, font, size, track=0):
        return self.c.stringWidth(s, font, size) + track * max(0, len(s) - 1)

    def text(self, x, y, s, font="UI", size=9, color=BODY, track=0, align="l"):
        c = self.c
        if align == "c":
            x -= self.tw(s, font, size, track) / 2
        elif align == "r":
            x -= self.tw(s, font, size, track)
        t = c.beginText(x, y)
        t.setFont(font, size)
        t.setFillColor(color)
        t.setCharSpace(track)   # always emit: Tc persists across text objects
        t.textOut(s)
        c.drawText(t)
        return x

    def wrap(self, s, font, size, width, track=0):
        words, lines, cur = s.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if self.tw(t, font, size, track) <= width or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, width, s, font="UI", size=9.4, lead=15,
             color=BODY, track=0, align="l", maxlines=None):
        lines = self.wrap(s, font, size, width, track)
        if maxlines:
            lines = lines[:maxlines]
        for i, ln in enumerate(lines):
            ax = x if align == "l" else (x + width / 2 if align == "c" else x + width)
            self.text(ax, y - i * lead, ln, font, size, color, track, align[0])
        return y - (len(lines) - 1) * lead

    def label(self, x, y, s, color=GOLD, size=7.6, font="UIB"):
        self.text(x, y, s.upper(), font, size, color, track=2.0)

    def rule(self, x, y, w, color=GOLD, h=1.6):
        self.c.setFillColor(color)
        self.c.rect(x, y, w, h, stroke=0, fill=1)

    # -- boxes -----------------------------------------------------
    def rrect(self, x, y, w, h, r=10, fill=None, stroke=None, lw=0.8):
        c = self.c
        if fill:
            c.setFillColor(fill)
        if stroke:
            c.setStrokeColor(stroke)
            c.setLineWidth(lw)
        c.roundRect(x, y, w, h, r, stroke=1 if stroke else 0, fill=1 if fill else 0)

    def img(self, path, x, y, w, h, r=10, dpi=170, shade=None, blur=0):
        c = self.c
        c.saveState()
        p = c.beginPath()
        p.roundRect(x, y, w, h, r)
        c.clipPath(p, stroke=0, fill=0)
        c.drawImage(ImageReader(prep(path, w, h, dpi, blur)), x, y, w, h,
                    preserveAspectRatio=False, anchor="c", mask=None)
        if shade:
            for (col, alpha, y0, y1) in shade:
                self._vgrad(x, y + h * y0, w, h * (y1 - y0), col, alpha)
        c.restoreState()

    def _vgrad(self, x, y, w, h, color, a_top_bottom, steps=42):
        """Vertical fade: a_top_bottom = (alpha_at_bottom, alpha_at_top)."""
        c = self.c
        a0, a1 = a_top_bottom
        for i in range(steps):
            t = i / (steps - 1.0)
            c.setFillColor(color, alpha=a0 + (a1 - a0) * t)
            c.rect(x, y + h * t, w, h / steps + 0.7, stroke=0, fill=1)
        c.setFillAlpha(1)

    def shade_img(self, path, x, y, w, h, r=10, dpi=170,
                  bands=((INK, (0.92, 0.0), 0.0, 0.62),)):
        self.c.saveState()
        p = self.c.beginPath()
        p.roundRect(x, y, w, h, r)
        self.c.clipPath(p, stroke=0, fill=0)
        self.c.drawImage(ImageReader(prep(path, w, h, dpi)), x, y, w, h,
                         preserveAspectRatio=False, mask=None)
        for col, alphas, y0, y1 in bands:
            self._vgrad(x, y + h * y0, w, h * (y1 - y0), col, alphas)
        self.c.restoreState()

    # -- page chrome -----------------------------------------------
    def bg(self, color=CREAM):
        self.c.setFillColor(color)
        self.c.rect(0, 0, W, H, stroke=0, fill=1)

    def new(self, color=CREAM):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.bg(color)

    def foot(self, dark=False):
        y = 42
        self.c.setStrokeColor(GOLD_DK if dark else LINE)
        self.c.setLineWidth(0.7)
        self.c.line(M, y + 14, W - M, y + 14)
        self.text(M, y, self.footer_note, "UISB", 6.6,
                  GOLD if dark else MUTED, track=1.2)
        self.text(W - M, y, "%02d" % self.page, "UISB", 6.6,
                  GOLD if dark else MUTED, track=1.2, align="r")

    def head(self, label, title, sub=None, y=H - 92, dark=False,
             tsize=25, width=CW):
        self.label(M, y, label, GOLD)
        lines = self.wrap(title, "Disp", tsize, width)
        ty = y - 26
        for i, ln in enumerate(lines):
            self.text(M, ty - i * (tsize + 4), ln, "Disp", tsize,
                      WHITE_P if dark else "#171C1E")
        ty -= (len(lines) - 1) * (tsize + 4)
        if sub:
            ty = self.para(M, ty - 17, width - 40, sub, "UI", 9.2, 13.6,
                           GOLD_BR if dark else MUTED)
        return ty

    def save(self):
        self.c.showPage()
        self.c.save()


# ============================================================ page recipes
def cover(cat, hero, kicker, title, subtitle, tagline, footer):
    cat.new(INK)
    c = cat.c
    cat.shade_img(hero, 0, 0, W, H, r=0, dpi=150, bands=(
        (INK, (0.66, 0.20), 0.0, 0.55),
        (INK, (0.30, 0.90), 0.45, 1.0),
    ))
    # warm top rule
    c.setFillColor(GOLD)
    c.rect(0, H - 9, W, 9, stroke=0, fill=1)
    c.setFillColor(GOLD_DK)
    c.rect(0, H - 12, W, 3, stroke=0, fill=1)

    lg = ImageReader(logo_png())
    lw = 96
    c.drawImage(lg, M, H - 78 - lw, lw, lw, mask="auto",
                preserveAspectRatio=True, anchor="nw")

    y = H - 78 - lw - 52
    cat.label(M, y, kicker, GOLD, size=8.4)
    y -= 46
    cat.text(M, y, title, "Disp", 43, WHITE_P, track=0.5)
    y -= 40
    cat.text(M, y, subtitle, "DispR", 27, "#EDE6D6")
    y -= 26
    cat.rule(M, y, 92, GOLD, 2.2)
    y -= 24
    cat.para(M, y, CW - 120, tagline, "UI", 10, 15, "#CFC7B6")

    cat.text(M, 46, footer, "UISB", 8.2, GOLD, track=1.6)


def story(cat, label, title, sub, hero, side_a, side_b, body, stats):
    cat.new()
    y = cat.head(label, title, sub)
    top = y - 26
    gh = 330
    gw_l = CW * 0.605
    gap = 14
    cat.img(hero, M, top - gh, gw_l, gh, r=12)
    sh = (gh - gap) / 2
    cat.img(side_a, M + gw_l + gap, top - sh, CW - gw_l - gap, sh, r=12)
    cat.img(side_b, M + gw_l + gap, top - gh, CW - gw_l - gap, sh, r=12)

    y = top - gh - 44
    cat.para(M, y, CW * 0.82, body, "UI", 10.2, 17.4, BODY)

    y = 126                                   # stats anchored to the page foot
    cat.c.setStrokeColor(LINE)
    cat.c.setLineWidth(0.7)
    cat.c.line(M, y + 26, W - M, y + 26)
    colw = CW / len(stats)
    for i, (h, t) in enumerate(stats):
        x = M + i * colw
        cat.label(x, y, h, GOLD)
        cat.para(x, y - 16, colw - 18, t, "UI", 8.8, 13, MUTED)
    cat.foot()


def feature(cat, label, title, sub, hero, cards, pill=None, note=None):
    cat.new()
    y = cat.head(label, title, sub)
    ih = 268
    top = y - 24
    cat.img(hero, M, top - ih, CW, ih, r=14)

    by = top - ih - 22
    ch = 176 if not note else 196
    cat.rrect(M, by - ch, CW, ch, 16, fill=INK_SOFT, stroke=GOLD_DK, lw=0.9)
    n = len(cards)
    inner = CW - 44
    cgap = 13
    cw = (inner - cgap * (n - 1)) / n
    cy = by - 30
    for i, (h, t) in enumerate(cards):
        x = M + 22 + i * (cw + cgap)
        cat.c.setFillColor(GOLD)
        cat.c.rect(x, cy - 58, 1.6, 58, stroke=0, fill=1)
        hy = cat.para(x + 11, cy - 11, cw - 14, h, "Disp", 11.4, 14.5, WHITE_P)
        cat.para(x + 11, hy - 15, cw - 14, t, "UI", 8.2, 12, "#B7AE9C")
    if pill:
        px = M + 22
        pw = cat.tw(pill.upper(), "UIB", 7.6, 1.8) + 30
        cat.rrect(px, by - ch + 22, pw, 22, 11, fill=GOLD)
        cat.text(px + 15, by - ch + 29.5, pill.upper(), "UIB", 7.6, "#1A1410", track=1.8)
    if note:
        cat.para(M + 22, by - ch + 62, CW - 44, note, "UI", 8.4, 12.5, "#9E9788")
    cat.foot()


def gallery(cat, label, title, sub, tiles, cols=2):
    cat.new()
    y = cat.head(label, title, sub)
    top = y - 26
    gap = 14
    tw_ = (CW - gap * (cols - 1)) / cols
    rows = math.ceil(len(tiles) / cols)
    avail = top - 78
    th_ = (avail - gap * (rows - 1)) / rows - 30
    for i, (path, cap, desc) in enumerate(tiles):
        r, cc = divmod(i, cols)
        x = M + cc * (tw_ + gap)
        yy = top - (r + 1) * th_ - r * (gap + 30)
        cat.img(path, x, yy, tw_, th_, r=12)
        cat.text(x, yy - 15, cap, "Disp", 11.4, "#171C1E")
        cat.text(x, yy - 26, desc.upper(), "UISB", 6.8, GOLD, track=1.4)
    cat.foot()


def duo(cat, label, title, sub, big, small, body, bullets):
    cat.new()
    y = cat.head(label, title, sub)
    top = y - 24
    ih = 300
    cat.img(big, M, top - ih, CW, ih, r=14)
    y = top - ih - 24
    ih2 = y - 122
    lw_ = CW * 0.50
    cat.img(small, M, y - ih2, lw_, ih2, r=12)
    tx = M + lw_ + 24
    twid = CW - lw_ - 24
    ty = cat.para(tx, y - 12, twid, body, "UI", 9.6, 15.6, BODY)
    ty -= 24
    for b in bullets:
        cat.c.setFillColor(GOLD)
        cat.c.circle(tx + 3, ty + 3.2, 2.4, stroke=0, fill=1)
        ty = cat.para(tx + 14, ty, twid - 14, b, "UI", 9, 13, MUTED) - 14
    cat.foot()


def swatches(cat, label, title, sub, items, cols=4, drawer=None, rows_note=None):
    """items: (name, meta, payload) — payload handed to drawer(cat,x,y,w,h,payload)."""
    cat.new()
    y = cat.head(label, title, sub)
    top = y - 26
    gap = 14
    tw_ = (CW - gap * (cols - 1)) / cols
    rows = math.ceil(len(items) / cols)
    block = (top - 96) / rows
    sh = block - 44
    for i, (name, meta, payload) in enumerate(items):
        r, cc = divmod(i, cols)
        x = M + cc * (tw_ + gap)
        yy = top - (r + 1) * sh - r * 44
        drawer(cat, x, yy, tw_, sh, payload)
        cat.c.setStrokeColor(LINE)
        cat.c.setLineWidth(0.7)
        cat.c.roundRect(x, yy, tw_, sh, 10, stroke=1, fill=0)
        cat.text(x, yy - 15, name, "Disp", 10.6, "#171C1E")
        cat.text(x, yy - 26, meta.upper(), "UISB", 6.6, MUTED, track=1.3)
    if rows_note:
        cat.para(M, 96, CW * 0.78, rows_note, "UI", 8.6, 12.8, MUTED)
    cat.foot()


def spec(cat, label, title, sub, cols, rows, note=None):
    cat.new()
    y = cat.head(label, title, sub)
    top = y - 34
    widths = [CW * f for f in cols[1]]
    xs, acc = [], M
    for wd in widths:
        xs.append(acc)
        acc += wd

    cat.c.setFillColor(INK_SOFT)
    cat.c.rect(M, top - 24, CW, 24, stroke=0, fill=1)
    for i, hcell in enumerate(cols[0]):
        cat.text(xs[i] + 10, top - 16, hcell.upper(), "UIB", 7.2, GOLD_BR, track=1.4)

    all_cells = [[cat.wrap(str(v), "UI", 8.6, widths[i] - 20) for i, v in enumerate(row)]
                 for row in rows]
    nat = [max(26, 12 + max(len(x) for x in cells) * 12) for cells in all_cells]
    floor_y = 150 if note else 118
    slack = max(0.0, (top - 24 - floor_y) - sum(nat)) / len(rows)

    yy = top - 24
    for ri, row in enumerate(rows):
        cells = all_cells[ri]
        rh = nat[ri] + slack
        if ri % 2 == 0:
            cat.c.setFillColor(PAPER_W)
            cat.c.rect(M, yy - rh, CW, rh, stroke=0, fill=1)
        for i, lines in enumerate(cells):
            fnt = "UISB" if i == 0 else "UI"
            col = "#1F2426" if i == 0 else BODY
            base = yy - (rh - (len(lines) - 1) * 12) / 2 - 3
            for li, ln in enumerate(lines):
                cat.text(xs[i] + 10, base - li * 12, ln, fnt, 8.6, col)
        cat.c.setStrokeColor(LINE)
        cat.c.setLineWidth(0.6)
        cat.c.line(M, yy - rh, W - M, yy - rh)
        yy -= rh
    if note:
        cat.para(M, yy - 24, CW * 0.86, note, "UI", 8.4, 12.6, MUTED)
    cat.foot()


def process(cat, label, title, sub, steps, hero=None):
    cat.new()
    y = cat.head(label, title, sub)
    top = y - 28
    if hero:
        ih = 176
        cat.img(hero, M, top - ih, CW, ih, r=14)
        top = top - ih - 30
    n = len(steps)
    for i, (h, t) in enumerate(steps):
        yy = top - i * ((top - 90) / n)
        cat.c.setStrokeColor(GOLD)
        cat.c.setLineWidth(1)
        cat.c.circle(M + 15, yy - 8, 15, stroke=1, fill=0)
        cat.text(M + 15, yy - 12, "%02d" % (i + 1), "UISB", 9, GOLD, align="c")
        cat.text(M + 46, yy - 4, h, "Disp", 14, "#171C1E")
        cat.para(M + 46, yy - 22, CW - 60, t, "UI", 9, 13.4, MUTED)
        if i < n - 1:
            cat.c.setStrokeColor(LINE)
            cat.c.setLineWidth(0.6)
            cat.c.line(M, yy - 40, W - M, yy - 40)
    cat.foot()


def grid_cards(cat, label, title, sub, cards, cols=3, hero=None):
    cat.new()
    y = cat.head(label, title, sub)
    top = y - 26
    gap = 14
    cw = (CW - gap * (cols - 1)) / cols
    rows = math.ceil(len(cards) / cols)
    ch = max(48 + len(cat.wrap(h, "Disp", 12.4, cw - 32)) * 15
             + len(cat.wrap(t, "UI", 8.5, cw - 32)) * 12.4
             for h, t in cards)
    grid_h = rows * ch + gap * (rows - 1)
    if hero:
        # the hero soaks up whatever height the cards do not need
        ih = max(140.0, top - 96 - grid_h - 26)
        cat.img(hero, M, top - ih, CW, ih, r=14)
        top = top - ih - 26
    else:
        top -= min(70.0, max(0.0, top - 96 - grid_h) / 2)
    for i, (h, t) in enumerate(cards):
        r, cc = divmod(i, cols)
        x = M + cc * (cw + gap)
        yy = top - (r + 1) * ch - r * gap
        cat.rrect(x, yy, cw, ch, 12, fill=PAPER_W, stroke=LINE, lw=0.7)
        cat.c.setFillColor(GOLD)
        cat.c.rect(x + 16, yy + ch - 26, 22, 1.8, stroke=0, fill=1)
        hy = cat.para(x + 16, yy + ch - 48, cw - 32, h, "Disp", 12.4, 15, "#171C1E")
        cat.para(x + 16, hy - 17, cw - 32, t, "UI", 8.5, 12.4, MUTED)
    cat.foot()


def back_cover(cat, hero, kicker, title, sub, contact_rows, closing):
    cat.new(INK)
    cat.shade_img(hero, 0, 0, W, H, r=0, dpi=150, bands=(
        (INK, (0.88, 0.62), 0.0, 1.0),
    ))
    c = cat.c
    lg = ImageReader(logo_png())
    lw = 92
    c.drawImage(lg, M, H - 66 - lw, lw, lw, mask="auto",
                preserveAspectRatio=True, anchor="nw")

    y = H - 66 - lw - 44
    cat.label(M, y, kicker, GOLD, size=8)
    y -= 40
    cat.text(M, y, title, "Disp", 31, WHITE_P)
    y -= 22
    cat.para(M, y, CW - 90, sub, "UI", 9.6, 14.6, "#C9C1B1")

    boxh = 40 + len(contact_rows) * 34
    by = 150
    cat.rrect(M, by, CW, boxh, 16, fill=None, stroke=GOLD_DK, lw=1)
    c.setFillColor("#0E1315", alpha=0.55)
    c.roundRect(M, by, CW, boxh, 16, stroke=0, fill=1)
    c.setFillAlpha(1)
    yy = by + boxh - 30
    for i, (k, v) in enumerate(contact_rows):
        cat.label(M + 22, yy, k, GOLD, size=7.2)
        cat.text(M + 118, yy, v, "UI", 9, "#E4DED0")
        if i < len(contact_rows) - 1:
            c.setStrokeColor("#3A3226")
            c.setLineWidth(0.6)
            c.line(M + 22, yy - 12, W - M - 22, yy - 12)
        yy -= 34

    c.setFillColor(GOLD)
    c.rect(M, 96, CW, 1.4, stroke=0, fill=1)
    cat.text(M, 76, closing, "UISB", 7.4, GOLD, track=1.6)


# ---------- swatch drawers ----------
def flat_drawer(cat, x, y, w, h, payload):
    """payload = (fill, accent) — simple tinted glass / paint chip."""
    fill, accent = payload
    c = cat.c
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, 10)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(fill)
    c.rect(x, y, w, h, stroke=0, fill=1)
    c.setFillColor(accent, alpha=0.55)
    c.saveState()
    c.translate(x + w * 0.5, y + h * 0.5)
    c.rotate(24)
    c.rect(-w * 0.16, -h, w * 0.20, h * 2, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor("#FFFFFF", alpha=0.30)
    c.saveState()
    c.translate(x + w * 0.22, y + h * 0.5)
    c.rotate(24)
    c.rect(-w * 0.05, -h, w * 0.07, h * 2, stroke=0, fill=1)
    c.restoreState()
    c.setFillAlpha(1)
    c.restoreState()
