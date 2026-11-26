#!/usr/bin/env python3
"""Build the Hoymiles PH site into ../site/.
Look and layout follow hoymiles.com; features follow marstekenergy.ph.
Usage:  python3 build.py
"""
import json, os, shutil, html
from datetime import date
from urllib.parse import quote as q
from data import SITE, CALC, CATEGORIES, PRODUCTS, NEWS, FAQ, IMAGES, HERO, FEATURED, SPECLINE, SYSTEMS, AC_BATTERY, SELLER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "site")
# PREVIEW=1 python3 build.py  -> ../preview/ with a sample brand and drawn
# images, for sharing as a design preview (no Hoymiles logo or photos).
PREVIEW = os.environ.get("PREVIEW") == "1"
PREVIEW_IMG = os.path.join(os.path.dirname(HERE), "preview_images")
if PREVIEW:
    OUT = os.path.join(os.path.dirname(HERE), "preview")
    SITE = dict(SITE, brand="YourBrand Energy PH", company="YourBrand Energy (sample brand)",
                email="hello@yourbrand.example", url="https://yourbrand.example",
                facebook="https://www.facebook.com/", instagram="https://www.instagram.com/")
E = html.escape
CAT = {c["id"]: c for c in CATEGORIES}
PROD = {p["id"]: p for p in PRODUCTS}

CHEV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
SVG = {
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3.5h4l2 5-2.5 1.5a12 12 0 0 0 5.5 5.5l1.5-2.5 5 2v4a1.5 1.5 0 0 1-1.7 1.5A17.5 17.5 0 0 1 3.5 5.2 1.5 1.5 0 0 1 5 3.5Z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3 7 9 6 9-6"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8.5V7c0-1 .4-1.5 1.5-1.5H17V2.6h-2.4C11.9 2.6 11 4.2 11 6.4v2.1H9V12h2v9.4h3V12h2.3l.4-3.5Z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6A8.4 8.4 0 0 1 7.8 19l-4.3 1.2 1.2-4.2a8.4 8.4 0 1 1 15.8-4.4Z"/></svg>',
 "viber": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.8c4.6 0 7.4 2.5 7.4 7s-2.8 7-7.4 7h-.6l-2.6 2.6v-3.1C6 15.3 4.6 13 4.6 9.8c0-4.5 2.8-7 7.4-7Z"/><path d="M9.4 7.6c.3 1.8 2.1 3.6 3.9 3.9"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "grid": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 17.5h7M17.5 14v7"/></svg>',
 "bolt": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
 "sun": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3.5"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.2 5.2l1.6 1.6M17.2 17.2l1.6 1.6M18.8 5.2l-1.6 1.6M6.8 17.2l-1.6 1.6"/></svg>',
 "app": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M11 18.5h2"/></svg>',
 "bars": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20h18M6 20v-6M11 20V8M16 20v-9M21 20V5"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-4.5"/></svg>',
 "tool": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 7a4 4 0 1 0 3 3l4 4-3 3-4-4a4 4 0 0 1 0-6z"/></svg>',
 "people": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6M15 14.5c3 0 6 2 6 5.5"/></svg>',
 "calc": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="2.5" width="14" height="19" rx="2.5"/><path d="M8 6.5h8M8 11h2M12 11h2M16 11h0M8 14.5h2M12 14.5h2M8 18h2M12 18h4"/></svg>',
 "tag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8" r="1.3"/></svg>',
}
FEAT_ICONS = ["grid", "bolt", "shield", "sun", "app", "bars", "tool", "people", "tag"]

def peso(n): return "₱{:,.0f}".format(n)
def tel(p): return "+63" + p.replace(" ", "")[1:]
def in_cat(cid): return [p for p in PRODUCTS if p["cat"] == cid]

def img(key):
    if PREVIEW:
        for ext in (".webp", ".svg", ".png", ".jpg"):
            if os.path.exists(os.path.join(PREVIEW_IMG, key + ext)): return f"images/{key}{ext}"
        return None
    url = IMAGES.get(key)
    exts = ([os.path.splitext(url)[1]] if url else []) + [".webp", ".png", ".jpg", ".svg"]
    for ext in exts:
        if os.path.exists(os.path.join(HERE, "images", key + ext)): return f"images/{key}{ext}"
    return url

def spec_line(p):
    if p["id"] in SPECLINE: return SPECLINE[p["id"]]
    vals = [v for _, v in p["specs"] if len(v) <= 24][:3]
    return " | ".join(vals)

def price_row(p, save=False):
    if p.get("price") is None: return '<p class="price-row"><span class="price">Price on request</span></p>'
    if p.get("options") and not save: return f'<p class="price-row"><span class="price"><small class="price-from">from</small> {peso(p["price"])}</span></p>'
    if p.get("options"):
        return '<div class="price-opts">' + "".join(f'<div><span>{E(k)}</span><b>{peso(v)}</b></div>' for k, v in p["options"]) + '</div>'
    s = f'<p class="price-row"><span class="price">{peso(p["price"])}</span>'
    if p.get("was"): s += f'<span class="price--old">{peso(p["was"])}</span>'
    if save and p.get("was"): s += f'<span class="price-save">Save {peso(p["was"] - p["price"])}</span>'
    return s + "</p>"

def shot(p, cls="product__shot"):
    u = img(p["id"])
    if not u: return f'<div class="{cls} {cls}--empty">Photo coming soon</div>'
    return f'<div class="{cls}"><img src="{u}" alt="Hoymiles {E(p["name"])}" loading="lazy"></div>'

def card(p):
    pk = " product--package" if p["cat"] == "packages" else ""
    return f'''
  <article class="product{pk}" data-cat="{p["cat"]}">
    <span class="ptag">{E(CAT[p["cat"]]["short"])}</span>
    <h3><a href="{p["id"]}.html">{E(p["name"])}</a></h3>
    <p class="product__spec">{E(spec_line(p))}</p>
    <a class="product__media" href="{p["id"]}.html" tabindex="-1" aria-hidden="true">{shot(p)}</a>
    {price_row(p)}
    <div class="product__links"><a class="link" href="{p["id"]}.html">Learn More {CHEV}</a><a class="link" href="{p["id"]}.html#specs">Tech Specs {CHEV}</a><a class="link" href="quote.html?product={p["id"]}">Get a Quote {CHEV}</a></div>
  </article>'''

def crumbs(*items):
    li = ['<li><a href="index.html">Home</a></li>'] + [
        f'<li><a href="{h}">{E(t)}</a></li>' if h else f"<li>{E(t)}</li>" for h, t in items]
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(li)}</ol></nav>'

