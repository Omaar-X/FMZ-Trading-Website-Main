# -*- coding: utf-8 -*-
"""FM Trading F.Z.E — Glass Works catalogue."""
import os
from catbuild import *

G = "assets/images/glass/"
OUT = os.path.join(ROOT, "assets/Catalogue/FM_Trading_Glass_Works_Catalogue.pdf")

cat = Cat(OUT)

# 01 — cover
cover(cat,
      G + "panoramic-glass-wall-modern-office.webp",
      "FM Trading F.M.Z",
      "GLASS WORKS",
      "Signature Collection",
      "Tempered clarity. Frameless precision. Flawless installation across the UAE.",
      "AJMAN CHINA MALL  |  SHOP DB 030  |  GATE 7")

# 02 — brand story
story(cat, "Brand Story", "Clarity, Cut to Fit Your Space",
      "Precision glass for bathrooms, offices and living interiors.",
      G + "frameless-glass-shower-marble-bathroom.webp",
      G + "luxury-marble-bathroom-glass-enclosure.webp",
      G + "glass-partition-office-conference-room.webp",
      "FM Trading F.M.Z fabricates and installs safety-grade architectural glass — frameless "
      "shower enclosures, office and room partitions, mirrors and splashbacks. Every panel is "
      "measured on site, tempered for safety, edge-polished by hand and fitted with hardware "
      "chosen to match the finishes already in your room.",
      [("Tempered", "Safety-grade glass on every panel we supply."),
       ("Precision", "Site-measured and CNC-cut to the millimetre."),
       ("Complete", "Design, fabrication and installation in one team.")])

# 03 — frameless showers
feature(cat, "Bath & Shower", "Frameless Shower Enclosures",
        "Minimal hardware, maximum light — built around your bathroom, not a standard size.",
        G + "minimalist-frameless-glass-shower.webp",
        [("Frameless Build", "Slim hinges and clamps only — no bulky aluminium frame."),
         ("10mm Tempered", "Heat-treated safety glass with hand-polished edges."),
         ("Easy-Clean Coat", "Optional nano coating that repels limescale and soap."),
         ("Custom Hardware", "Brass, chrome, matte black or champagne finishes.")],
        pill="Custom sizes available",
        note="Also available: 8mm framed and semi-frameless systems, sliding door tracks, "
             "walk-in fixed panels and steam-room enclosures.")

# 04 — shower gallery
gallery(cat, "Collection", "Bath Enclosures in Place",
        "A selection of enclosures completed for homes and hotel apartments.",
        [(G + "clean-modern-glass-shower-bathtub.webp", "Bath Screen", "Hinged · 8mm clear"),
         (G + "elegant-glass-shower-bathtub-bathroom.webp", "Corner Enclosure", "Frameless · 10mm"),
         (G + "contemporary-glass-shower-wood-flooring.webp", "Walk-In Panel", "Fixed · matte black"),
         (G + "mediterranean-marble-glass-shower-bathroom.webp", "Marble Suite", "Frameless · low-iron")])

# 05 — partitions
feature(cat, "Commercial", "Office & Room Partitions",
        "Daylight through the whole floor plate, with acoustic separation where you need it.",
        G + "glass-partition-office-conference-room.webp",
        [("Single Glazed", "10–12mm tempered panels with slim floor and ceiling tracks."),
         ("Double Glazed", "Twin-pane cavity system for meeting rooms and offices."),
         ("Frosted Bands", "Manifestation film or acid-etched privacy strips."),
         ("Doors & Locks", "Patch-fitting glass doors, floor springs and access control.")],
        pill="Fast-track fit-out",
        note="Suitable for offices, clinics, showrooms, retail units and residential room dividers.")

# 06 — partition duo
duo(cat, "Workspace", "Glass Walls That Open Up a Floor",
    "Panoramic glazing and cubicle systems delivered as a single package.",
    G + "panoramic-glass-wall-modern-office.webp",
    G + "office-cubicles-glass-partition-walls.webp",
    "We survey the site, produce a shop drawing for approval, then fabricate and install — "
    "including tracks, seals, hardware and any film or branding applied to the glass.",
    ["Floor-to-ceiling panels up to 3.2m in height",
     "Butt-jointed or slim-profile aluminium framing",
     "Acoustic seals for meeting and consultation rooms",
     "Company logo and manifestation film applied on site"])

# 07 — finishes
swatches(cat, "Finishes", "Glass & Hardware Finishes",
         "Choose the glass tone and the metal that surrounds it.",
         [("Clear Float", "Standard tempered", ("#DCE8E6", "#FFFFFF")),
          ("Low-Iron", "Ultra clear", ("#E9F3F0", "#FFFFFF")),
          ("Bronze Tint", "Warm privacy", ("#8A6B49", "#D6B48A")),
          ("Grey Tint", "Cool privacy", ("#6F7B7E", "#C3CDCF")),
          ("Acid Etched", "Frosted matte", ("#D2D8D5", "#F2F5F3")),
          ("Reflective", "One-way daytime", ("#4E6367", "#9FB6B9")),
          ("Brushed Brass", "Hardware", ("#B08D4F", "#E4C588")),
          ("Matte Black", "Hardware", ("#232626", "#5A5F5F"))],
         cols=4, drawer=flat_drawer,
         rows_note="Chips are indicative. Physical glass and hardware samples are available at "
                   "our Ajman China Mall showroom, Shop DB 030, Gate 7.")

