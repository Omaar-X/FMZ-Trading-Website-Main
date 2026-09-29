# -*- coding: utf-8 -*-
"""Build three curated FM Trading collection catalogues from existing product imagery."""
import os
from catbuild import *

OUT_DIR = os.path.join(ROOT, "output/pdf")
os.makedirs(OUT_DIR, exist_ok=True)

CONTACT = [
    ("Contact", "MD Shohel"),
    ("Phone", "056 727 5998   |   058 957 9733   |   050 506 5399"),
    ("Email", "kazishohel5511@gmail.com"),
    ("Location", "Shop DB 030, Gate 7, Ajman China Mall, U.A.E"),
]


def finish(cat, image, title, subtitle):
    back_cover(cat, image, "Designed around your space", title, subtitle,
               CONTACT + [("Service", "Free consultation, measurement and quotation")],
               "FM TRADING F.Z.E  |  INTERIOR DESIGN & DECORATION")
    cat.save()


def luxury_interiors():
    out = os.path.join(OUT_DIR, "FM-Trading-Luxury-Interiors-Collection.pdf")
    C = "assets/images/curtains/"
    Wp = "assets/images/wallpaper/"
    T = "assets/images/tv-decor/"
    cat = Cat(out)
    cover(cat, C + "modern-luxurious-living-room-curtains.webp", "FM Trading F.Z.E",
          "LUXURY INTERIORS", "Curated Collection",
          "Curtains, feature walls and TV decor composed as one refined interior.",
          "AJMAN CHINA MALL  |  SHOP DB 030  |  GATE 7")
    story(cat, "The Collection", "Layered Luxury, Made Personal",
          "A coordinated palette of fabric, texture, timber and light.",
          C + "luxury-living-room-beige-drapery.webp",
          Wp + "luxurious-bedroom-chandelier-wallpaper.webp",
          T + "luxury-marble-tv-feature-wall.webp",
          "This edit brings together our most elegant curtains, designer wallpaper and custom TV walls. "
          "Each element can be supplied separately or planned as a complete room package, measured and installed by our UAE team.",
          [("Coordinated", "Materials selected to sit beautifully together."),
           ("Made to Fit", "Every curtain and feature wall is site measured."),
           ("Installed", "One team from selection through final styling.")])
    gallery(cat, "Living Spaces", "Warm, Quiet and Refined",
            "Four directions for a premium lounge or family room.",
            [(C + "traditional-fireplace-room-drapery.webp", "Classic Drapery", "Full-height tailored folds"),
             (T + "modern-tv-shelving-lounge-decor.webp", "Integrated Media", "Storage and display"),
             (Wp + "green-accent-wall-elegant-bedroom.webp", "Soft Colour", "Calm feature wall"),
             (T + "elegant-living-room-large-tv-setup.webp", "Statement Wall", "Balanced luxury")])
    feature(cat, "Signature Detail", "Curtains That Finish the Room",
            "Control daylight, soften acoustics and introduce texture with made-to-measure drapery.",
            C + "ornate-dining-room-window-curtain.webp",
            [("Sheer + Blackout", "Layered performance for day and night."),
             ("Wave or Pinch Pleat", "Headers selected for the room style."),
             ("Motorised Option", "Quiet tracks for large glazing."),
             ("Full Installation", "Accurate drops, clean hems and aligned folds.")],
            pill="Made to measure")
    grid_cards(cat, "Complete the Look", "One Room, One Material Story", None,
               [("Designer Wallpaper", "Pattern, texture and colour selected around your furniture and lighting."),
                ("Custom TV Decor", "Panels, shelves and concealed wiring designed to fit the wall."),
                ("Curtain Styling", "Fabric, lining, track and header specified as one system."),
                ("Flooring Match", "Warm oak, cool grey and stone looks to anchor the palette."),
                ("Glass Details", "Mirrors and glass accents that increase light and depth."),
                ("On-Site Samples", "Compare finishes in the actual daylight of your room.")], cols=3,
               hero=T + "contemporary-tv-room-chandelier.webp")
    finish(cat, Wp + "bright-luxury-bedroom-wallpaper-design.webp", "Book a Free Interior Consultation",
           "Bring us your room dimensions or invite us to measure. We will build a coordinated proposal around your taste and budget.")
    return out