def banner(title, intro, *trail, photo=None, extra=""):
    if photo:
        return f'''
<section class="banner banner--photo">
  <div class="banner__in">
    <div><h1>{title}</h1><p class="lead">{intro}</p>{extra}
    {crumbs(*trail)}</div>
    <div class="banner__pic"><img src="{img(photo)}" alt=""></div>
  </div>
</section>'''
    return f'''
<section class="banner">
  <div class="banner__in">
    <h1>{title}</h1><p class="lead">{intro}</p>{extra}
    {crumbs(*trail)}
  </div>
</section>'''

def nextstep(title="Ready to power through the next brownout?", text="Tell us your monthly bill and what you want to keep running. We will size it and quote the whole job — same-day callback.",
             href="quote.html", label="Request a quote"):
    return f'''
<section class="nextstep" data-mark="{"YourBrand" if PREVIEW else "Hoymiles"}">
  <div class="nextstep__in">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="nextstep__go">
      <a class="btn btn--green" href="{href}">{label} {CHEV}</a>
      {f'<a class="btn" href="tel:{tel(SITE["phones"][0])}">Call {SITE["phones"][0]}</a>' if SITE["phones"] else ""}
      <a class="nextstep__arrow" href="{href}" aria-label="{label}"><svg viewBox="0 0 64 64"><path d="M14 50 50 14M22 14h28v28"/></svg></a>
    </div>
  </div>
</section>'''

# ------------------------------------------------------------------ chrome
MAIN_NAV = [("savings-calculator.html", "Savings calculator"),
            ("dealers.html", "Become a dealer"), ("about.html", "About us"), ("contact.html", "Contact")]
TOP_NAV = [("news.html", "Updates"), ("where-to-buy.html", "Where to buy"), ("faq.html", "FAQ")]

def wordmark(header=True):
    if header:
        return (f'<a class="wordmark" href="index.html">'
                f'<img class="wordmark__dark" src="{img("logo")}" alt="{E(SITE['brand'])}" width="120" height="34">'
                f'<img class="wordmark__light" src="{img("logo-light")}" alt="" aria-hidden="true" width="120" height="34">'
                f'<span class="wordmark__ph">PH</span></a>')
    return f'<a class="wordmark" href="index.html"><img src="{img("logo")}" alt="{E(SITE['brand'])}" width="134" height="38"><span class="wordmark__ph">PH</span></a>'

def header(active):
    tabs, panels = [], []
    for i, c in enumerate(CATEGORIES):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button class="mega__tab" role="tab" aria-selected="{sel}" aria-controls="panel-{c["id"]}" id="tab-{c["id"]}" type="button">{E(c["name"])}</button>')
        items = ""
        for p in in_cat(c["id"]):
            u = img(p["id"])
            th = f'<img src="{u}" alt="" loading="lazy">' if u else "<span>Photo coming soon</span>"
            pr = (("from " if p.get("options") else "") + peso(p["price"])) if p.get("price") else "Price on request"
            items += f'<a class="mega__item" href="{p["id"]}.html"><span class="mega__thumb">{th}</span><span class="mega__name">{E(p["name"])}</span><span class="mega__price">{pr}</span></a>'
        items += f'<a class="mega__item mega__item--all" href="{c["id"]}.html"><span class="mega__thumb mega__thumb--all">{ARROW}</span><span class="mega__name">All {E(c["name"].lower())}</span></a>'
        panels.append(f'<div class="mega__panel" role="tabpanel" id="panel-{c["id"]}" aria-labelledby="tab-{c["id"]}" data-active="{sel}">{items}</div>')
    main = "".join(f'<a class="nav__link" href="{h}"{" aria-current=page" if h == active else ""}>{t}</a>' for h, t in MAIN_NAV)
    top = "".join(f'<a href="{h}">{t}</a>' for h, t in TOP_NAV)
    return f'''<header class="masthead">
  <div class="masthead__inner">
    {wordmark()}
    <button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">
      <svg class="icon-bars" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      <svg class="icon-x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <div class="navwrap" id="nav">
      <div class="topbar">{top}<a class="shop" href="quote.html">Get a quote</a></div>
      <nav class="nav" aria-label="Main">
        <div class="menu" id="productMenu">
          <a class="nav__trigger" id="productTrigger" href="products.html" aria-expanded="false" aria-controls="productMega" aria-haspopup="true">Products <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></a>
          <div class="mega" id="productMega"><div class="mega__in">
            <div class="mega__tabs" role="tablist" aria-label="Product categories">{"".join(tabs)}</div>
            <div><div class="mega__bar"><a class="mega__seeall" href="products.html">All {len(PRODUCTS)} products {ARROW}</a></div>
            {"".join(panels)}</div>
          </div></div>
        </div>
        {main}
        <a class="nav__cta" href="quote.html">Get a quote</a>
      </nav>
    </div>
  </div>
</header>'''

def footer():
    cats = "".join(f'<li><a href="{c["id"]}.html">{E(c["name"])}</a></li>' for c in CATEGORIES)
    a, b = SITE["footer_tag"]
    return f'''<footer class="footer">
  <div class="footer__in">
    <div class="footer__top">
      <div>
        {wordmark(False)}
        <p class="footer__tag">{E(a)} {E(b)}</p>
        <p class="footer__seller">{"Design preview: sample brand and sample photos." if PREVIEW else E(brand_name()) + " is an authorized seller of Hoymiles products in the Philippines."}</p>
      </div>
      <div class="footer__cols">
        <div><h2>Products</h2><ul class="footer__links">{cats}</ul></div>
        <div><h2>Tools &amp; support</h2><ul class="footer__links">
          <li><a href="savings-calculator.html">Savings calculator</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="quote.html">Request a quote</a></li>
          <li><a href="where-to-buy.html">Where to buy</a></li></ul></div>
        <div><h2>Company</h2><ul class="footer__links">
          <li><a href="about.html">About us</a></li>
          <li><a href="news.html">Updates</a></li>
          <li><a href="dealers.html">Become a dealer</a></li>
          <li><a href="contact.html">Contact us</a></li>{"".join(f"<li>{l}</li>" for l in contact_links("|").split("|") if l)}</ul></div>
      </div>
    </div>
    <div class="footer__bottom">
      <span>&copy; <span id="year">{SITE["year"]}</span> {E(brand_name())}. Prices in Philippine pesos and subject to change. Hoymiles is a trademark of Hoymiles Power Electronics Inc.</span>
      <div class="social">{"".join(f'<a href="{SITE[k]}" aria-label="{n}">{SVG[s]}</a>' for k, n, s in (("facebook", "Facebook", "fb"), ("instagram", "Instagram", "ig"), ("messenger", "Messenger", "chat"), ("viber", "Viber", "viber")) if SITE[k])}</div>
    </div>
  </div>
</footer>
''' + (f'<a class="chatfab" href="{SITE["messenger"]}" aria-label="Chat with us on Messenger">{SVG["chat"]}</a>' if SITE["messenger"] else "")

