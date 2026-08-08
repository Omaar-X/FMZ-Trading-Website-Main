# -*- coding: utf-8 -*-
"""FM Trading F.Z.E — Wallpaper catalogue."""
import os, math
from catbuild import *

P = "assets/images/wallpaper/"
OUT = os.path.join(ROOT, "assets/Catalogue/FM_Trading_Wallpaper_Catalogue.pdf")


# ---------- pattern swatch drawer ----------
def pattern_drawer(cat, x, y, w, h, payload):
    kind, base, accent = payload
    c = cat.c
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, 10)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(base)
    c.rect(x, y, w, h, stroke=0, fill=1)
    c.setFillColor(accent)
    c.setStrokeColor(accent)

    if kind == "plain":                                   # subtle linen weave
        c.setStrokeColor(accent, alpha=0.5)
        c.setLineWidth(0.5)
        for i in range(0, int(h), 4):
            c.line(x, y + i, x + w, y + i)
        for i in range(0, int(w), 4):
            c.line(x + i, y, x + i, y + h)

    elif kind == "stripe":
        sw = w / 9.0
        for i in range(0, 10, 2):
            c.rect(x + i * sw, y, sw, h, stroke=0, fill=1)

    elif kind == "damask":
        step = w / 3.0
        c.setLineWidth(1.1)
        for row in range(int(h / step) + 2):
            for col in range(4):
                cx = x + col * step + (step / 2 if row % 2 else 0)
                cy = y + row * step
                c.circle(cx, cy, step * 0.30, stroke=1, fill=0)
                c.circle(cx, cy, step * 0.13, stroke=0, fill=1)

    elif kind == "geometric":
        step = w / 4.0
        c.setLineWidth(1.0)
        for row in range(int(h / step) + 2):
            for col in range(6):
                cx = x + col * step - step / 2
                cy = y + row * step
                pth = c.beginPath()
                pth.moveTo(cx, cy - step * 0.42)
                pth.lineTo(cx + step * 0.42, cy)
                pth.lineTo(cx, cy + step * 0.42)
                pth.lineTo(cx - step * 0.42, cy)
                pth.close()
                c.drawPath(pth, stroke=1, fill=0)

    elif kind == "floral":
        step = w / 3.2
        for row in range(int(h / step) + 2):
            for col in range(5):
                cx = x + col * step + (step / 2 if row % 2 else 0)
                cy = y + row * step
                for a in range(6):
                    ang = math.radians(a * 60)
                    c.circle(cx + math.cos(ang) * step * 0.16,
                             cy + math.sin(ang) * step * 0.16,
                             step * 0.11, stroke=0, fill=1)

    elif kind == "panel3d":                               # fluted 3D panel
        sw = w / 8.0
        for i in range(9):
            c.setFillColor(accent, alpha=0.85)
            c.rect(x + i * sw, y, sw * 0.52, h, stroke=0, fill=1)
            c.setFillColor("#FFFFFF", alpha=0.16)
            c.rect(x + i * sw, y, sw * 0.16, h, stroke=0, fill=1)
        c.setFillAlpha(1)

    elif kind == "marble":
        veins = ((0.88, 0.98, 2.6), (0.74, 0.86, 1.2), (0.70, 0.80, 0.6),
                 (0.55, 0.66, 2.2), (0.49, 0.60, 0.9),
                 (0.34, 0.45, 2.4), (0.29, 0.40, 0.7),
                 (0.14, 0.24, 1.8), (0.05, 0.13, 0.9))
        for sy, ey, lw_ in veins:
            c.setStrokeColor(accent, alpha=0.30 + lw_ * 0.16)
            c.setLineWidth(lw_)
            pth = c.beginPath()
            pth.moveTo(x - 2, y + h * sy)
            pth.curveTo(x + w * 0.30, y + h * (sy + 0.07),
                        x + w * 0.66, y + h * (ey - 0.09),
                        x + w + 2, y + h * ey)
            c.drawPath(pth, stroke=1, fill=0)

    elif kind == "wood":
        c.setStrokeColor(accent, alpha=0.7)
        c.setLineWidth(0.9)
        for i in range(0, int(w), 9):
            pth = c.beginPath()
            pth.moveTo(x + i, y)
            pth.curveTo(x + i + 4, y + h * 0.33, x + i - 4, y + h * 0.66,
                        x + i + 2, y + h)
            c.drawPath(pth, stroke=1, fill=0)

    elif kind == "mural":
        c.setFillColor(accent, alpha=0.9)
        pth = c.beginPath()
        pth.moveTo(x, y + h * 0.42)
        pth.lineTo(x + w * 0.30, y + h * 0.78)
        pth.lineTo(x + w * 0.52, y + h * 0.55)
        pth.lineTo(x + w * 0.78, y + h * 0.88)
        pth.lineTo(x + w, y + h * 0.60)
        pth.lineTo(x + w, y)
        pth.lineTo(x, y)
        pth.close()
        c.drawPath(pth, stroke=0, fill=1)
        c.setFillColor("#FFFFFF", alpha=0.55)
        c.circle(x + w * 0.72, y + h * 0.80, w * 0.09, stroke=0, fill=1)
        c.setFillAlpha(1)

    c.setStrokeAlpha(1)
    c.setFillAlpha(1)
    c.restoreState()