def office_glass():
    out = os.path.join(OUT_DIR, "FM-Trading-Office-and-Glass-Collection.pdf")
    G = "assets/images/glass/"
    F = "assets/images/flooring/"
    cat = Cat(out)
    cover(cat, G + "panoramic-glass-wall-modern-office.webp", "FM Trading F.Z.E",
          "OFFICE & GLASS", "Workspace Collection",
          "Bright partitions, durable flooring and a clean professional finish.",
          "AJMAN CHINA MALL  |  SHOP DB 030  |  GATE 7")
    story(cat, "Workspace Planning", "More Light. Better Separation.",
          "A practical fit-out package for offices, clinics and showrooms.",
          G + "glass-partition-office-conference-room.webp",
          G + "office-cubicles-glass-partition-walls.webp",
          F + "open-plan-grey.jpg",
          "Glass partitions keep daylight moving while creating focused rooms. Pair them with commercial-grade flooring, privacy film and coordinated hardware for a workspace that is easy to maintain and ready for daily use.",
          [("Measured", "Site survey and opening checks before fabrication."),
           ("Flexible", "Clear, frosted, framed and frameless options."),
           ("Complete", "Glass, doors, film and flooring from one supplier.")])
    feature(cat, "Partitions", "Glass Rooms Without the Visual Weight",
            "Create meeting rooms, consultation spaces and executive offices while preserving openness.",
            G + "glass-partition-office-conference-room.webp",
            [("Tempered Safety Glass", "Precision cut and edge polished."),
             ("Privacy Options", "Frosted bands, full film or company graphics."),
             ("Door Hardware", "Patch fittings, locks and floor springs."),
             ("Acoustic Upgrade", "Double-glazed systems for quieter rooms.")],
            pill="Survey available")
    gallery(cat, "Flooring", "Built for Everyday Movement",
            "Professional tones with straightforward maintenance.",
            [(F + "catalog-spc-grey-openplan.jpg", "Cool Grey SPC", "Open-plan offices"),
             (F + "hallway-grey.jpg", "Stone Grey", "Corridors and reception"),
             (F + "dining-natural-oak.jpg", "Natural Oak", "Executive rooms"),
             (F + "catalog-spc-kitchen.jpg", "Durable Finish", "Staff and service areas")])
    grid_cards(cat, "Project Scope", "Everything Around the Partition", None,
               [("Site Survey", "Measurements, levels, access and fixing conditions checked on site."),
                ("Shop Drawings", "Panel divisions, doors and hardware confirmed before production."),
                ("Privacy Film", "Manifestation bands, frosting and brand graphics installed cleanly."),
                ("Floor Preparation", "Subfloor checks and practical transition details."),
                ("Fast Installation", "Sequenced work to reduce disruption to your operation."),
                ("Aftercare", "Door adjustment, replacement seals and maintenance support.")], cols=3,
               hero=G + "panoramic-glass-wall-modern-office.webp")
    finish(cat, G + "office-cubicles-glass-partition-walls.webp", "Request a Workspace Survey",
           "Share your floor plan or book a site visit for a clear quotation covering partitions, doors, film and flooring.")
    return out


def outdoor_flooring():
    out = os.path.join(OUT_DIR, "FM-Trading-Outdoor-and-Flooring-Collection.pdf")
    Gr = "assets/images/grass/"
    F = "assets/images/flooring/"
    cat = Cat(out)
    cover(cat, Gr + "rooftop-terrace-artificial-grass-turf.webp", "FM Trading F.Z.E",
          "OUTDOOR & FLOORING", "Surface Collection",
          "Practical surfaces for terraces, balconies, family rooms and commercial spaces.",
          "AJMAN CHINA MALL  |  SHOP DB 030  |  GATE 7")
    story(cat, "Surface Solutions", "Comfort Underfoot, Indoors and Out",
          "Easy-care finishes selected for UAE homes and businesses.",
          Gr + "patio-furniture-artificial-grass-lawn.webp",
          F + "living-warm-oak.jpg",
          Gr + "zk-prime-house.jpg",
          "Artificial grass turns hard outdoor areas into inviting green zones, while SPC and laminate flooring bring warmth and durability indoors. We help select the right construction for traffic, moisture, sunlight and maintenance needs.",
          [("Durable", "Products chosen around real use conditions."),
           ("Comfortable", "Softer, quieter surfaces for everyday living."),
           ("Installed", "Preparation, fitting and clean handover included.")])
    gallery(cat, "Artificial Grass", "Green Spaces Without the Upkeep",
            "Options for rooftops, balconies, play zones and landscaping.",
            [(Gr + "zk-5g-roll.jpg", "5G Turf", "Dense premium pile"),
             (Gr + "zk-gold-hand.jpg", "ZK Gold", "Soft-touch finish"),
             (Gr + "zk-color-playground.jpg", "Colour Range", "Play and activity zones"),
             (Gr + "rooftop-terrace-artificial-grass-turf.webp", "Terrace Living", "Outdoor relaxation")])
    feature(cat, "Indoor Flooring", "A Strong Foundation for the Room",
            "Wood and stone looks with practical cleaning and reliable day-to-day performance.",
            F + "living-warm-oak.jpg",
            [("SPC Options", "Water-resistant rigid-core construction."),
             ("Natural Looks", "Oak, grey and warm neutral finishes."),
             ("Neat Transitions", "Skirting and profiles matched to the floor."),
             ("Professional Fit", "Subfloor checks and aligned installation.")],
            pill="Samples available")
    grid_cards(cat, "Choosing Well", "Match the Surface to the Space", None,
               [("Balconies", "Drainage-aware turf layouts with tidy perimeter finishing."),
                ("Rooftops", "Comfortable green zones for seating and family use."),
                ("Play Areas", "Soft, colourful options for active spaces."),
                ("Living Rooms", "Warm wood tones with easy daily cleaning."),
                ("Commercial Floors", "Durable neutrals designed around higher traffic."),
                ("Material Samples", "See colour and texture in your own lighting before ordering.")], cols=3,
               hero=F + "catalog-spc-golden-dining.jpg")
    finish(cat, Gr + "patio-furniture-artificial-grass-lawn.webp", "Book a Free Measurement",
           "Tell us where the surface will be used and we will recommend the right product, quantity and installation method.")
    return out


for builder in (luxury_interiors, office_glass, outdoor_flooring):
    path = builder()
    print("wrote", path, round(os.path.getsize(path) / 1024), "KB")