# 08 — specifications
spec(cat, "Technical", "Specifications & Applications",
     "Standard build-ups we supply. Non-standard sizes are quoted on survey.",
     (["Product", "Thickness", "Typical Application", "Finish Options"],
      [0.26, 0.14, 0.34, 0.26]),
     [["Frameless shower", "10 / 12 mm", "Bathrooms, en-suites, hotel apartments",
       "Clear, low-iron, frosted"],
      ["Framed shower", "6 / 8 mm", "Compact bathrooms, staff accommodation",
       "Clear, frosted"],
      ["Office partition", "10 / 12 mm", "Meeting rooms, workstations, clinics",
       "Clear, tinted, film-banded"],
      ["Double glazed partition", "10 + 10 mm", "Acoustic meeting rooms, executive offices",
       "Clear, integrated blinds"],
      ["Glass door", "10 / 12 mm", "Entrances, partitions, retail",
       "Patch fitting, floor spring"],
      ["Mirror", "5 / 6 mm", "Vanity, wardrobe, gym, feature walls",
       "Silver, bronze, antique"],
      ["Splashback", "6 mm", "Kitchens, vanity counters",
       "Back-painted any RAL colour"],
      ["Balustrade", "12 / 17.5 mm", "Stairs, balconies, terraces",
       "Clear, laminated, spigot fixed"]],
     note="All tempered glass is supplied to BS EN 12150 safety standards and permanently "
          "stamped. Laminated build-ups are available where a fall risk exists.")

# 09 — process
process(cat, "How We Work", "From Survey to Silicone",
        "A five-step process that keeps the site clean and the schedule predictable.",
        [("Site Survey", "We measure openings, check levels and confirm access — no guesswork "
                         "from floor plans alone."),
         ("Drawing & Quote", "You receive a shop drawing with glass type, hardware finish and a "
                             "fixed price before anything is cut."),
         ("Fabrication", "Panels are cut, edge-polished, drilled and tempered to your approved "
                         "drawing."),
         ("Installation", "Our fitters install tracks, panels and hardware, then seal and clean "
                          "the same day where possible."),
         ("Handover", "We test doors, adjust hinges, remove protection film and walk the job "
                      "with you before sign-off.")])

# 10 — mirrors & extras
grid_cards(cat, "Also Available", "Beyond the Enclosure",
           "The rest of the glass package, from the same team and the same visit.",
           [("Feature Mirrors", "LED-lit, bevelled, antique and full-wall mirrors cut to any "
                                "shape for vanities, gyms and living rooms."),
            ("Kitchen Splashbacks", "Back-painted toughened glass in any colour — seamless, "
                                    "heat-safe and wiped clean in seconds."),
            ("Balustrades", "Laminated glass balustrades with spigot, channel or standoff "
                            "fixings for stairs, balconies and terraces."),
            ("Shopfronts", "Toughened glass shopfronts, display windows and patch-fitted "
                           "entrance doors for retail units."),
            ("Frosting & Film", "Privacy film, manifestation bands, safety film and printed "
                                "logo graphics applied on site."),
            ("Repairs & Refits", "Cracked panel replacement, hinge and roller renewal, door "
                                 "realignment and re-sealing.")],
           cols=3)

# 11 — why us
grid_cards(cat, "The FM Difference", "Why Clients Keep Calling Us Back",
           None,
           [("Safety First", "Every panel is tempered, stamped and installed to standard — no "
                             "shortcuts on glass that people walk into."),
            ("One Team", "Survey, fabrication and installation stay in-house, so nothing gets "
                         "lost between suppliers."),
            ("Clean Sites", "Protection down, offcuts removed, silicone tooled and glass "
                            "polished before we leave."),
            ("Fair Pricing", "A fixed quote from the drawing — no surprises once the job "
                             "starts."),
            ("Fast Response", "Site survey within 48 hours across Ajman, Sharjah, Dubai and the "
                              "Northern Emirates."),
            ("After Care", "Hinge adjustment, re-sealing and replacement support long after "
                           "handover.")],
           cols=3, hero=G + "luxury-marble-bathroom-glass-enclosure.webp")

# 12 — care
grid_cards(cat, "Care Guide", "Keeping Glass Looking New",
           "Five minutes a week is all a frameless enclosure needs.",
           [("Squeegee Daily", "A quick pull-down after showering stops limescale before it "
                               "bonds to the surface."),
            ("Mild Cleaners Only", "Use a non-abrasive glass cleaner. Avoid scouring pads and "
                                   "strong acids on coated glass."),
            ("Check the Seals", "Replace worn PVC seals every few years to keep water inside "
                                "the enclosure."),
            ("Mind the Hardware", "Wipe hinges dry and tighten fixings annually — we can do "
                                  "this on a service visit.")],
           cols=2, hero=G + "contemporary-glass-shower-wood-flooring.webp")

# 13 — back cover
back_cover(cat,
           G + "minimalist-frameless-glass-shower.webp",
           "Let us glaze your project",
           "Book a Free Site Survey",
           "Glass works, curtains, flooring, TV decor, wallpaper and artificial grass — one "
           "supplier for the whole interior.",
           [("Contact", "MD Shohel"),
            ("Phone", "056 727 5998   |   058 957 9733   |   050 506 5399"),
            ("Email", "kazishohel5511@gmail.com"),
            ("Location", "Shop DB 030, Gate 7, Ajman China Mall, U.A.E"),
            ("Services", "Curtain  |  Flooring  |  TV Decor  |  Glass  |  Wall Paper  |  Grass")],
           "FM TRADING F.M.Z  ·  INTERIOR DESIGN & DECORATION")

cat.save()
print("wrote", OUT, round(os.path.getsize(OUT) / 1024), "KB", cat.page, "pages")