def brand_name():
    return SITE["company"] or SITE["brand"]

def contact_links(sep=" · "):
    """Phone/email/chat links that are actually set."""
    out = [f'<a href="tel:{tel(p)}">{p}</a>' for p in SITE["phones"]]
    if SITE["email"]: out.append(f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>')
    return sep.join(out)

PAGES = []
def page(fn, title, desc, body, active="", head_extra="", scripts=""):
    full = f"{SITE['brand']} — Hoymiles HiOne and HiBattery home storage in the Philippines" if fn == "index.html" else f"{title} — {SITE['brand']}"
    url = SITE["url"] + "/" + ("" if fn == "index.html" else fn.replace(".html", ""))
    draft = ('<div class="draft">' + ("Design preview · sample brand" if PREVIEW else "Draft — not yet live") + '</div>') if SITE["draft_banner"] else ""
    doc = f'''<!DOCTYPE html>
<html lang="en-PH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(full)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_PH">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{img("logo")}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">{head_extra}
</head>
<body>
{header(active)}
<main id="top">{body}
</main>
{footer()}
{draft}{scripts}<script src="site.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f: f.write(doc)
    PAGES.append(fn)

# ================================================================== HOME
def build_home():
    systems = SYSTEMS

    fams = [("hione", "photo-sol-hione", "All-in-one home energy system", "HiOne",
             "Inverter, battery and whole-home backup in one slim, stackable unit — for family homes that want everything covered.",
             [("Power", "8–12 kW"), ("Storage", "8–64 kWh"), ("Backup", "0 ms")], PROD["hione-inverter"]["price"]),
            ("hibattery", "hibattery-inverter", "Plug-and-play storage", "HiBattery",
             "Stackable LFP storage that plugs in beside new or existing solar. No rewiring, automatic backup.",
             [("Storage", "4.02–16 kWh"), ("Solar input", "up to 4 kW"), ("Rating", "IP66")], PROD["hibattery-battery"]["price"])]
    fam_html = "".join(f'''
      <a href="{cat}.html">
        <div class="fam__img{" fam__img--product" if not pid.startswith("photo-") else ""}"><img src="{img(pid)}" alt="Hoymiles {name}" loading="lazy"></div>
        <div class="fam__body"><span class="fam__kicker">{kick}</span><h3>{name}</h3><p>{desc}</p>
          <dl>{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in specs)}</dl>
          <div class="fam__foot"><b><small>from</small>{peso(price)}</b><span class="link">Explore {name} {CHEV}</span></div></div>
      </a>''' for cat, pid, kick, name, desc, specs, price in fams)

    sols = [("photo-family-home", "Family homes", "Whole-home backup for the whole family", "Solar covers the day, a HiOne carries the night, and brownouts pass unnoticed.", "hione-inverter.html", "HiOne Inverter"),
            ("photo-solar-field", "Existing solar", "Store the energy you already make", "HiBattery plugs in beside your current system and keeps the midday surplus for the evening.", "hibattery-battery.html", "HiBattery"),
            ("photo-sol-hione", "Modern interiors", "Designed to live in the house", "255 mm deep, quiet and IP66 — HiOne fits a hallway, garage or utility room.", "hione-inverter.html", "HiOne Inverter"),
            ("photo-hione-home", "Bigger homes", "Room to grow", "Stack up to eight 8 kWh HiOne Batteries on one inverter — up to 64 kWh for large households.", "hione-battery.html", "HiOne Battery")]
    sol_html = "".join(f'''
    <div class="sol{" is-active" if i == 0 else ""}"><img src="{img(k)}" alt="" loading="{"eager" if i == 0 else "lazy"}">
      <div class="sol__body"><span>{tag}</span><h3>{t}</h3><p>{d}</p><a class="link" href="{h}">{lbl} {CHEV}</a></div></div>''' for i, (k, tag, t, d, h, lbl) in enumerate(sols))
    sol_tabs = "".join(f'<button class="soltab" type="button" aria-selected="{"true" if i == 0 else "false"}">{s[1]}</button>' for i, s in enumerate(sols))

    pillars = "".join(f'<article class="pillar"><div class="pillar__icon">{SVG[k]}</div><h3>{t}</h3><p>{d}</p></article>' for k, t, d in SELLER["pillars"])
    sample = '<span class="install__sample">Sample photo</span>' if PREVIEW else ""
    installs = "".join(f'<figure class="install"><img src="{img(k)}" alt="" loading="lazy">{sample}<figcaption><b>{E(t)}</b><span>{SVG["pin"]}{E(loc)}</span></figcaption></figure>' for k, t, loc in SELLER["installs"])
    stats = SELLER["stats"] if SELLER.get("ready") else [("0 ms", "HiOne backup switchover"), ("8–64 kWh", "HiOne storage per inverter"), ("190+", "Countries with Hoymiles systems"), ("Since 2012", "Hoymiles, listed in Shanghai")]
    proof = "".join(f"<div><strong>{E(a)}</strong><span>{E(b)}</span></div>" for a, b in stats)
    qt, qw = SELLER["quote"]

    why_sec = (f'''<section class="sec">
  <div class="shell">
    <div class="sec__head"><span class="eyebrow">Why buy from us</span><h2>Bought here, installed here, looked after here</h2>
      <p class="lead">{E(who)} supplies, installs and services every system itself, so there is one team to call for the life of your system.</p></div>
    <div class="pillars">{pillars}</div>
    <div class="installs">{installs}</div>
    <blockquote class="testimonial"><p>“{E(qt)}”</p><cite>{E(qw)}</cite></blockquote>
  </div>
</section>''' if SELLER.get("ready") else "")
    faq_html = "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in FAQ[:5])
    news_imgs = ["photo-solar-field", "photo-hione-home", "photo-sol-hione"]
    news = "".join(news_card(n, news_imgs[i % len(news_imgs)]) for i, n in enumerate(NEWS[:3]))
    who = SITE["brand"]

    body = f'''
<section class="hero4">
  <img src="{img("photo-hione-home")}" alt="Hoymiles HiOne installed on a home at dusk" fetchpriority="high">
  <div class="hero4__in">
    <span class="eyebrow">Hoymiles HiOne &amp; HiBattery · Philippines</span>
    <h1>Reliable power for Filipino homes.</h1>
    <p>Solar and battery storage that lowers your bill by day and keeps your home running through every brownout.</p>
    <div class="hero4__cta"><a class="btn btn--green" href="#systems">Find your system {CHEV}</a><a class="btn btn--light" href="quote.html">Request a quote</a></div>
  </div>
