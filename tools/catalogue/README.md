# Catalogue builders

Source for the two catalogues that are generated rather than supplied as artwork:

| Script | Output |
| --- | --- |
| `build_glass.py` | `assets/Catalogue/FM_Trading_Glass_Works_Catalogue.pdf` |
| `build_wallpaper.py` | `assets/Catalogue/FM_Trading_Wallpaper_Catalogue.pdf` |

`catbuild.py` is the shared A4 layout engine — palette, page templates (cover, brand
story, feature, gallery, spec table, swatches, process, card grid, back cover) and the
image cropping cache. Copy and edit the content lists in the two build scripts to change
wording, page order or photography; they read images straight out of `assets/images/`.

## Running

```bash
pip install reportlab pillow pymupdf
python tools/catalogue/build_glass.py
python tools/catalogue/build_wallpaper.py
```

Run from the repo root. `ROOT` at the top of `catbuild.py` points at this project, and the
display/UI fonts are Georgia and Segoe UI loaded from `C:/Windows/Fonts` — change both if
you build on another machine.

## After rebuilding

Regenerate the cover thumbnail the catalogue page shows:

```bash
python -c "import fitz,io;from PIL import Image;p=fitz.open('assets/Catalogue/FM_Trading_Glass_Works_Catalogue.pdf')[0];z=900/p.rect.width;Image.open(io.BytesIO(p.get_pixmap(matrix=fitz.Matrix(z,z)).tobytes('png'))).convert('RGB').save('assets/images/catalog-thumbs/glass-catalogue-cover.jpg','JPEG',quality=84,optimize=True,progressive=True)"
```

Then update the page count and file size in the card's `.cat-meta` list in `catalog.html`.