cat = Cat(OUT)

# 01 — cover
cover(cat,
      P + "luxurious-bedroom-chandelier-wallpaper.webp",
      "FM Trading F.M.Z",
      "WALL PAPER",
      "Designer Collection",
      "Texture, pattern and depth — imported rolls, custom murals, bubble-free application.",
      "AJMAN CHINA MALL  |  SHOP DB 030  |  GATE 7")

# 02 — brand story
story(cat, "Brand Story", "Walls That Set the Mood",
      "Designer wallcoverings supplied, matched and applied by one team.",
      P + "elegant-bedroom-accent-wallpaper.webp",
      P + "modern-bedroom-designer-wallpaper.webp",
      P + "green-accent-wall-elegant-bedroom.webp",
      "Paint gives a wall a colour; wallpaper gives it a character. FM Trading F.M.Z stocks "
      "imported vinyl, non-woven and fabric-backed wallcoverings alongside made-to-measure "
      "photo murals — then prepares, primes and papers the wall so the pattern lines up and "
      "the seams disappear.",
      [("Curated", "Hundreds of designs, shortlisted to suit your room."),
       ("Measured", "We calculate rolls and pattern repeat for you."),
       ("Applied", "Wall prep, priming and bubble-free installation.")])

# 03 — accent walls
feature(cat, "Signature", "Bedroom Accent Walls",
        "One papered wall changes the whole room — usually behind the headboard.",
        P + "carved-headboard-striped-wallpaper-bedroom.webp",
        [("Pattern Match", "Repeats aligned across every drop, seam to seam."),
         ("Wall Prep", "Filled, sanded and primed before a single roll goes up."),
         ("Washable Vinyl", "Wipe-clean surfaces that survive real bedrooms."),
         ("Trim & Finish", "Clean cuts at cornices, sockets and skirting.")],
        pill="Free room measure",
        note="Popular for master bedrooms, kids' rooms, majlis feature walls, headboard "
             "recesses and hallway panels.")

# 04 — gallery
gallery(cat, "Collection", "Rooms We Have Papered",
        "A selection of accent walls and full-room installations.",
        [(P + "modern-bedroom-wallpaper-blue-accent.webp", "Blue Accent", "Non-woven · matte"),
         (P + "bright-luxury-bedroom-wallpaper-design.webp", "Bright Luxe", "Vinyl · soft sheen"),
         (P + "dark-accent-wallpaper-modern-bedroom.webp", "Dark Feature", "Textured · deep tone"),
         (P + "spacious-bedroom-stylish-wallpaper.webp", "Full Room", "Fabric-backed · washable")])