</section>
<div class="proof">{proof}</div>

<section class="sec" id="systems">
  <div class="shell">
    <div class="sec__head sec__head--row"><div><span class="eyebrow">Product families</span><h2>Two ways to store your solar</h2>
      <p class="lead">Start small with plug-in storage, or cover the whole house with an all-in-one system.</p></div>
      <a class="btn" href="products.html">All products {CHEV}</a></div>
    <div class="fam">{fam_html}</div>
  </div>
</section>

<section class="sec sec--soft" id="prices">
  <div class="shell">
    <div class="sec__head sec__head--row"><div><span class="eyebrow">Products &amp; prices</span><h2>Four products. Clear prices.</h2>
      <p class="lead">Unit prices in pesos. Panels and installation are quoted after a short call or site check.</p></div>
      <a class="btn" href="quote.html">Request a quote {CHEV}</a></div>
    <div class="products products--four">{"".join(card(PROD[x]) for x in FEATURED)}</div>
  </div>
</section>

<section class="soltabs4" data-tabslider aria-label="Solutions">{sol_html}
  <div class="soltabs" role="tablist">{sol_tabs}</div>
</section>

{why_sec}

<section class="sec sec--soft">
  <div class="shell">
    <div class="savings">
      <div><span class="eyebrow">Savings estimate</span><h2>See what solar could take off your bill</h2>
        <p>Enter your average monthly bill for an instant estimate, or open the full calculator to adjust every assumption.</p></div>
      <form class="quick" id="quick" onsubmit="return false">
        <label for="q-bill">Average monthly electricity bill</label>
        <div class="quick__row">
          <div class="quick__field"><span>₱</span><input id="q-bill" type="number" inputmode="numeric" min="0" step="500" value="8000" aria-label="Monthly bill in pesos"></div>
          <a class="btn btn--sun" id="q-go" href="savings-calculator.html">Full calculator {CHEV}</a>
        </div>
        <p class="quick__out" id="q-out" aria-live="polite"></p>
      </form>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell split">
    <div><span class="eyebrow">FAQ</span><h2 class="display">Common questions</h2>
      <p class="lead">More answers on the <a class="ulink" href="faq.html">FAQ page</a>, or <a class="ulink" href="contact.html">contact our team</a>.</p>
      <div class="askbox"><b>Still deciding?</b><p>Send us a photo of your electric bill and we will recommend a system — no obligation.</p>
        <a class="btn" href="quote.html?topic=question">Send us a message {CHEV}</a></div></div>
    <div class="faq">{faq_html}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="shell">
    <div class="sec__head sec__head--row"><div><span class="eyebrow">Newsroom</span><h2>Latest news</h2></div><a class="btn" href="news.html">All updates {CHEV}</a></div>
    <div class="news">{news}</div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="dealer-band">
      <div><span class="eyebrow">Sub-dealer program</span><h2>Sell and install Hoymiles in your area</h2>
      <p>Dealer pricing, product and technical training, marketing materials and local warranty support.</p></div>
      <a class="btn btn--green" href="dealers.html">Become a dealer {CHEV}</a>
    </div>
  </div>
</section>
{nextstep("Talk to a solar specialist", "Send your bill and what you want to keep running. We will recommend a system and quote it, installation included.")}'''
    js = (f'<script>window.HM_SYSTEMS={json.dumps(systems)};window.HM_RATE={CALC["meralco_rate"]};window.HM_SUN={CALC["sun_hours"]};</script>\n')
    page("index.html", "Home", "Hoymiles HiOne all-in-one systems and HiBattery plug-in storage, supplied and installed in the Philippines.", body, scripts=js)

def news_card(n, pic=None):
    d = date.fromisoformat(n["date"]).strftime("%B %d, %Y")
    im = f'<div class="post__img"><img src="{img(pic)}" alt="" loading="lazy"></div>' if pic and img(pic) else ""
    return f'''
    <article class="post">{im}<div class="post__body"><h3>{E(n["title"])}</h3><p>{E(n["summary"])}</p>
      <div class="post__foot"><time datetime="{n["date"]}">{d}</time><a class="link" href="{n["url"]}" target="_blank" rel="noopener">Read More {CHEV}</a></div></div></article>'''

# ============================================================ CATALOGUE
def build_categories():
    for c in CATEGORIES:
        body = banner(E(c["name"]), E(c["blurb"]), ("products.html", "Products"), (None, c["name"])) + f'''
<section class="sec">
  <div class="shell">
    <div class="products">{"".join(card(p) for p in in_cat(c["id"]))}
    </div>
  </div>
</section>''' + nextstep("Not sure which one?", "Tell us your monthly bill and what you want to keep running. We will size it for you and quote the whole job.")
        page(f'{c["id"]}.html', c["name"], c["blurb"], body)

def build_products():
    radios = f'<label><input type="radio" name="cat" value="all" checked><span>All Products</span><span class="count">{len(PRODUCTS)}</span></label>' + "".join(
        f'<label><input type="radio" name="cat" value="{c["id"]}"><span>{E(c["name"])}</span><span class="count">{len(in_cat(c["id"]))}</span></label>' for c in CATEGORIES)
    body = banner("All Products", f"Everything we carry — {len(PRODUCTS)} Hoymiles products. Prices are per unit; panels, delivery and installation are quoted after a short call.",
                  (None, "Products")) + f'''
<section class="sec sec--soft">
  <div class="shell catalog">
    <aside class="filter"><h2>Filter by product category</h2><form id="catFilter">{radios}</form></aside>
    <div class="products" id="catalogGrid">{"".join(card(p) for p in PRODUCTS)}
    </div>
  </div>
