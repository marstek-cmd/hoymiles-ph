#!/usr/bin/env python3
"""Download the official Hoymiles product images into images/ so the site
no longer loads them from Hoymiles' CDN. Run once (needs internet), then
run build.py again.   python3 get_images.py"""
import os, urllib.request
from data import IMAGES
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, "images"), exist_ok=True)
for key, url in IMAGES.items():
    dest = os.path.join(here, "images", key + os.path.splitext(url)[1])
    if os.path.exists(dest):
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
            f.write(r.read())
        print("ok  ", key)
    except Exception as e:
        print("FAIL", key, e)
print("Done. Now run: python3 build.py")
