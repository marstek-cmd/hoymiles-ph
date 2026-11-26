
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var desktop = function () { return window.matchMedia('(min-width: 1100px)').matches; };

  var masthead = document.querySelector('.masthead');

  /* Header is transparent only while the page sits at the top of a dark opening section. */
  (function () {
    var main = document.querySelector('main');
    var first = main && main.firstElementChild;
    while (first && first.nodeType !== 1) first = first.nextElementSibling;
    var darkTop = !!first && (first.classList.contains('hero') || first.classList.contains('banner--photo'));
    if (!darkTop) return;
    document.body.classList.add('has-dark-top');

    var ticking = false;
    function sync() {
      var atTop = window.scrollY < 40;
      document.body.classList.toggle('hero-top', atTop && !document.body.classList.contains('nav-open'));
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(sync); }
    }, { passive: true });
    document.addEventListener('nav-toggled', sync);
    sync();
  })();
  function measureHeader() {
    if (!masthead) return;
    document.documentElement.style.setProperty('--header-h', masthead.offsetHeight + 'px');
  }
  measureHeader();
  window.addEventListener('resize', measureHeader);
  window.addEventListener('load', measureHeader);
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  function closeNav() {
    document.body.classList.remove('nav-open');
    if (burger) burger.setAttribute('aria-expanded', 'false');
    document.dispatchEvent(new Event('nav-toggled'));
    var m = document.getElementById('productMenu');
    var t = document.getElementById('productTrigger');
    if (m && !desktop()) { m.setAttribute('data-open', 'false'); }
    if (t && !desktop()) { t.setAttribute('aria-expanded', 'false'); }
  }
  window.addEventListener('resize', function () {
    if (desktop() && document.body.classList.contains('nav-open')) closeNav();
  });
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) document.body.classList.remove('hero-top');
      document.dispatchEvent(new Event('nav-toggled'));
    });
    nav.addEventListener('click', function (ev) {
      var a = ev.target.closest('a');
      if (a && !(a.id === 'productTrigger' && !desktop())) closeNav();
    });
  }

  /* Products mega menu. Hover on desktop, click everywhere. */
  var menu = document.getElementById('productMenu');
  var trigger = document.getElementById('productTrigger');
  if (menu && trigger) {
    var hoverTimer;
    function openMenu(state) {
      menu.setAttribute('data-open', state ? 'true' : 'false');
      trigger.setAttribute('aria-expanded', state ? 'true' : 'false');
    }
    trigger.addEventListener('click', function (ev) {
      if (desktop()) return;
      ev.preventDefault();
      openMenu(menu.getAttribute('data-open') !== 'true');
    });
    trigger.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') { ev.preventDefault(); openMenu(true); }
    });
    menu.addEventListener('mouseenter', function () {
      if (!desktop()) return;
      clearTimeout(hoverTimer);
      openMenu(true);
    });
    menu.addEventListener('mouseleave', function () {
      if (!desktop()) return;
      hoverTimer = setTimeout(function () { openMenu(false); }, 160);
    });
    document.addEventListener('click', function (ev) {
      if (desktop() && !menu.contains(ev.target)) openMenu(false);
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { openMenu(false); closeNav(); trigger.focus(); }
    });
    menu.addEventListener('click', function (ev) {
      if (ev.target.closest('.mega__item')) { openMenu(false); closeNav(); }
    });

    var tabs = menu.querySelectorAll('.mega__tab');
    tabs.forEach(function (tab) {
      var show = function () {
        tabs.forEach(function (t) { t.setAttribute('aria-selected', 'false'); });
        tab.setAttribute('aria-selected', 'true');
        menu.querySelectorAll('.mega__panel').forEach(function (p) {
          p.setAttribute('data-active', p.id === tab.getAttribute('aria-controls') ? 'true' : 'false');
        });
      };
      tab.addEventListener('click', function () {
        show();
        if (!desktop()) tab.scrollIntoView({ inline: 'center', block: 'nearest', behavior: reduced ? 'auto' : 'smooth' });
      });
      tab.addEventListener('mouseenter', function () { if (desktop()) show(); });
    });
  }

  /* Hero carousel */
  var slidesWrap = document.getElementById('slides');
  if (slidesWrap) {
    var slides = Array.prototype.slice.call(slidesWrap.querySelectorAll('.slide'));
    var dots = Array.prototype.slice.call(document.querySelectorAll('.dot'));
    var index = 0, timer = null, DELAY = 6000;

    function show(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        var on = n === index;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', on ? 'false' : 'true');
      });
      dots.forEach(function (d, n) {
        d.setAttribute('aria-current', n === index ? 'true' : 'false');
      });
    }
    function next() { show(index + 1); }
    function prev() { show(index - 1); }
    function start() {
      if (reduced || timer) return;
      timer = setInterval(next, DELAY);
    }
    function stop() { clearInterval(timer); timer = null; }

    dots.forEach(function (d) {
      d.addEventListener('click', function () {
        show(parseInt(d.dataset.goto, 10));
        stop(); start();
      });
    });
    var pv = document.querySelector('.hero__arrow--prev'), nx = document.querySelector('.hero__arrow--next');
    if (pv) pv.addEventListener('click', function () { prev(); stop(); start(); });
    if (nx) nx.addEventListener('click', function () { next(); stop(); start(); });

    slidesWrap.addEventListener('focusin', stop);
    slidesWrap.addEventListener('focusout', start);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stop(); } else { start(); }
    });

    var x0 = null;
    slidesWrap.addEventListener('touchstart', function (ev) { x0 = ev.touches[0].clientX; stop(); }, { passive: true });
    slidesWrap.addEventListener('touchend', function (ev) {
      if (x0 === null) return;
      var dx = ev.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) { dx < 0 ? next() : prev(); }
      x0 = null; start();
    });

    show(0);
    start();
  }

  /* Any CTA carrying data-product ticks that box in the form */
  document.querySelectorAll('[data-product]').forEach(function (link) {
    link.addEventListener('click', function () {
      var box = document.querySelector('input[name="products"][value="' + link.dataset.product + '"]');
      if (box) box.checked = true;
    });
  });

  /* ---------------------------------------------------------
     Quote form
     The endpoint comes from data.py (SITE["quote_endpoint"]).
     --------------------------------------------------------- */
  var QUOTE_ENDPOINT = 'https://script.google.com/macros/s/AKfycbwJEOfCmpKu5Qp51tVnLZ9a4zeKm9uOq-eUFTCGnot9GYgqvMMFUbFLoHS8czgE_9gl/exec';
  var PHONE = '';

  var form = document.getElementById('quoteForm');
  if (form) {
    // ?topic=dealer / ?topic=question preselects the dropdown; products are only required for quotes
    var tsel = form.elements['topic'];
    var tmap = { dealer: 'Dealer application', question: 'Question', quote: 'Quote' };
    var tq = new URLSearchParams(location.search).get('topic');
    if (tsel && tq && tmap[tq]) tsel.value = tmap[tq];
    function syncTopic() {
      var q = !tsel || tsel.value === 'Quote';
      var star = form.querySelector('.req-q'); if (star) star.hidden = !q;
    }
    if (tsel) { tsel.addEventListener('change', syncTopic); syncTopic(); }
    var statusEl = document.getElementById('quoteStatus');
    var submitEl = document.getElementById('quoteSubmit');

    function clearErrors() {
      form.querySelectorAll('.field__error').forEach(function (n) { n.remove(); });
      form.querySelectorAll('[aria-invalid]').forEach(function (n) { n.removeAttribute('aria-invalid'); });
    }
    function fail(el, msg) {
      el.setAttribute('aria-invalid', 'true');
      var p = document.createElement('p');
      p.className = 'field__error';
      p.textContent = msg;
      (el.closest('.field') || el.closest('.fieldset') || el.parentNode).appendChild(p);
    }
    function say(msg, kind) {
      statusEl.textContent = msg;
      statusEl.className = 'quote__status' + (kind ? ' is-' + kind : '');
    }

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      clearErrors();
      say('');

      var first = null;
      ['name', 'phone', 'city'].forEach(function (n) {
        var el = form.elements[n];
        if (!el.value.trim()) { fail(el, 'Please fill this in.'); first = first || el; }
      });

      var email = form.elements['email'];
      if (email.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value.trim())) {
        fail(email, 'That email address does not look right.');
        first = first || email;
      }

      var picked = form.querySelectorAll('input[name="products"]:checked');
      var topic = form.elements['topic'] ? form.elements['topic'].value : 'Quote';
      if (!picked.length && topic === 'Quote') {
        var box = form.querySelector('.checks');
        fail(box, 'Pick at least one product.');
        first = first || box;
      }

      if (first) {
        say('Please check the highlighted fields.', 'error');
        (first.focus ? first : first.querySelector('input')).focus();
        return;
      }

      if (form.elements['website'].value) { say('Thanks — we will be in touch.', 'ok'); return; }

      var data = new URLSearchParams();
      data.append('topic', topic);
      data.append('name', form.elements['name'].value.trim());
      data.append('phone', form.elements['phone'].value.trim());
      data.append('email', form.elements['email'].value.trim());
      data.append('city', form.elements['city'].value.trim());
      data.append('address', form.elements['address'].value.trim());
      data.append('solar', (form.querySelector('input[name="solar"]:checked') || {}).value || '');
      data.append('notes', form.elements['notes'].value.trim());
      data.append('products', Array.prototype.map.call(picked, function (c) { return c.value; }).join(', '));
      data.append('page', location.href);

      if (!QUOTE_ENDPOINT || QUOTE_ENDPOINT.indexOf('__') === 0) {
        say('Sorry, our form is still being set up. Please try again later' + (PHONE ? ' or call ' + PHONE : '') + '.', 'error');
        return;
      }

      submitEl.disabled = true;
      say('Sending…');

      fetch(QUOTE_ENDPOINT, { method: 'POST', body: data })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(function () {
          form.classList.add('quote--sent');
          say('Thanks — we have your message. Our team will get back to you today.', 'ok');
        })
        .catch(function () {
          submitEl.disabled = false;
          say('Sorry, that did not go through. Please try again' + (PHONE ? ' or call ' + PHONE : '') + '.', 'error');
        });
    });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();


