# -*- coding: utf-8 -*-
"""
All editable site content lives here. Change a value, run `python3 build.py`,
and every page is regenerated into ../site/.

PRICES ARE DRAFT PLACEHOLDERS. Replace them with your real landed/retail
prices before going live. Set price to None to show "Price on request".
`was` (optional) shows a struck-through compare-at price and a "Save" label.
"""

SITE = {
    "brand": "Hoymiles PH",
    "domain": "hoymiles.ph",
    "url": "https://hoymiles.ph",
    # Legal entity that actually sells/installs. Shown in footer + About.
    "company": "",                                          # optional legal name; empty = brand
    "tagline": "Open energy for every Filipino home.",
    "footer_tag": ("Be solar-ready.", "Open energy for all."),
    # Leave empty to hide. Customers then reach you through the quote/contact form.
    "phones": [],
    "email": "",
    "address": "",
    "hours": "Mon–Sat, 8:00 AM – 6:00 PM",
    # Paste full links to show these icons (empty = hidden):
    "facebook": "",       # https://www.facebook.com/<your-page>
    "instagram": "",
    "messenger": "",      # https://m.me/<your-page>  (also shows the floating chat button)
    "viber": "",
    # Paste a Formspree / Web3Forms / Getform endpoint here to receive form
    # submissions by email. Leave empty and forms fall back to opening the
    # visitor's email app with everything pre-filled.
    # Paste your Google Apps Script web-app URL (same setup as the Marstek
    # site) to receive quote requests. Empty = form asks people to call.
    "quote_endpoint": "https://script.google.com/macros/s/AKfycbwJEOfCmpKu5Qp51tVnLZ9a4zeKm9uOq-eUFTCGnot9GYgqvMMFUbFLoHS8czgE_9gl/exec",
    # Where the "Apply now" dealer buttons go (e.g. a Google Form / Netlify form).
    "dealer_apply_url": "quote.html?topic=dealer",
    # Shows a thin "draft" bar on every page. Set False before launch.
    "draft_banner": False,
    "year": 2026,
}

# Savings calculator defaults (editable by the visitor on the page too)
CALC = {
    "meralco_rate": 15.5510,       # PHP/kWh, Nov 2026 residential, check bill
    "meralco_label": "November 2026",
    "sun_hours": 4.0,              # kWh per kWp per day after losses
    "export_rate": 6.00,           # PHP/kWh credited for exported energy (net-metering, approx.)
}

CATEGORIES = [
    {"id": "hibattery", "name": "HiBattery plug-in storage", "short": "HiBattery",
     "blurb": "Plug-and-play LFP storage from 4.02 to 16 kWh. Adds backup and stores your solar without rewiring the house.",
     "icon": "battery"},
    {"id": "hione", "name": "HiOne all-in-one systems", "short": "HiOne",
     "blurb": "Inverter, battery and 0 ms backup in one slim, stackable unit, in 8, 10 and 12 kW with 8 to 64 kWh of storage.",
     "icon": "aio"},
]

OFFICIAL = "https://www.hoymiles.com"

