# hoymiles.ph — draft website

Design follows the calm, photography-led style of hoymiles.com: white header, full-bleed photo
banner, key-number bar, showroom product cards, photo tabs. Fonts: Inter Tight + Inter.

Features follow marstekenergy.ph: product mega-menu, prices, product pages with
quote/call/share buttons and "Complete the system", quote form that pre-ticks the product,
savings calculator, dealer program, where to buy, updates, contact.

```
site/            ← the finished website. Upload the contents of this folder.
src/data.py      ← ALL content: company details, prices, products, hero slides, news, FAQ
src/build.py     ← page templates (Marstek markup). Run it to regenerate site/
src/assets/      ← styles.css (hoymiles.com look) and site.js (Marstek features)
src/get_images.py← downloads the Hoymiles product photos into src/images/
```

## Preview
Open `site/index.html` in your browser. All photos and the logo are in `site/images/`.

## Edit and rebuild
    cd src
    python3 build.py

## Product range
Four products: HiBattery Inverter (₱125,000), HiBattery (₱120,000), HiOne Inverter
(8 / 10 / 12 kW: ₱110,000 / ₱130,000 / ₱150,000) and HiOne Battery (8 kWh, ₱120,000).
Prices as of 26 Nov 2026. Edit PRODUCTS in data.py; the calculator's HiOne set-ups are SYSTEMS.

## Design preview with a sample brand
`python3 preview_assets.py && PREVIEW=1 python3 build.py` builds ../preview/ with a
placeholder brand and drawn illustrations instead of the Hoymiles logo and photos.

## Before launch
- [x] Quote form connected (Google Apps Script web app, 26 Nov 2026).
- [ ] Optional contact details in `SITE` (data.py): phones, email, address, Facebook/Instagram/Messenger/Viber links.
      Anything left empty is hidden; customers then reach you through the form.
- [ ] `SELLER` (data.py): when you have real figures (installs, warranty, service time, payment options,
      install photos, a real customer quote) fill them in and set `"ready": True` to show the
      "Why buy from us" section. Until then the homepage shows Hoymiles facts instead.
- [ ] Dealers page: set your quarterly sales target (marked `[₱ target]`)
- [ ] Check the Meralco rate in `CALC` each month, and prices when they change.

## Connect the quote form (Google Sheet, free)
1. Create a new Google Sheet (e.g. "Hoymiles PH requests").
2. In the sheet: Extensions → Apps Script. Delete what is there and paste `quote-form/Code.gs`.
   Change `NOTIFY_EMAIL` to the inbox that should get an alert for each request. Save.
3. Deploy → New deployment → type "Web app". Execute as: Me. Who has access: Anyone. Deploy,
   allow the permissions Google asks for, and copy the Web app URL (ends in /exec).
4. Open that URL in a browser: it should say "Hoymiles PH form is running".
5. Paste the URL into `quote_endpoint` in data.py, run `python3 build.py`, and upload `site/` again.
6. Send a test from the live site's Contact page. A row appears in the "Requests" tab and you get an email.
If you edit Code.gs later: Deploy → Manage deployments → edit → Version: New version (the URL stays the same).

## Draft banner
`draft_banner` in data.py. True shows a small "Draft — not yet live" label at the bottom of every
page, handy while you test on the pages.dev address. It is off (False) for launch.

## Extras beyond the Marstek feature set
- FAQ page (hoymiles.com has one)
- All-products page with a category filter (like hoymiles.com/products)
- Floating Messenger chat button