/* Arriving at quote.html?product=his-hybrid pre-ticks that box. */
(function () {
  'use strict';
  var slug = new URLSearchParams(location.search).get('product');
  if (!slug) return;
  var box = document.querySelector('input[name="products"][data-slug="' + CSS.escape(slug) + '"]');
  if (!box) return;
  box.checked = true;
  var label = box.closest('.check');
  if (label) {
    label.classList.add('check--prefilled');
    label.scrollIntoView({ block: 'center', behavior:
      window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  }
})();

/* ---------------------------------------------------------
   Savings calculator.
   Everything is computed in the browser; nothing is uploaded.
   Conservative on purpose, and every step is printed back.
   --------------------------------------------------------- */
(function () {
  'use strict';
  var form = document.getElementById('calcForm');
  if (!form) return;

  var $ = function (id) { return document.getElementById(id); };
  var peso = function (n) { return '₱' + Math.round(n).toLocaleString('en-PH'); };
  var WEATHER = 0.85;

  // Filled in by build.py from data.py
  var SYSTEMS = window.HM_SYSTEMS || [];
  var AC_BATT = window.HM_ACBATT || { slug:'hibattery-battery', name:'HiBattery', price:120000, kwh:4.02 };

  function pickPackage(dailyKwh) {
    // the smallest package whose panels cover the daily use; fall back to the largest
    for (var i = 0; i < SYSTEMS.length; i++) {
      if (SYSTEMS[i].kwp * 4.0 * WEATHER >= dailyKwh * 0.9) return SYSTEMS[i];
    }
    return SYSTEMS[SYSTEMS.length - 1];
  }
  function recommendForSurplus(surplus) {
    var units = Math.min(4, Math.max(1, Math.ceil(surplus / (AC_BATT.kwh * 0.9))));
    return { slug: AC_BATT.slug, name: units === 1 ? AC_BATT.name : units + ' × ' + AC_BATT.name,
             price: AC_BATT.price * units, kwh: AC_BATT.kwh * units, kwp: 0, units: units };
  }

  function compute() {
    var bill  = Math.max(0, parseFloat($('c-bill').value) || 0);
    var util  = $('c-utility').value;
    var rate  = util === 'custom' ? (parseFloat($('c-rate').value) || 0) : parseFloat(util);
    var setup = $('c-setup').value;
    var kwp   = parseFloat($('c-kwp').value) || 0;
    var ownBat= parseFloat($('c-bat').value) || 0;
    var sun   = parseFloat($('c-sun').value) || 4.0;

    $('c-raterow').hidden = util !== 'custom';
    $('c-kwprow').hidden  = !(setup === 'solar' || setup === 'both');
    $('c-batrow').hidden  = setup !== 'both';

    if (!bill || !rate) return;

    var monthlyKwh = bill / rate;
    var dailyKwh   = monthlyKwh / 30;
    var steps = [], sys, saving = 0, caveat = '';

    steps.push('Your bill of ' + peso(bill) + ' at ₱' + rate.toFixed(2) +
               ' per kWh works out to about ' + Math.round(monthlyKwh).toLocaleString('en-PH') +
               ' kWh a month, or ' + dailyKwh.toFixed(1) + ' kWh a day.');

    if (setup === 'both') {
      var prodB    = kwp * sun * WEATHER;
      var surplusB = Math.max(0, prodB - dailyKwh * 0.45);
      var eveningB = dailyKwh * 0.55;
      var alreadyB = Math.min(surplusB, ownBat * 0.9, eveningB);
      var headroom = Math.max(0, Math.min(surplusB - alreadyB, eveningB - alreadyB));
      steps.push('Your ' + kwp + ' kWp array makes roughly ' + prodB.toFixed(1) +
                 ' kWh a day, and about ' + surplusB.toFixed(1) + ' kWh of that is left over after daytime use.');
      steps.push('Your existing ' + ownBat + ' kWh battery already holds about ' + alreadyB.toFixed(1) +
                 ' kWh of that surplus for the evening.');
      if (headroom < 0.5) {
        sys = recommendForSurplus(Math.max(surplusB, 1)); saving = 0;
        steps.push('That leaves under half a kWh a day unstored, so more storage would have almost nothing left to catch.');
        caveat = 'Honest answer: on these numbers more storage will not lower your bill. It buys a longer run in a brownout. ' +
                 'If you want more savings from here, more panels are the lever, not more battery.';
      } else {
        sys = recommendForSurplus(headroom);
        var addB = Math.min(headroom, sys.kwh * 0.9);
        saving = addB * rate * 30;
        steps.push('About ' + headroom.toFixed(1) + ' kWh a day is still being exported or wasted — that is what added storage could catch.');
        steps.push('Sized to that gap, ' + sys.name + ' holds a further ' + addB.toFixed(1) + ' kWh a day: ' +
                   addB.toFixed(1) + ' kWh × ₱' + rate.toFixed(2) + ' × 30 days = ' + peso(saving) + ' a month.');
        caveat = 'This is the added saving on top of what you save today, not the total. AC-coupled storage works beside most ' +
                 'existing inverters, but a site visit confirms it.';
      }
    } else if (setup === 'battery') {
      sys = SYSTEMS[0]; saving = 0;
      steps.push('You already have storage, but with no panels and a flat residential tariff there is no cheap window to charge it from.');
      steps.push('Adding panels is what turns that battery into bill savings, so the closest fit is a HiOne system paired with panels.');
      caveat = 'Honest answer: panels are the missing piece here, not more storage.';
    } else if (setup === 'solar') {
      var produced = kwp * sun * WEATHER;
      var surplus  = Math.max(0, produced - dailyKwh * 0.45);
      sys = recommendForSurplus(surplus);
      var stored = Math.min(surplus, sys.kwh * 0.9, dailyKwh * 0.55);
      saving = stored * rate * 30;
      steps.push('Your ' + kwp + ' kWp array makes roughly ' + produced.toFixed(1) + ' kWh a day — ' + sun.toFixed(1) +
                 ' kWh per kWp, less 15% for cloud cover and seasonal variation.');
      steps.push('Around 45% of a household’s use happens in daylight, so about ' + surplus.toFixed(1) + ' kWh a day is surplus.');
      steps.push('Sized to that surplus, ' + sys.name + ' can hold ' + stored.toFixed(1) + ' kWh of it for the evening.');
      steps.push('That is ' + stored.toFixed(1) + ' kWh × ₱' + rate.toFixed(2) + ' × 30 days = ' + peso(saving) + ' a month.');
      caveat = 'This assumes you currently export surplus for little or no credit. On net metering with a fair export rate, the saving is smaller.';
    } else {
      sys = pickPackage(dailyKwh);
      var prod2 = sys.kwp * sun * WEATHER;
      var day   = Math.min(prod2, dailyKwh * 0.45);
      var night = sys.kwh > 0 ? Math.min(Math.max(0, prod2 - day), sys.kwh * 0.9, dailyKwh * 0.55) : 0;
      var offset = day + night;
      saving = offset * rate * 30;
      steps.push('A ' + sys.name + ' is typically paired with about ' + sys.kwp + ' kWp of panels (quoted separately), making roughly ' + prod2.toFixed(1) +
                 ' kWh a day — ' + sun.toFixed(1) + ' kWh per kWp, less 15% for cloud cover and seasonal variation.');
      steps.push('About 45% of your use is in daylight, so ' + day.toFixed(1) + ' kWh a day comes straight off the roof.');
      if (sys.kwh > 0) {
        steps.push('Its ' + sys.kwh + ' kWh battery carries a further ' + night.toFixed(1) + ' kWh into the evening.');
      } else {
        steps.push('This set-up has no battery, so surplus is exported. We have not counted any net-metering credit.');
      }
      steps.push('That is ' + offset.toFixed(1) + ' kWh × ₱' + rate.toFixed(2) + ' × 30 days = ' + peso(saving) + ' a month.');
      caveat = 'An estimate from an average bill, not a survey: real yield depends on roof direction, shading and your usage pattern. The price shown is the HiOne equipment only; panels and installation are quoted separately, so payback is not shown.';
    }

    var capped = Math.min(saving, bill * 0.85);
    if (capped < saving) {
      steps.push('Capped at 85% of your bill: fixed charges, metering and taxes stay on it no matter how much you generate.');
      saving = capped;
    }
    var years = (saving > 0 && setup !== 'none') ? sys.price / (saving * 12) : 0;

    $('o-kwh').textContent  = Math.round(monthlyKwh).toLocaleString('en-PH');
    $('o-save').textContent = saving > 0 ? peso(saving) : '—';
    if (years > 0) { $('o-payback').textContent = years.toFixed(1); $('o-payunit').textContent = 'years'; }
    else { $('o-payback').textContent = '—'; $('o-payunit').textContent = setup === 'none' ? 'quoted with panels' : 'backup, not bill savings'; }

    $('o-rec').innerHTML =
      '<p class="calc__label">Closest fit</p>' +
      '<h2>' + sys.name + ' — ' + peso(sys.price) + (setup === 'none' || setup === 'battery' ? ' <small>equipment only</small>' : '') + '</h2>' +
      '<p>Based on ' + dailyKwh.toFixed(1) + ' kWh a day' + (setup === 'solar' ? ' and your existing array.' : '.') + '</p>' +
      '<a class="btn btn--green" href="' + sys.slug + '.html">See the ' + (sys.slug === AC_BATT.slug ? AC_BATT.name : 'HiOne Inverter') + '</a> ' +
      '<a class="btn" href="quote.html?product=' + sys.slug + '">Request a quote</a>';
    $('o-working').innerHTML = steps.map(function (s) { return '<li>' + s + '</li>'; }).join('');
    $('o-caveat').textContent = caveat;
  }

  form.addEventListener('input', compute);
  form.addEventListener('change', compute);
  compute();
})();

/* ---------------------------------------------------------
   Microinverter sizer (system-sizer.html)
   --------------------------------------------------------- */
(function () {
  'use strict';
  var form = document.getElementById('sizerForm');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };

  function size() {
    var w = parseFloat($('s-watt').value) || 0, n = parseInt($('s-count').value, 10) || 0, ph = $('s-phase').value;
    var sun = 4.0 * 0.85, rows = [], ac = 0, units = 0, steps = [];
    if (!w || !n) return;
    var dc = w * n;
    steps.push(n + ' panels × ' + w + ' W = ' + (dc / 1000).toFixed(2) + ' kWp of DC.');
    if (ph === 'three') {
      units = Math.ceil(n / 8); ac = units * 5000;
      rows.push([units + ' × MiT Series 8-in-1 (5 kW)', 'mit-8in1']);
      rows.push(['1 × DTU-Pro-S gateway', 'dtu-pro-s']);
      steps.push('Three-phase: the MiT takes eight panels per unit, so ' + units + ' unit' + (units > 1 ? 's' : '') + '.');
    } else if (w > 670) {
      units = Math.ceil(n / 4); ac = units * 2750;
      rows.push([units + ' × MiS-W Pro 2750 (4 panels each)', 'mis-w-pro']);
      rows.push(['Built-in Wi-Fi — no separate gateway', null]);
      steps.push('Panels above 670 W go on the MiS-W Pro, rated for modules up to 928 W+, four per unit.');
    } else {
      var model = w <= 540 ? 'HMS-1600-4T' : w <= 600 ? 'HMS-1800-4T' : 'HMS-2000-4T';
      var acp = w <= 540 ? 1600 : w <= 600 ? 1800 : 2000;
      var small = w <= 540 ? 800 : w <= 600 ? 900 : 1000;
      var four = Math.floor(n / 4), rem = n % 4, two = 0;
      if (rem === 3) { four += 1; } else if (rem) { two = 1; }
      units = four + two; ac = four * acp + two * small;
      if (four) rows.push([four + ' × ' + model, 'hms-2000-4t']);
      if (two) rows.push([two + ' × HMS-' + small + '-2T', 'hms-1000-2t']);
      rows.push([(units <= 4 ? '1 × DTU-WLite-S' : '1 × DTU-Pro-S') + ' gateway', units <= 4 ? 'dtu-wlite-s' : 'dtu-pro-s']);
      rows.push(['Trunk cable, ' + units + ' connector' + (units > 1 ? 's' : ''), 'trunk-cable-hms']);
      steps.push(w + ' W panels sit in the ' + model + ' range, four per unit' + (rem ? '; the leftover ' + rem + ' panel' + (rem > 1 ? 's go' : ' goes') + (rem === 3 ? ' on one more 4-in-1' : ' on a 2-in-1') : '') + '.');
      steps.push(units <= 4 ? 'Up to four microinverters: the DTU-WLite-S gateway is enough.' : 'More than four microinverters: use the DTU-Pro-S gateway.');
    }
    var ratio = dc / ac;
    steps.push('AC output ' + (ac / 1000).toFixed(2) + ' kVA, DC/AC ratio ' + ratio.toFixed(2) + (ratio > 1.35 ? ' — high; expect some clipping at midday.' : '.'));
    steps.push('At 4.0 kWh per kWp less 15% for weather, expect about ' + Math.round(dc / 1000 * sun * 30) + ' kWh a month.');

    $('z-dc').textContent = (dc / 1000).toFixed(2);
    $('z-ac').textContent = (ac / 1000).toFixed(2);
    $('z-gen').textContent = Math.round(dc / 1000 * sun * 30).toLocaleString('en-PH');
    $('z-bom').innerHTML = '<p class="calc__label">Bill of materials</p><h2>' + units + ' microinverter' + (units > 1 ? 's' : '') + '</h2><ul>' +
      rows.map(function (r) { return '<li>' + (r[1] ? '<a href="' + r[1] + '.html">' + r[0] + '</a>' : r[0]) + '</li>'; }).join('') +
      '</ul><a class="btn btn--green" href="quote.html?product=' + (rows[0][1] || '') + '">Request a quote for this</a>';
    $('z-working').innerHTML = steps.map(function (s) { return '<li>' + s + '</li>'; }).join('');
  }
  form.addEventListener('input', size);
  form.addEventListener('change', size);
  size();
})();

/* copy-link button on product pages */
(function () {
  document.querySelectorAll('.share__copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var done = function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy link'; }, 1800); };
      if (navigator.clipboard) { navigator.clipboard.writeText(b.dataset.copy).then(done, function(){}); }
    });
  });
})();