</section>'''
    page("products.html", "All products", "Every Hoymiles product we supply in the Philippines.", body)

def build_product(p):
    c = CAT[p["cat"]]
    url = f'{SITE["url"]}/{p["id"]}'
    share_txt = q(f'{p["name"]} - {SITE["brand"]} {url}')
    about = "".join(f"<p>{E(x)}</p>" for x in p["about"][:1])
    more = "".join(f"<p>{E(x)}</p>" for x in p["about"])
    feats = "".join(f'<div class="feat">{SVG[FEAT_ICONS[i % len(FEAT_ICONS)]]}<div><p>{E(x)}</p></div></div>' for i, x in enumerate(p["features"]))
    specs = "".join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in p["specs"])
    inst = "".join(f"<li>{E(x)}</li>" for x in p["install"])
    whys = "".join(f'<div class="feat">{SVG[FEAT_ICONS[(i + 3) % len(FEAT_ICONS)]]}<div><h3>{E(a)}</h3><p>{E(b)}</p></div></div>' for i, (a, b) in enumerate(p["why"]))
    sheet = (f'<a class="ulink" href="{p["datasheet"]}" target="_blank" rel="noopener">Download Spec Sheet</a>' if p.get("datasheet") else "")
    addons = [PROD[a] for a in p.get("addons", []) if a in PROD]
    related = [x for x in in_cat(p["cat"]) if x["id"] != p["id"]][:4]
    u = img(p["id"])
    pic = f'<img src="{u}" alt="Hoymiles {E(p["name"])}">' if u else '<span class="muted">Photo coming soon</span>'
    addon_html = f'''
<section class="sec sec--soft" id="system">
  <div class="shell"><div class="sec__head center"><h2>Complete the System</h2><p class="lead">The parts most people add to the {E(p["name"])}.</p></div>
  <div class="products products--four">{"".join(card(a) for a in addons)}</div></div>
</section>''' if addons else ""
    rel_html = f'''
<section class="sec">
  <div class="shell"><div class="sec__head center"><h2>Related Products</h2></div>
  <div class="products products--four">{"".join(card(a) for a in related)}</div></div>
</section>''' if related else ""
    body = f'''
<section class="pdp-hero">
  <div class="pdp-hero__in">
    <div>
      <h1>{E(p["name"])}</h1>
      <p class="pdp-hero__tag">{E(p["tagline"])}</p>
      <div class="pdp-hero__desc"><p>{E(p["subtitle"])}</p>{about}</div>
      {price_row(p, save=True)}
      <p class="pdp__note">{E(p["note"])}</p>
      <div class="pdp__actions">
        <a class="btn btn--green" href="quote.html?product={p["id"]}">Request a quote {CHEV}</a>
        {f'<a class="btn" href="tel:{tel(SITE["phones"][0])}">Call {SITE["phones"][0]} {CHEV}</a>' if SITE["phones"] else f'<a class="btn" href="quote.html?topic=question">Ask a question {CHEV}</a>'}
        {sheet}
      </div>
      <div class="share"><span>Share</span>
        <a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" rel="noopener" aria-label="Share on Facebook">{SVG["fb"]}</a>
        <a href="https://wa.me/?text={share_txt}" target="_blank" rel="noopener" aria-label="Share on WhatsApp">{SVG["wa"]}</a>
        <a href="viber://forward?text={share_txt}" aria-label="Share on Viber">{SVG["viber"]}</a>
        <button type="button" class="share__copy" data-copy="{url}">Copy link</button>
      </div>
    </div>
    <div class="pdp-hero__img">{pic}</div>
  </div>
  <div class="shell" style="position:relative;z-index:1;padding-bottom:1.2rem">{crumbs(("products.html", "Products"), (c["id"] + ".html", c["name"]), (None, p["name"]))}</div>
</section>
<div class="subnav"><div class="shell subnav__in"><a href="#features">Features</a><a href="#specs">Tech Specs</a><a href="#why">Why this one</a>{'<a href="#system">Complete the System</a>' if addons else ""}<a href="quote.html?product={p["id"]}">Get a Quote</a></div></div>
<section class="sec" id="features">
  <div class="shell">
    <div class="sec__head center"><h2>Features</h2></div>
    <div class="feats">{feats}</div>
    <div class="cols2" style="margin-top:3rem">
      <div class="prose"><h3 class="h3">About the {E(p["name"])}</h3>{more}</div>
      <div><h3 class="h3">Installation &amp; connectivity</h3><ul class="ticks">{inst}</ul></div>
    </div>
  </div>
</section>
<section class="specs-sec" id="specs">
  <div class="shell">
    <div class="sec__head center"><h2>Tech Specs</h2></div>
    <div class="specs-panel">
      <div class="specs-panel__img">{pic}</div>
      <div>
        <table class="spectable"><tbody><tr><th scope="row">Model</th><td>{E(p["model"])}</td></tr>{specs}</tbody></table>
        <p class="sheet">{f'<a href="{p["datasheet"]}" target="_blank" rel="noopener">Full datasheet on hoymiles.com</a> · ' if p.get("datasheet") else ""}Specifications summarised from Hoymiles’ published data.</p>
      </div>
    </div>
  </div>
</section>
<section class="sec" id="why">
  <div class="shell"><div class="sec__head center"><h2>Why the {E(p["name"])}</h2></div><div class="feats">{whys}</div></div>
</section>{addon_html}{rel_html}
{nextstep()}'''
    ld = {"@context": "https://schema.org", "@type": "Product", "name": "Hoymiles " + p["name"], "brand": {"@type": "Brand", "name": "Hoymiles"},
          "model": p["model"], "description": p["subtitle"]}
    if u: ld["image"] = u
    if p.get("price"):
        ld["offers"] = {"@type": "Offer", "priceCurrency": "PHP", "price": p["price"], "availability": "https://schema.org/InStock",
                        "seller": {"@type": "Organization", "name": brand_name()}}
    page(f'{p["id"]}.html', p["name"], p["subtitle"], body, head_extra=f'\n<script type="application/ld+json">{json.dumps(ld)}</script>')

# ============================================================ CALCULATORS
def build_savings():
    c = CALC
    systems = SYSTEMS
    ac = PROD[AC_BATTERY]
    js = (f'<script>window.HM_SYSTEMS={json.dumps(systems)};'
          f'window.HM_ACBATT={json.dumps({"slug": ac["id"], "name": ac["name"], "price": ac["price"], "kwh": 4.02})};</script>\n')
    body = banner("What could solar take off your bill?",
                  "Enter your average monthly bill. Everything is worked out in your browser — nothing is uploaded, nothing is sent to us, and every assumption is shown and editable.",
                  (None, "Savings calculator")) + f'''