PRODUCTS = [
    # ------------------------------ HIBATTERY -------------------------------
    {
        "id": "hibattery-inverter", "cat": "hibattery", "name": "HiBattery Inverter", "featured": True,
        "model": "HiBattery Inverter", "tagline": "Plug-in storage with 4 kW of solar input.",
        "subtitle": "4.02 kWh plug-and-play micro storage, DC and AC coupled, expandable to 16 kWh.",
        "price": 125000, "was": None,
        "note": "Unit price. Extra battery modules sold separately.",
        "lead": "An all-rounder that takes up to four panels directly, stores the energy, and switches to backup automatically when the grid fails.",
        "about": [
            "HiBattery Inverter has four MPPTs (4 × 1,000 W) for direct solar input and up to 2,500 VA output. Stack extra modules to reach 16.08 kWh.",
            "LFP cells rated for 8,000 cycles, an IP66 casing and a 10-year warranty make it a long-term investment."
        ],
        "features": ["4.02 kWh, expandable to 16.08 kWh", "4 kW PV input (4 MPPTs)", "2,500 VA max output",
                     "Automatic backup switchover", "LFP, 8,000 cycles", "IP66", "Wi-Fi + Bluetooth, local MQTT", "10-year warranty"],
        "specs": [("Capacity", "4.02 kWh (up to 16.08 kWh)"), ("PV input", "4 × 1,000 W MPPT"),
                  ("Max output", "2,500 VA"), ("Chemistry", "LFP, 8,000 cycles"), ("Enclosure", "IP66"),
                  ("Connectivity", "Bluetooth, 2.4 GHz Wi-Fi"), ("Warranty", "10 years")],
        "install": ["Plug-and-play", "Optional smart meter for zero-export control", "Indoor or outdoor"],
        "why": [("All-in-one micro", "Solar input and storage in one."), ("Grows to 16 kWh", "Stackable."),
                ("Weatherproof", "IP66."), ("Smart", "App and local control.")],
        "addons": ["hibattery-battery"],
        "datasheet": OFFICIAL + "/hibattery-4020-x.html",
    },
    {
        "id": "hibattery-battery", "cat": "hibattery", "name": "HiBattery", "featured": True,
        "model": "HiBattery", "tagline": "Add storage to the solar you already have.",
        "subtitle": "4.02 kWh AC-coupled plug-and-play storage for existing solar systems.",
        "price": 120000, "was": None, "note": "Unit price.",
        "lead": "Already have solar? HiBattery plugs in beside it, stores the surplus you would otherwise export, and gives it back in the evening.",
        "about": ["AC coupling means your existing panels and inverter stay exactly as they are. The battery charges from surplus and discharges at night or during outages.",
                  "Same LFP cells, IP66 casing and stackable design as the HiBattery Inverter."],
        "features": ["4.02 kWh LFP", "AC-coupled retrofit", "Works with existing grid-tie solar", "Stackable", "IP66"],
        "specs": [("Capacity", "4.02 kWh"), ("Coupling", "AC"), ("Chemistry", "LFP"), ("Enclosure", "IP66")],
        "install": ["Plugs in beside your existing system", "No changes to your panels"],
        "why": [("Keep your solar", "No rewiring of panels."), ("Store surplus", "Use noon solar at night.")],
        "addons": ["hibattery-inverter"],
        "datasheet": OFFICIAL + "/hibattery-4020-ac.html",
    },

    # ------------------------------- HIONE ---------------------------------
    {
        "id": "hione-inverter", "cat": "hione", "name": "HiOne Inverter", "featured": True,
        "model": "HiOne 8 / 10 / 12 kW S G3", "tagline": "The heart of a HiOne system.",
        "subtitle": "Single-phase HiOne inverter in 8, 10 or 12 kW. Stacks with 1 to 8 HiOne Batteries (8–64 kWh) for 0 ms whole-home backup.",
        "price": 110000, "options": [("8 kW", 110000), ("10 kW", 130000), ("12 kW", 150000)], "was": None,
        "note": "Inverter price. Add at least one HiOne Battery (₱120,000 per 8 kWh). Panels and installation quoted separately.",
        "lead": "Hoymiles' flagship home system. Slim, stackable and wire-free between modules, with 0 ms whole-home backup.",
        "about": [
            "Add 8 kWh HiOne Batteries, up to eight per inverter (8–64 kWh). Each uses 314 Ah LFP cells rated for 8,000+ cycles.",
            "Up to four MPPTs and 200% DC/AC oversizing let you put more panels on the roof. Hoymiles quotes about 15 minutes of hands-on installation time."
        ],
        "features": ["8, 10 or 12 kW", "8–64 kWh modular LFP", "Up to 4 MPPTs, 200% oversizing",
                     "98.5% max efficiency", "0 ms backup with gateway", "IP66 indoor/outdoor",
                     "Wall or floor mount, 255 mm deep", "8,000+ cycles"],
        "specs": [("Power", "8, 10 or 12 kW single-phase"), ("Storage", "8–64 kWh (8 kWh packs)"),
                  ("Cells", "314 Ah LiFePO₄"), ("Max PV", "24 kW recommended"), ("Max input voltage", "600 V"),
                  ("Max efficiency", "98.5%"), ("Backup", "0 ms with gateway"), ("Enclosure", "IP66"), ("Depth", "255 mm")],
        "install": ["Wire-free stacking", "One gateway supports 2 HiOne units", "Up to 8 HiOne Batteries per inverter"],
        "why": [("Slim", "255 mm deep."), ("Modular", "Up to 64 kWh."), ("Seamless backup", "0 ms."),
                ("Fast install", "Plug-together modules.")],
        "addons": ["hione-battery"],
        "datasheet": OFFICIAL + "/hione.html",
    },
    {
        "id": "hione-battery", "cat": "hione", "name": "HiOne Battery", "featured": False,
        "model": "HiOne 8 kWh pack", "tagline": "Add capacity any time.",
        "subtitle": "Stackable 8 kWh LFP pack for HiOne systems, up to eight packs per inverter.",
        "price": 120000, "was": None, "note": "Price for one 8 kWh pack.",
        "lead": "Expand an existing HiOne in minutes. Packs click onto the stack with no extra wiring.",
        "about": ["Each pack uses 314 Ah LiFePO₄ cells rated for 8,000+ cycles."],
        "features": ["8 kWh per pack", "314 Ah LFP cells", "8,000+ cycles", "Wire-free stacking", "IP66"],
        "specs": [("Capacity", "8 kWh"), ("Cells", "314 Ah LiFePO₄"), ("Max per inverter", "8 packs (64 kWh)"), ("Enclosure", "IP66")],
        "install": ["Stacks onto an existing HiOne", "No extra wiring"],
        "why": [("Pay as you grow", "One pack at a time."), ("Quick", "Minutes to add.")],
        "addons": ["hione-inverter"],
        "datasheet": OFFICIAL + "/hione.html",
    },
]

