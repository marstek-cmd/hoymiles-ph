#!/usr/bin/env python3
"""Draws stand-in SVG images for the shareable design preview (artifacts cannot
load remote photos). Writes ../preview_images/<key>.svg for every IMAGES key."""
import os
from data import IMAGES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "preview_images")
os.makedirs(OUT, exist_ok=True)

def svg(w, h, body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{defs}</defs>{body}</svg>'

GREY = '<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#8d939c"/><stop offset=".5" stop-color="#b9bec6"/><stop offset="1" stop-color="#7d838c"/></linearGradient>'
DARK = '<linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="#16181d"/><stop offset=".5" stop-color="#2c3038"/><stop offset="1" stop-color="#121418"/></linearGradient>'
WHITE = '<linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="#dfe2e8"/><stop offset=".5" stop-color="#fbfbfd"/><stop offset="1" stop-color="#d6d9e0"/></linearGradient>'
SH = '<radialGradient id="s"><stop offset="0" stop-color="#000" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
DEFS = GREY + DARK + WHITE + SH

def tower(mods=3, top="d"):
    x, w, y = 190, 220, 70
    b = f'<ellipse cx="300" cy="545" rx="150" ry="16" fill="url(#s)"/>'
    b += f'<rect x="{x}" y="{y}" width="{w}" height="120" rx="10" fill="url(#{top})"/>'
    b += f'<rect x="{x+70}" y="{y+40}" width="80" height="26" rx="4" fill="#0a0b0e"/><circle cx="{x+90}" cy="{y+53}" r="4" fill="#7dd96a"/><circle cx="{x+110}" cy="{y+53}" r="4" fill="#5fb3ff"/><circle cx="{x+130}" cy="{y+53}" r="4" fill="#5fb3ff"/>'
    hgt = (470 - 125) // mods
    for i in range(mods):
        yy = y + 125 + i * hgt
        b += f'<rect x="{x}" y="{yy}" width="{w}" height="{hgt-5}" rx="8" fill="url(#g)"/>'
        b += f'<rect x="{x}" y="{yy}" width="{w}" height="6" rx="3" fill="#fff" opacity=".25"/>'
    b += f'<circle cx="300" cy="{y+125+hgt//2}" r="16" fill="none" stroke="#e9ebef" stroke-width="3" opacity=".8"/>'
    return svg(600, 600, b, DEFS)

def box(wd=360, ht=230, top="d", body="g", leds=True, y0=None):
    x = 300 - wd // 2; y = y0 or (330 - ht // 2)
    b = f'<ellipse cx="300" cy="{y+ht+14}" rx="{wd//2+20}" ry="14" fill="url(#s)"/>'
    b += f'<rect x="{x}" y="{y}" width="{wd}" height="{ht}" rx="14" fill="url(#{body})"/>'
    b += f'<rect x="{x}" y="{y}" width="{wd}" height="{int(ht*.22)}" rx="12" fill="url(#{top})"/>'
    if leds:
        b += "".join(f'<rect x="{x+20+i*16}" y="{y+int(ht*.09)}" width="10" height="4" rx="2" fill="#6fd0ff"/>' for i in range(4))
    b += f'<circle cx="300" cy="{y+int(ht*.6)}" r="14" fill="none" stroke="#ffffff" stroke-width="3" opacity=".7"/>'
    return svg(600, 600, b, DEFS)

def charger():
    b = '<ellipse cx="300" cy="530" rx="120" ry="12" fill="url(#s)"/>'
    b += '<rect x="210" y="90" width="180" height="300" rx="22" fill="url(#w)"/><rect x="240" y="130" width="120" height="70" rx="8" fill="#14161b"/>'
    b += '<path d="M300 200 h0" /><rect x="285" y="250" width="30" height="60" rx="8" fill="#2a2e36"/>'
    b += '<path d="M300 310 C300 420 420 420 420 500" fill="none" stroke="#2a2e36" stroke-width="14" stroke-linecap="round"/>'
    b += '<circle cx="300" cy="350" r="9" fill="#7dd96a"/>'
    return svg(600, 600, b, DEFS)

def scene(sky1, sky2, ground, unit="tower", sun=True, people=False, car=False, field=False):
    W, H = 1600, 900
    d = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky1}"/><stop offset="1" stop-color="{sky2}"/></linearGradient>'
         f'<linearGradient id="gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ground}"/><stop offset="1" stop-color="#0c1410"/></linearGradient>'
         '<linearGradient id="pv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1c2a5a"/><stop offset="1" stop-color="#0b1330"/></linearGradient>'
         '<linearGradient id="wall" x1="0" x2="1"><stop offset="0" stop-color="#e9e4dc"/><stop offset="1" stop-color="#cfc7bb"/></linearGradient>' + DEFS)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    if sun: b += '<circle cx="1260" cy="230" r="70" fill="#ffd9a0" opacity=".9"/><circle cx="1260" cy="230" r="160" fill="#ffd9a0" opacity=".12"/>'
    b += '<path d="M0 560 Q300 500 600 545 T1200 520 T1600 540 V900 H0Z" fill="#2c3a33" opacity=".6"/>'
    b += f'<rect y="620" width="{W}" height="280" fill="url(#gr)"/>'
    if field:
        for r in range(6):
            y = 560 + r * 55; sc = 0.6 + r * 0.22
            for c in range(-2, 14):
                x = c * 140 * sc + (r % 2) * 50
                b += f'<polygon points="{x},{y} {x+120*sc},{y} {x+100*sc},{y+38*sc} {x-20*sc},{y+38*sc}" fill="url(#pv)" stroke="#3a4f9a" stroke-width="1"/>'
        return svg(W, H, b, d)
    # house
    b += '<polygon points="760,380 1080,230 1400,380" fill="#3b3430"/>'
    b += '<rect x="800" y="380" width="560" height="300" fill="url(#wall)"/>'
    for i in range(5):
        b += f'<polygon points="{850+i*95},{350-i*0} {930+i*95},{312} {1000+i*95},{346} {920+i*95},{384}" fill="url(#pv)" stroke="#5d74c6" stroke-width="1.5" transform="translate(0,{-i*0})"/>'
    b += '<rect x="1180" y="470" width="130" height="210" fill="#2a2420"/><rect x="1190" y="480" width="110" height="190" fill="#f3c27a" opacity=".85"/>'
    b += '<rect x="860" y="450" width="150" height="110" fill="#f3c27a" opacity=".75"/>'
    # unit on wall
    if unit == "tower":
        b += '<rect x="1060" y="470" width="80" height="210" rx="6" fill="url(#g)"/><rect x="1060" y="470" width="80" height="55" rx="6" fill="url(#d)"/><circle cx="1085" cy="497" r="3" fill="#7dd96a"/>'
    else:
        b += '<rect x="1040" y="560" width="120" height="90" rx="8" fill="url(#g)"/><rect x="1040" y="560" width="120" height="22" rx="8" fill="url(#d)"/>'
    if car:
        b += '<g transform="translate(250,600)"><path d="M0 70 Q20 20 110 15 L260 10 Q330 15 370 60 L400 70 Q410 100 390 110 H20 Q0 105 0 70Z" fill="#e8ebf0"/><path d="M120 22 L250 18 Q300 22 330 58 H100Z" fill="#26303d"/><circle cx="90" cy="112" r="28" fill="#15171b"/><circle cx="310" cy="112" r="28" fill="#15171b"/></g>'
    if people:
        b += '<g fill="#f2f2f2"><circle cx="420" cy="560" r="20"/><path d="M395 590 Q420 575 445 590 L460 720 H380Z"/><circle cx="560" cy="640" r="14"/><path d="M542 662 Q560 652 578 662 L585 740 H535Z" fill="#e05a4a"/></g>'
    return svg(W, H, b, d)