<section class="sec sec--soft">
<div class="shell calc">
<form class="calc__form" id="calcForm" novalidate>
<div class="field">
<label for="c-bill">Average monthly bill</label>
<span class="hint">Use the 12-month average printed on your bill, not a single month.</span>
<div class="inputwrap"><span class="inputwrap__pre">₱</span><input id="c-bill" type="number" inputmode="numeric" min="0" step="100" value="14000"></div>
</div>
<div class="field">
<label for="c-utility">Your electricity provider</label>
<span class="hint">Rates differ across the country and change every month.</span>
<select id="c-utility">
<option value="{c["meralco_rate"]}">Meralco — ₱{c["meralco_rate"]:.2f} per kWh ({c["meralco_label"]})</option>
<option value="custom">Other provider — I will enter my rate</option>
</select>
</div>
<div class="field" id="c-raterow" hidden>
<label for="c-rate">Your rate per kWh</label>
<span class="hint">Divide the total on your bill by the kWh used.</span>
<div class="inputwrap"><span class="inputwrap__pre">₱</span><input id="c-rate" type="number" inputmode="decimal" min="1" step="0.01" value="{c["meralco_rate"]:.2f}"></div>
</div>
<div class="field">
<label for="c-setup">What you have now</label>
<select id="c-setup">
<option value="none">No solar, no battery</option>
<option value="solar">Solar panels, no battery</option>
<option value="both">Solar panels and a battery</option>
<option value="battery">A battery, no solar</option>
</select>
</div>
<div class="field" id="c-kwprow" hidden>
<label for="c-kwp">Size of your array</label>
<span class="hint">In kilowatts-peak. Not sure? Count the panels and multiply by 0.6.</span>
<div class="inputwrap"><input id="c-kwp" type="number" inputmode="decimal" min="0" step="0.5" value="5"><span class="inputwrap__post">kWp</span></div>
</div>
<div class="field" id="c-batrow" hidden>
<label for="c-bat">Battery you already have</label>
<span class="hint">Total usable capacity in kWh.</span>
<div class="inputwrap"><input id="c-bat" type="number" inputmode="decimal" min="0" step="0.5" value="5"><span class="inputwrap__post">kWh</span></div>
</div>
<details class="calc__assume">
<summary>Assumptions used</summary>
<div class="field">
<label for="c-sun">Usable sun hours per day</label>
<span class="hint">Energy yield per kWp after losses. 4.0 is a reasonable Philippine average.</span>
<div class="inputwrap"><input id="c-sun" type="number" inputmode="decimal" min="1" max="7" step="0.1" value="{c["sun_hours"]}"><span class="inputwrap__post">kWh/kWp/day</span></div>
</div>
<p class="calc__source">The Meralco figure of ₱{c["meralco_rate"]:.4f}/kWh is the {c["meralco_label"]} residential rate. It changes monthly — for anything you are deciding on, use the rate on your latest bill.</p>
</details>
</form>
<div class="calc__out" id="calcOut" aria-live="polite">
<div class="calc__topline">
<div><span class="calc__label">You use about</span><strong class="calc__big" id="o-kwh">—</strong><span class="calc__unit">kWh a month</span></div>
<div><span class="calc__label">Estimated saving</span><strong class="calc__big" id="o-save">—</strong><span class="calc__unit">per month</span></div>
<div><span class="calc__label">Pays for itself in</span><strong class="calc__big" id="o-payback">—</strong><span class="calc__unit" id="o-payunit">years</span></div>
</div>
<div class="calc__rec" id="o-rec"></div>
<div class="calc__working">
<h2 class="h3">How this was worked out</h2>
<ol class="working" id="o-working"></ol>
<p class="calc__caveat" id="o-caveat"></p>
</div>
</div>
</div>
</section>''' + nextstep("An estimate is not a quote", "A real quote needs your roof, your usage pattern and your switchboard. Send your details and we will do it properly.")
    page("savings-calculator.html", "Savings calculator", "Estimate what Hoymiles solar and storage could take off your electricity bill.", body, "savings-calculator.html", scripts=js)

# ================================================================= QUOTE
def build_quote():
    groups = ""
    for c in CATEGORIES:
        boxes = "".join(f'''
<label class="check"><input type="checkbox" name="products" value="{E(p["name"])}" data-slug="{p["id"]}"><span>{E(p["name"])} <em>{("from " if p.get("options") else "") + peso(p["price"]) if p.get("price") else "on request"}</em></span></label>''' for p in in_cat(c["id"]))
        groups += f'<div class="check-group"><p class="check-group__title">{E(c["name"])}</p>{boxes}</div>'
    alt = contact_links()
    body = banner("Tell us what you need",
                  "Fill this in and someone from our team will call you the same day with a full quote, including installation in your area. No cold calls — we only ring the people who ask us to.",
                  (None, "Request a quote")) + f'''
<section class="sec">
<div class="shell">
<ol class="steps">
<li><h2>Send your details</h2><p>Tell us what you are looking at and where you are. Takes a minute.</p></li>
<li><h2>We call you back</h2><p>We confirm the right system, the total with installation, and the lead time.</p></li>
<li><h2>Pay</h2><p>GCash, bank transfer, or partner financing where available.</p></li>
<li><h2>Installation</h2><p>We install, commission and connect your system to the Hoymiles app.</p></li>
</ol>
<form class="quote formcard" id="quoteForm" novalidate style="margin-top:2rem">
<p class="field field--wide" style="margin-bottom:1.2rem"><label for="f-topic">What can we help with? *</label>
<select id="f-topic" name="topic"><option value="Quote">A quote for my home</option><option value="Question">A question</option><option value="Dealer application">Becoming a sub-dealer</option></select></p>
<div class="quote__grid">
<p class="field"><label for="f-name">Full name *</label><input id="f-name" name="name" type="text" autocomplete="name" required></p>
<p class="field"><label for="f-phone">Contact number *</label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="09XX XXX XXXX" required></p>
<p class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></p>
<p class="field"><label for="f-city">City or municipality *</label><input id="f-city" name="city" type="text" autocomplete="address-level2" required></p>
<p class="field field--wide"><label for="f-address">Installation address</label><input id="f-address" name="address" type="text" autocomplete="street-address" placeholder="House number, street, barangay"></p>
</div>
<fieldset class="fieldset" id="f-products"><legend>Products you are interested in <span class="req-q">*</span></legend><div class="checks">{groups}</div></fieldset>
<fieldset class="fieldset"><legend>Your current solar setup</legend>
<div class="radios">
<label class="check"><input type="radio" name="solar" value="None" checked><span>No solar yet</span></label>
<label class="check"><input type="radio" name="solar" value="Panels, no battery"><span>Panels, no battery</span></label>
<label class="check"><input type="radio" name="solar" value="Panels and inverter"><span>Panels and inverter</span></label>
<label class="check"><input type="radio" name="solar" value="Existing battery system"><span>Existing battery system</span></label>
<label class="check"><input type="radio" name="solar" value="Not sure"><span>Not sure</span></label>
</div></fieldset>
<p class="field" style="margin-top:1.4rem"><label for="f-notes">Message / anything else? <span class="hint">Monthly bill, what to keep running in an outage, roof space, single- or three-phase.</span></label>
<textarea id="f-notes" name="notes" rows="3"></textarea></p>
<p class="hp" aria-hidden="true"><label for="f-website">Leave this empty</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></p>
<div class="quote__foot">
<button class="btn btn--green" type="submit" id="quoteSubmit">Send my request {CHEV}</button>
{f'<span class="quote__alt">or contact us: {alt}</span>' if alt else ""}
</div>
<p class="privacy">We use your details only to prepare your quote and contact you about it. We do not share them with anyone else.</p>
<p class="quote__status" id="quoteStatus" role="status" aria-live="polite"></p>
</form>
</div>
</section>'''
    page("quote.html", "Request a quote", "Request a quote for Hoymiles HiOne and HiBattery systems in the Philippines.", body)

# =========================================================== COMPANY PAGES
def build_about():
    body = banner("Smart energy for Filipino homes and businesses", "We supply, install and support Hoymiles solar and storage systems across the Philippines.",
                  (None, "About us"), photo="photo-solar-field") + f'''