# 05 — geometric & textured
feature(cat, "Texture", "Geometric & 3D Panelling",
        "Relief patterns that catch the light and give a flat wall real depth.",
        P + "geometric-pattern-accent-wall.webp",
        [("Embossed Vinyl", "Raised patterns you can feel, printed on heavy stock."),
         ("3D Wall Panels", "PVC and PU panels for fluted and coffered effects."),
         ("Metallic Inks", "Gold, bronze and pewter highlights under warm light."),
         ("Grasscloth", "Natural fibre wallcoverings with a woven texture.")],
        pill="Sample panels in showroom")

# 06 — duo
duo(cat, "Living Spaces", "Beyond the Bedroom",
    "Majlis walls, living rooms, hallways and commercial interiors.",
    P + "luxurious-bedroom-chandelier-wallpaper.webp",
    P + "modern-bedroom-wallpaper-blue-accent.webp",
    "Wallpaper is not only for bedrooms. We paper majlis feature walls, TV walls, staircases, "
    "reception areas, salons and clinics — matching the wallcovering to the flooring and "
    "curtains supplied in the same package.",
    ["Majlis and living-room feature walls",
     "TV wall panelling combined with our TV decor service",
     "Hallways, staircases and ceiling papers",
     "Salons, clinics, offices and retail fit-outs"])

# 07 — pattern families
swatches(cat, "Pattern Families", "The Design Families We Stock",
         "Start with a family, then narrow down to a colourway in the showroom.",
         [("Plain Texture", "Linen · woven", ("plain", "#E4DED2", "#C9BFAC")),
          ("Classic Stripe", "Vertical repeat", ("stripe", "#EFE9DC", "#C8A96A")),
          ("Damask", "Traditional", ("damask", "#E7E1D4", "#A98C55")),
          ("Geometric", "Modern repeat", ("geometric", "#E6EAE7", "#5E7C7A")),
          ("Floral", "Botanical", ("floral", "#EFE6E6", "#B98089")),
          ("3D Panel", "Fluted relief", ("panel3d", "#E9E4D8", "#B7A183")),
          ("Marble", "Stone effect", ("marble", "#EDEDEA", "#8E9AA0")),
          ("Wood Grain", "Timber effect", ("wood", "#E3D6C2", "#9A7346"))],
         cols=4, drawer=pattern_drawer,
         rows_note="Swatches are illustrative of each family. Full pattern books and A4 samples "
                   "are available at our Ajman China Mall showroom, Shop DB 030, Gate 7.")

# 08 — specifications
spec(cat, "Technical", "Materials & Specifications",
     "What each material is best at, so the right one ends up on your wall.",
     (["Material", "Roll Size", "Best For", "Cleaning"],
      [0.24, 0.17, 0.34, 0.25]),
     [["Non-woven", "0.53 × 10 m", "Bedrooms, living rooms, easy future removal",
       "Damp cloth"],
      ["Vinyl coated", "0.53 × 10 m", "Kids' rooms, hallways, high-traffic walls",
       "Washable / scrubbable"],
      ["Heavy vinyl", "1.06 × 15.6 m", "Offices, clinics, hotels, commercial corridors",
       "Scrubbable"],
      ["Fabric backed", "0.70 × 10 m", "Majlis, master bedrooms, feature walls",
       "Dry dusting only"],
      ["Grasscloth", "0.91 × 5.5 m", "Luxury feature walls, studies",
       "Dry dusting only"],
      ["3D PVC panel", "Per panel", "TV walls, headboard recesses, reception desks",
       "Damp cloth"],
      ["Custom mural", "Made to size", "Any wall — printed to your exact measurement",
       "Laminate optional"],
      ["Self-adhesive", "0.45 × 10 m", "Rentals, cupboards, quick refreshes",
       "Damp cloth"]],
     note="Standard pattern repeats run 32–64 cm. We allow for repeat and wastage when "
          "calculating your roll count, so you are not left one drop short.")