/* Photo tab sliders (Products & Solutions, Success Stories) */
(function () {
  document.querySelectorAll('[data-tabslider]').forEach(function (box) {
    var panes = box.querySelectorAll('.sol'), tabs = box.querySelectorAll('.soltab'), i = 0, t;
    function go(n) {
      i = (n + panes.length) % panes.length;
      panes.forEach(function (p, k) { p.classList.toggle('is-active', k === i); });
      tabs.forEach(function (b, k) { b.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
    }
    tabs.forEach(function (b, k) { b.addEventListener('click', function () { go(k); clearInterval(t); }); });
    t = setInterval(function () { go(i + 1); }, 7000);
  });
})();

/* All-products filter */
(function () {
  var f = document.getElementById('catFilter');
  if (!f) return;
  var cards = document.querySelectorAll('#catalogGrid .product');
  function apply() {
    var v = (f.querySelector('input:checked') || {}).value || 'all';
    cards.forEach(function (c) { c.hidden = !(v === 'all' || c.dataset.cat === v); });
    if (history.replaceState) history.replaceState(null, '', v === 'all' ? location.pathname : '#' + v);
  }
  f.addEventListener('change', apply);
  var h = location.hash.slice(1);
  if (h) { var r = f.querySelector('input[value="' + h + '"]'); if (r) r.checked = true; }
  apply();
})();

/* Product page section bar */
(function () {
  var bar = document.querySelector('.subnav');
  if (!bar) return;
  var links = Array.prototype.filter.call(bar.querySelectorAll('a'), function (a) { return a.getAttribute('href').charAt(0) === '#'; });
  function sync() {
    var cur = null;
    links.forEach(function (a) {
      var s = document.querySelector(a.getAttribute('href'));
      if (s && s.getBoundingClientRect().top < 200) cur = a;
    });
    links.forEach(function (a) { a.classList.toggle('is-on', a === cur); });
  }
  window.addEventListener('scroll', sync, { passive: true }); sync();
})();

/* Home page quick savings estimate */
(function () {
  var inp = document.getElementById('q-bill');
  if (!inp) return;
  var out = document.getElementById('q-out'), go = document.getElementById('q-go');
  var S = window.HM_SYSTEMS || [], rate = window.HM_RATE || 15.55, sun = (window.HM_SUN || 4) * 0.85;
  var peso = function (n) { return '₱' + Math.round(n).toLocaleString('en-PH'); };
  function run() {
    var bill = parseFloat(inp.value) || 0;
    if (bill < 500 || !S.length) { out.textContent = 'Enter your bill to see an estimate.'; return; }
    var daily = bill / rate / 30, sys = S[S.length - 1];
    for (var i = 0; i < S.length; i++) { if (S[i].kwp * sun >= daily * 0.9) { sys = S[i]; break; } }
    var prod = sys.kwp * sun, day = Math.min(prod, daily * 0.45);
    var night = Math.min(Math.max(0, prod - day), sys.kwh * 0.9, daily * 0.55);
    var save = Math.min((day + night) * rate * 30, bill * 0.85);
    out.innerHTML = 'About <strong>' + peso(save) + '</strong> a month off your bill with solar and a <a class="ulink" href="' + sys.slug + '.html">' + sys.name + '</a>.';
    go.href = 'savings-calculator.html';
  }
  inp.addEventListener('input', run); run();
})();