<section class="sec">
<div class="shell split">
<div class="prose">
<h2 class="display" style="margin-bottom:1.2rem">Who we are</h2>
<!-- EDIT: your story. -->
<p>{E(brand_name())} {"is a sample brand used for this design preview." if PREVIEW else "is an authorized seller of Hoymiles products in the Philippines."} We bring in the equipment, design and install the system, and stay reachable after the sale — which matters more than the spec sheet when a system is going onto your roof.</p>
<p>Hoymiles was founded in 2012 and makes solar and storage technology installed in more than 190 countries and regions. We focus on two of its home ranges: HiBattery plug-in storage and the HiOne all-in-one system.</p>
<p>Brownouts are routine here and electricity rates are among the highest in the region. Solar answers the bill; storage answers the outage. Send your details through the quote form and one of our team will call you the same day.</p>
</div>
<dl class="facts">
<div class="fact"><dt>2012</dt><dd>Year Hoymiles was founded</dd></div>
<div class="fact"><dt>190+</dt><dd>Countries and regions with Hoymiles installations</dd></div>
<div class="fact"><dt>3</dt><dd>Island groups we deliver to and install in</dd></div>
</dl>
</div>
</section>''' + nextstep("Talk to us", "Same-day callback, nationwide delivery, and installation arranged where it is needed.")
    page("about.html", "About us", f"{SITE['company']} supplies, installs and supports Hoymiles HiOne and HiBattery systems in the Philippines.", body)

def build_dealers():
    perks = [("tag", "Official dealer pricing", "Buy at dealer rates, so there is a margin on every system you sell."),
             ("bolt", "Exclusive dealer discounts", "Promotions run for dealers that are not offered to the public."),
             ("grid", "Product knowledge training", "Learn the range properly: HiBattery, HiOne and how to size them."),
             ("bars", "Design and sales training", "Size a system from a bill and take a customer from enquiry to order."),
             ("tool", "Technical support", "Our team backs you on design, commissioning and after-sales concerns."),
             ("app", "Marketing materials", "Official Hoymiles photography and promotional material to sell with."),
             ("people", "Lead generation support", "Enquiries from your area passed on to you, when available."),
             ("shield", "Priority access to new products", "Stock and information on new units before they reach the public.")]
    cards = "".join(f'<div class="feat">{SVG[i]}<div><h3>{a}</h3><p>{b}</p></div></div>' for i, a, b in perks)
    apply = SITE["dealer_apply_url"]
    body = banner("Become an official sub-dealer",
                  "Sell Hoymiles solar and storage in your area, with dealer pricing, training and our team behind you. For solar installers, electrical contractors, business owners and sales professionals.",
                  (None, "Become a dealer"), photo="photo-hione-home",
                  extra=f'<p style="margin-top:1.6rem"><a class="btn btn--green" href="{apply}">Apply now {CHEV}</a></p>') + f'''
<section class="sec">
<div class="shell">
<div class="sec__head center"><h2>Benefits for qualified sub-dealers</h2></div>
<div class="feats feats--4">{cards}</div>
</div>
</section>
<section class="sec sec--soft">
<div class="shell split">
<div class="prose">
<h2 class="display" style="margin-bottom:1.2rem">What we expect</h2>
<p>As an official sub-dealer you promote and actively sell Hoymiles products, protect the brand’s reputation, and attend the product, technical and sales training we run. You follow official pricing, marketing and branding policies, look after your customers, and coordinate after-sales concerns with us.</p>
<p>To keep an active accreditation, sub-dealers need to meet a minimum sales target each quarter. Falling short may lead to a review of the accreditation.</p>
</div>
<dl class="facts">
<!-- EDIT: set your own quarterly target -->
<div class="fact"><dt>[₱ target]</dt><dd>Minimum accumulated sales per quarter</dd></div>
<div class="fact"><dt>3–5 min</dt><dd>To complete the application</dd></div>
<div class="fact"><dt>1 ID</dt><dd>Government-issued, JPG, PNG or PDF</dd></div>
</dl>
</div>
</section>
<section class="sec">
<div class="shell">
<div class="sec__head center"><h2>From application to accreditation</h2></div>
<ol class="steps">
<li><h3>Have your ID ready</h3><p>You will upload one government-issued ID with the form.</p></li>
<li><h3>Fill in the application</h3><p>Your details, business background, target area and experience.</p></li>
<li><h3>We review it</h3><p>Our dealer team reviews every application and contacts qualified applicants.</p></li>
<li><h3>Training and onboarding</h3><p>Approved dealers get pricing, training and materials before they start selling.</p></li>
</ol>
<p class="center" style="margin-top:2rem"><a class="btn btn--green" href="{apply}">Apply as a sub-dealer {CHEV}</a></p>
<p class="center" style="margin-top:1rem;font-size:.85rem;color:var(--muted)">Submitting an application does not guarantee approval. Questions first? <a class="ulink" href="quote.html?topic=question">Send us a message</a>.</p>
</div>
</section>'''
    page("dealers.html", "Become a dealer", "Become an official Hoymiles sub-dealer in the Philippines.", body)

def build_where():
    body = banner("Where to Buy", "We sell and install direct across the Philippines. You talk to us directly — we quote, then we deliver and install.", (None, "Where to buy")) + f'''