def logo(light=False):
    ink = "#ffffff" if light else "#0b1a4a"
    b = (f'<circle cx="20" cy="20" r="15" fill="none" stroke="#6cc04a" stroke-width="4"/>'
         f'<path d="M12 22 Q20 6 28 22" fill="none" stroke="{ink}" stroke-width="3.5" stroke-linecap="round"/>'
         f'<text x="44" y="28" font-family="Work Sans,Arial,sans-serif" font-weight="700" font-size="22" fill="{ink}">YourBrand</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 156 40" width="156" height="40">{b}</svg>'

ART = {
    "logo": logo(), "logo-light": logo(True),
    "hione-3-12-s": tower(3), "hione-8-20-t": tower(4), "recommended-package": tower(2), "premium-package": tower(3),
    "hione-battery-pack": box(260, 150, top="g", leds=False),
    "hibattery-4020-x": box(360, 230), "starter-package": box(360, 230),
    "hibattery-4020-ac": box(330, 260, body="g", top="d"),
    "hibattery-1920-ac": box(420, 120, top="d"),
    "hione-22vd": charger(),
    "photo-family-home": scene("#f4b57e", "#fbe3c4", "#3f6b3a", unit="tower"),
    "photo-hione-home": scene("#232a4a", "#a26a6a", "#2c3d2c", unit="tower", car=True),
    "photo-hibattery-wall": scene("#9fb6d6", "#e8eef6", "#4e7a45", unit="box"),
    "photo-sol-indoor": scene("#cfd7e6", "#f3f5fa", "#5a8450", unit="box", sun=False),
    "photo-sol-hione": scene("#1a2040", "#5a5c86", "#253526", unit="tower"),
    "photo-sol-carport": scene("#7f9ccc", "#dfe8f5", "#4a6a42", unit="tower", car=True),
    "photo-solar-field": scene("#c9d6ea", "#f2f5fb", "#6d8a68", field=True, sun=False),
    "photo-story-1": scene("#e9a36c", "#f8dcc0", "#466e3e", unit="box"),
    "photo-story-2": scene("#8fa9d0", "#e9eef7", "#507a48", field=True),
    "photo-story-3": scene("#2b3358", "#8a7a9a", "#24331f", unit="tower"),
    "photo-story-4": scene("#7aa4d8", "#e6eef9", "#5c8a4c", unit="box"),
}
for k in ART:
    if True:
        open(os.path.join(OUT, k + ".svg"), "w").write(ART[k])
print("wrote", len(os.listdir(OUT)), "images to", OUT)