# 09 — custom murals
grid_cards(cat, "Made To Measure", "Custom Photo Murals",
           "Any image, printed to the exact width and height of your wall.",
           [("Your Own Image", "Send a photo or artwork — we check the resolution and print it "
                               "at wall scale."),
            ("Design Library", "Thousands of licensed mural designs: landscapes, marble, city "
                               "skylines, kids' themes."),
            ("Seamless Panels", "Printed as numbered drops that line up edge to edge with no "
                                "visible join."),
            ("Matte or Satin", "Choose the finish to suit the lighting in the room."),
            ("Laminated Option", "Extra protective layer for corridors, nurseries and "
                                 "commercial spaces."),
            ("Fitted By Us", "Printed, delivered and installed by the same team that measured "
                             "the wall.")],
           cols=3, hero=P + "dark-accent-wallpaper-modern-bedroom.webp")

# 10 — process
process(cat, "How We Work", "From Sample to Seamless",
        "Five steps between choosing a pattern and living with it.",
        [("Choose Your Pattern", "Browse the books in our showroom or send us a reference "
                                 "image — we shortlist matching designs."),
         ("Free Site Measure", "We measure the wall, check its condition and calculate rolls "
                               "including pattern repeat."),
         ("Quotation", "A fixed price covering material, wall preparation, adhesive and "
                       "installation."),
         ("Wall Preparation", "Cracks filled, surfaces sanded and primed — the step that "
                              "decides how good the finish looks."),
         ("Installation", "Drops hung, patterns aligned, edges trimmed and the room left "
                          "clean the same day.")])

# 11 — why us
grid_cards(cat, "The FM Difference", "Why Trust Us With Your Walls",
           None,
           [("Genuine Stock", "Imported rolls from established mills — not thin copies that "
                              "peel at the seams."),
            ("Correct Quantity", "We calculate repeat and wastage so batches match and nothing "
                                 "runs out mid-wall."),
            ("Same Batch", "All rolls for one wall come from a single production batch, so the "
                           "colour is consistent."),
            ("Prep Included", "Filling, sanding and priming are part of the quote, not an "
                              "extra charge later."),
            ("Clean Finish", "Furniture covered, floors protected and the room tidied before "
                             "we leave."),
            ("Full Package", "Pair the wallpaper with our curtains, flooring and TV decor in "
                             "one visit.")],
           cols=3, hero=P + "spacious-bedroom-stylish-wallpaper.webp")

# 12 — care
grid_cards(cat, "Care Guide", "Looking After Wallpaper",
           "Simple habits that keep a papered wall looking new for years.",
           [("Dust, Don't Soak", "Dry-dust textured and fabric papers. Only vinyl grades should "
                                 "meet a damp cloth."),
            ("Blot Marks Early", "Wipe spills straight away with a soft cloth — never scrub a "
                                 "printed surface."),
            ("Watch The Humidity", "Keep AC and ventilation running in bathrooms and kitchens "
                                   "so seams stay closed."),
            ("Keep A Spare Roll", "Store one roll from the batch — small repairs then match "
                                  "perfectly years later.")],
           cols=2, hero=P + "modern-bedroom-designer-wallpaper.webp")

# 13 — back cover
back_cover(cat,
           P + "green-accent-wall-elegant-bedroom.webp",
           "Let us dress your walls",
           "Book a Free Wall Measure",
           "Wallpaper, curtains, flooring, TV decor, glass and artificial grass — one supplier "
           "for the whole interior.",
           [("Contact", "MD Shohel"),
            ("Phone", "056 727 5998   |   058 957 9733   |   050 506 5399"),
            ("Email", "kazishohel5511@gmail.com"),
            ("Location", "Shop DB 030, Gate 7, Ajman China Mall, U.A.E"),
            ("Services", "Curtain  |  Flooring  |  TV Decor  |  Glass  |  Wall Paper  |  Grass")],
           "FM TRADING F.M.Z  ·  INTERIOR DESIGN & DECORATION")

cat.save()
print("wrote", OUT, round(os.path.getsize(OUT) / 1024), "KB", cat.page, "pages")