<section class="sec">
<div class="shell split">
<div class="prose">
<h2 class="display" style="margin-bottom:1.2rem">Direct, nationwide</h2>
<p>Orders are placed by phone or through the quote form. We confirm the right system for your household, quote the total including installation at your address, and handle commissioning and app setup.</p>
<p>Payment is by GCash, bank transfer, or partner financing where available. Nothing is charged before you have seen the full quote.</p>
<h2 class="display" style="margin:2rem 0 1rem">Want to sell Hoymiles?</h2>
<p>We are appointing official sub-dealers across the country. <a class="ulink" href="dealers.html">See the program and apply</a>.</p>
</div>
<dl class="facts">
<div class="fact"><dt>Luzon</dt><dd>Delivery and installation</dd></div>
<div class="fact"><dt>Visayas</dt><dd>Delivery and installation</dd></div>
<div class="fact"><dt>Mindanao</dt><dd>Delivery and installation</dd></div>
</dl>
</div>
</section>''' + nextstep("Ready to order?", "Tell us your city and what you are looking at. We will quote installation with it.")
    page("where-to-buy.html", "Where to buy", "Buy Hoymiles solar and storage in the Philippines.", body, "where-to-buy.html")

def build_news():
    pics = ["photo-family-home", "photo-hione-home", "photo-sol-hione", "photo-solar-field"]
    posts = "".join(news_card(n, pics[i % len(pics)]) for i, n in enumerate(NEWS))
    body = banner("Newsroom", f"The latest promos, new arrivals and news from Hoymiles and {E(SITE['brand'])}.", (None, "Updates")) + f'''
<section class="sec">
<div class="shell">
<!-- EDIT: add an item to NEWS in data.py per update. Newest first. -->
<div class="news">{posts}</div>
<p style="margin-top:1.6rem;font-size:.88rem;color:var(--muted)">Want to hear about promos and new arrivals first? Mention it when you <a class="ulink" href="quote.html">request a quote</a> and we’ll keep you posted.</p>
</div>
</section>'''
    page("news.html", "Updates", "Hoymiles news and Hoymiles PH updates.", body)

def build_contact():
    cards = []
    if SITE["phones"]: cards.append(f'<article class="contact__card">{SVG["phone"]}<h2>Phone</h2><p>{"<br>".join(f"<a href=tel:{tel(p)}>{p}</a>" for p in SITE["phones"])}</p></article>')
    if SITE["email"]: cards.append(f'<article class="contact__card">{SVG["mail"]}<h2>Email</h2><p><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p></article>')
    chat = " · ".join(f'<a href="{SITE[k]}">{n}</a>' for k, n in (("messenger", "Messenger"), ("viber", "Viber")) if SITE[k])
    if chat: cards.append(f'<article class="contact__card">{SVG["chat"]}<h2>Messenger &amp; Viber</h2><p>{chat}</p></article>')
    soc = " · ".join(f'<a href="{SITE[k]}">{n}</a>' for k, n in (("facebook", "Facebook"), ("instagram", "Instagram")) if SITE[k])
    if soc: cards.append(f'<article class="contact__card">{SVG["fb"]}<h2>Social</h2><p>{soc}</p></article>')
    if SITE["address"]: cards.append(f'<article class="contact__card" style="grid-column:1/-1">{SVG["pin"]}<h2>Showroom</h2><p>{E(SITE["address"])}<br>{E(SITE["hours"])}</p></article>')
    msg = f'''<article class="contact__card" style="grid-column:1/-1">{SVG["mail"]}<h2>Send us a message</h2>
<p>Questions, quotes and dealer enquiries all go through one short form. We reply the same day, {E(SITE["hours"])}.</p>
<p style="margin-top:1rem;display:flex;gap:.6rem;flex-wrap:wrap"><a class="btn btn--green" href="quote.html?topic=question">Send a message {CHEV}</a><a class="btn" href="quote.html">Request a quote</a></p></article>'''
    body = banner("Contact Us", "Send us a message or a quote request and our team will get back to you the same day.", (None, "Contact")) + f'''
<section class="sec">
<div class="shell split">
<div class="contact__cards">{msg}{"".join(cards)}</div>
<div>
<h2 class="h3">Helpful to include</h2>
<ul class="ticks">
<li><strong>Your average monthly bill.</strong> The 12-month average printed on it, not one month.</li>
<li><strong>What you want kept running</strong> during an outage.</li>
<li><strong>Whether you already have solar,</strong> and roughly what size.</li>
<li><strong>Single- or three-phase supply,</strong> if you know it.</li>
<li><strong>Your city or municipality,</strong> so we can quote installation.</li>
</ul>
</div>
</div>
</section>'''
    page("contact.html", "Contact", "Contact Hoymiles PH for a quote, a question or a dealer enquiry.", body, "contact.html")

def build_faq():
    items = "".join(f"\n<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in FAQ]}
    body = banner("FAQ", "Microinverters, brownout backup, net metering and warranty — the questions we get most.", (None, "FAQ")) + f'''
<section class="sec"><div class="shell"><div class="faq">{items}</div></div></section>''' + nextstep("Still have a question?", "Send us a message and we will get back to you the same day.", "quote.html?topic=question", "Send a message")
    page("faq.html", "FAQ", "Answers about Hoymiles HiOne and HiBattery, brownout backup and net metering in the Philippines.", body, "faq.html",
         head_extra=f'\n<script type="application/ld+json">{json.dumps(ld)}</script>')

def build_404():
    body = banner("Page not found", 'That page has moved or never existed. Try <a class="ulink" href="products.html">all products</a> or <a class="ulink" href="index.html">the home page</a>.', (None, "Not found"))
    page("404.html", "Page not found", "Page not found.", body)

# =================================================================== main
def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copy(os.path.join(HERE, "assets", "styles.css"), OUT)
    js = open(os.path.join(HERE, "assets", "site.js"), encoding="utf-8").read()
    js = js.replace("__ENDPOINT__", SITE.get("quote_endpoint", "") or "__ENDPOINT__").replace("__PHONE__", SITE["phones"][0] if SITE["phones"] else "")
    open(os.path.join(OUT, "site.js"), "w", encoding="utf-8").write(js)
    src_img = PREVIEW_IMG if PREVIEW else os.path.join(HERE, "images")
    if os.path.isdir(src_img) and os.listdir(src_img):
        shutil.copytree(src_img, os.path.join(OUT, "images"))
    build_home(); build_products(); build_categories()
    for p in PRODUCTS: build_product(p)
    build_savings(); build_quote()
    build_about(); build_dealers(); build_where(); build_news(); build_contact(); build_faq(); build_404()
    today = date.today().isoformat()
    sm = "".join(f"<url><loc>{SITE['url']}/{'' if p == 'index.html' else p.replace('.html', '')}</loc><lastmod>{today}</lastmod></url>"
                 for p in PAGES if p != "404.html")
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f"Built {len(PAGES)} pages into {OUT}")

if __name__ == "__main__":
    main()