NEWS = [
    {"date": "2026-11-19", "title": "Hoymiles helps power a remote mountain school in Pangasinan",
     "summary": "An off-grid solar system using Hoymiles equipment now supplies electricity to Kulangew Elementary School, a community that had gone without reliable power.",
     "url": "https://www.plataformamedia.com/en/2026/11/19/hoymiles-brings-solar-power-to-remote-mountain-school-in-the-philippines-to-bridge-energy-gap/"},
    {"date": "2026-11-12", "title": "Hoymiles CEO Yang Bo named to TIME100 Climate 2026",
     "summary": "TIME recognised Hoymiles' founder and CEO among the leaders driving climate action in business.",
     "url": "https://www.hoymiles.com/company-event/hoymiles-ceo-bo-yang-named-to-time100-climate-2026.html"},
    {"date": "2026-10-22", "title": "HiOne all-in-one storage launches in Canada",
     "summary": "Hoymiles introduced its HiOne residential system at ETC 2026, expanding the platform to North America.",
     "url": "https://www.hoymiles.com/product-release/hoymiles-hione-residential-energy-storage-canada-etc-2026.html"},
]

FAQ = [
    ("What is the difference between HiBattery and HiOne?",
     "HiBattery is plug-and-play storage (4.02 to 16 kWh) that adds backup and stores solar with minimal electrical work. HiOne is a full home energy system: hybrid inverter, battery and 0 ms whole-home backup in one unit, in 8, 10 and 12 kW with 8 to 64 kWh of storage."),
    ("Will my lights stay on during a brownout?",
     "Yes. HiBattery switches to backup automatically, and HiOne with its gateway switches in 0 ms, so routers, PCs and CCTV don’t restart."),
    ("Can I add a battery to my existing solar?",
     "Yes. HiBattery is AC-coupled: it plugs in beside your existing system without touching your panels or inverter."),
    ("Can I add more storage later?",
     "HiBattery Inverter stacks up to 16.08 kWh. HiOne takes up to eight 8 kWh HiOne Batteries, for 64 kWh."),
    ("Do you handle net metering with Meralco or my cooperative?",
     "We prepare the technical documents and guide you through your distribution utility’s net-metering application. Timelines depend on the DU."),
    ("How long is the warranty?",
     "Warranty is set by Hoymiles and depends on the product. HiBattery Inverter carries 10 years. We register your system and handle claims locally."),
    ("How do I monitor my system?",
     "Through the Hoymiles app on iOS and Android: daily generation, battery level, backup status and savings."),
    ("Do you install outside Metro Manila?",
     "Yes, across Luzon, Visayas and Mindanao. Ask us for the nearest installation team."),
]

# ---------------------------------------------------------------------------
# IMAGES — official Hoymiles product shots and photography. Run
# `python3 get_images.py` once (needs internet) to download them into images/;
# the build then uses the local copies automatically.
# ---------------------------------------------------------------------------
CDN = "https://w3oss.hoymiles.com/uploadfile/1/"
IMAGES = {
    "logo":              CDN + "202511/90d38bae74.svg",
    "logo-light":        CDN + "202511/831f6e4823.svg",
    # product photos: HiBattery items use the HiBattery Inverter shot, HiOne items the HiOne shot
    "hibattery-inverter": CDN + "202606/c9df205d86.png",
    "hibattery-battery":  CDN + "202606/c9df205d86.png",
    "hione-inverter":     CDN + "202510/24875e4e8d.png",
    "hione-battery":      CDN + "202510/24875e4e8d.png",
    # lifestyle photography (hoymiles.com home page)
    "photo-hione-home":    CDN + "202602/fd0ec55488.jpg",
    "photo-family-home":   CDN + "202603/a0130b2aa6.jpg",
    "photo-solar-field":   CDN + "202606/c830d03f9c.jpg",
    "photo-sol-hione":     CDN + "202610/919d2f8350.webp",
}

# Hero carousel on the home page, in order.
HERO = [
    {"id": "hione-inverter", "eyebrow": "All-in-one home energy system", "badge": "New", "photo": "photo-hione-home",
     "pillars": ["8, 10, 12 kW", "8–64 kWh modular", "0 ms backup"]},
    {"id": "hibattery-inverter", "eyebrow": "Plug-in home battery", "photo": "photo-solar-field",
     "pillars": ["4.02 kWh, to 16 kWh", "4 kW solar input", "IP66"]},
]
FEATURED = ["hibattery-inverter", "hibattery-battery", "hione-inverter", "hione-battery"]

# One-line spec shown under the name on product cards (hoymiles.com style).
SPECLINE = {
    "hibattery-inverter": "4.02 kWh | DC & AC-Coupled | Plug-and-Play",
    "hibattery-battery": "4.02 kWh | AC-Coupled | Plug-and-Play",
    "hione-inverter": "8 / 10 / 12 kW | 8–64 kWh | Single Phase",
    "hione-battery": "8 kWh | LFP | Stackable",
}

# Savings calculator + home quick estimate: HiOne set-ups it can recommend
# (equipment price = inverter + battery packs; panels and installation are quoted separately).
# kwp is the panel array a set-up like this is typically paired with.
SYSTEMS = [
    {"slug": "hione-inverter", "name": "HiOne 8 kW + 1 HiOne Battery (8 kWh)",   "price": 110000 + 120000,     "kwp": 8,  "kwh": 8},
    {"slug": "hione-inverter", "name": "HiOne 10 kW + 2 HiOne Batteries (16 kWh)", "price": 130000 + 2 * 120000, "kwp": 10, "kwh": 16},
    {"slug": "hione-inverter", "name": "HiOne 12 kW + 3 HiOne Batteries (24 kWh)", "price": 150000 + 3 * 120000, "kwp": 12, "kwh": 24},
]
AC_BATTERY = "hibattery-battery"

# ------------------------------------------------------------------
# YOUR OWN CREDENTIALS (homepage "Why buy from us" + numbers bar).
# PLACEHOLDERS — replace every value with your real figures before launch.
SELLER = {
    # False = the "Why buy from us" section is hidden and the numbers bar shows Hoymiles facts.
    # Set True only once every figure below is real.
    "ready": False,
    "stats": [("0 ms", "HiOne backup switchover"),
              ("120+", "Homes installed in the Philippines"),
              ("10 years", "Battery warranty, serviced locally"),
              ("48 hrs", "Service response in Metro Manila")],
    "pillars": [("shield", "Authorized and accountable", "Genuine Hoymiles stock with the full manufacturer warranty, claimed and handled by us — not shipped abroad."),
                ("tool", "Licensed installers", "Our own electrical engineers survey, install and commission every system, and file your net-metering papers."),
                ("tag", "Pay in installments", "0% installments up to 12 months on major credit cards, plus bank financing for larger systems."),
                ("people", "After-sales that answers", "One local team for monitoring, maintenance and repairs, reachable by phone or Viber.")],
    "installs": [("photo-sol-hione", "HiOne 16 kWh · 6.1 kWp", "Quezon City"),
                 ("photo-family-home", "HiOne 24 kWh · 9.8 kWp", "Alabang, Muntinlupa"),
                 ("photo-hione-home", "HiOne 12 kW · 24 kWh", "Clark, Pampanga")],
    "quote": ("We haven't noticed a single brownout since the HiOne went in, and our Meralco bill dropped by more than half.",
              "Homeowner, Quezon City"),
}
