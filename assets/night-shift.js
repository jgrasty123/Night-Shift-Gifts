/* ==========================================================================
   Night Shift Gift Co. — theme JS
   No framework, no build step. Everything is progressive: the page works
   with JS off, this only upgrades it.
   ========================================================================== */
(function () {
  'use strict';

  var money = function (cents) {
    return '$' + (cents / 100).toFixed(2);
  };

  var escapeHtml = function (str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };

  /* ---------------- mobile nav ---------------- */
  var navToggle = document.querySelector('[data-nav-toggle]');
  var navDrawer = document.getElementById('nav-drawer');
  if (navToggle && navDrawer) {
    navToggle.addEventListener('click', function () {
      var open = navDrawer.hasAttribute('open');
      if (open) {
        navDrawer.removeAttribute('open');
      } else {
        navDrawer.setAttribute('open', '');
      }
      navToggle.setAttribute('aria-expanded', String(!open));
    });
  }

  /* ---------------- cart drawer ---------------- */
  var drawer   = document.querySelector('[data-cart-drawer]');
  var scrim    = document.querySelector('[data-scrim]');
  var body     = document.querySelector('[data-cart-body]');
  var foot     = document.querySelector('[data-cart-foot]');
  var subtotal = document.querySelector('[data-cart-subtotal]');
  var lastFocus = null;

  var root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';

  function setCount(n) {
    document.querySelectorAll('[data-cart-count]').forEach(function (el) { el.textContent = n; });
    document.querySelectorAll('.bag').forEach(function (el) {
      el.setAttribute('data-has-items', String(n > 0));
    });
  }

  function renderCart(cart) {
    setCount(cart.item_count);
    if (!body) return;

    if (!cart.items.length) {
      body.innerHTML = '<p class="drawer__empty">Your cart is empty.</p>';
      if (foot) foot.hidden = true;
      return;
    }

    body.innerHTML = cart.items.map(function (item, i) {
      // line item properties (e.g. Gift message); skip Shopify's _private keys
      var props = Object.keys(item.properties || {})
        .filter(function (k) { return k.charAt(0) !== '_' && item.properties[k]; })
        .map(function (k) { return k + ': ' + escapeHtml(item.properties[k]); })
        .join(' · ');

      var meta = [];
      if (item.variant_title && item.variant_title !== 'Default Title') meta.push(escapeHtml(item.variant_title));
      if (item.selling_plan_allocation) meta.push(item.selling_plan_allocation.selling_plan.name);
      if (props) meta.push(props);

      return '' +
        '<div class="dline" data-line="' + (i + 1) + '">' +
          '<div class="dline__img">' +
            (item.image ? '<img src="' + item.image.replace(/(\.[a-z]+)(\?|$)/i, '_160x$1$2') + '" alt="">' : '') +
          '</div>' +
          '<div>' +
            '<b>' + escapeHtml(item.product_title) + '</b>' +
            (meta.length ? '<div class="dline__meta">' + meta.join(' · ') + '</div>' : '') +
            '<div class="qty">' +
              '<button type="button" data-line-step="-1" aria-label="Decrease quantity">&minus;</button>' +
              '<output>' + item.quantity + '</output>' +
              '<button type="button" data-line-step="1" aria-label="Increase quantity">+</button>' +
            '</div>' +
            '<button class="dline__remove" type="button" data-line-remove>Remove</button>' +
          '</div>' +
          '<div class="dline__price">' + money(item.final_line_price) + '</div>' +
        '</div>';
    }).join('');

    if (foot) foot.hidden = false;
    if (subtotal) subtotal.textContent = money(cart.total_price);
  }

  function fetchCart() {
    return fetch(root + 'cart.js', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (cart) { renderCart(cart); return cart; });
  }

  function openCart() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    if (scrim) { scrim.hidden = false; scrim.setAttribute('data-open', 'true'); }
    drawer.setAttribute('data-open', 'true');
    drawer.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var close = drawer.querySelector('[data-cart-close]');
    if (close) close.focus();
  }

  function closeCart() {
    if (!drawer) return;
    drawer.setAttribute('data-open', 'false');
    drawer.setAttribute('aria-hidden', 'true');
    if (scrim) scrim.setAttribute('data-open', 'false');
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  if (scrim) scrim.addEventListener('click', closeCart);
  document.querySelectorAll('[data-cart-close]').forEach(function (b) {
    b.addEventListener('click', closeCart);
  });

  document.addEventListener('keydown', function (e) {
    if (!drawer || drawer.getAttribute('data-open') !== 'true') return;
    if (e.key === 'Escape') { closeCart(); return; }
    if (e.key !== 'Tab') return;
    // trap focus inside the drawer
    var f = drawer.querySelectorAll('button, [href], input, select, textarea');
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  // header cart button opens the drawer instead of navigating
  document.querySelectorAll('.bag').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!drawer) return;              // no JS drawer -> let the link go to /cart
      e.preventDefault();
      fetchCart().then(openCart);
    });
  });

  // line quantity + remove, delegated
  if (body) {
    body.addEventListener('click', function (e) {
      var line = e.target.closest('[data-line]');
      if (!line) return;
      var index = parseInt(line.getAttribute('data-line'), 10);
      var qtyEl = line.querySelector('output');
      var current = parseInt(qtyEl.textContent, 10);
      var next = null;

      if (e.target.closest('[data-line-remove]')) next = 0;
      var step = e.target.closest('[data-line-step]');
      if (step) next = current + parseInt(step.getAttribute('data-step') || step.getAttribute('data-line-step'), 10);
      if (next === null || next < 0) return;

      body.style.opacity = '.5';
      fetch(root + 'cart/change.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({ line: index, quantity: next })
      })
        .then(function (r) { return r.json(); })
        .then(renderCart)
        .catch(function () { window.location.href = root + 'cart'; })
        .finally(function () { body.style.opacity = ''; });
    });
  }

  /* ---------------- add to cart ---------------- */
  function submitAdd(form, btn) {
    var label = btn ? btn.textContent : '';
    if (btn) { btn.setAttribute('data-state', 'loading'); btn.textContent = 'Adding…'; }

    return fetch(form.action || (root + 'cart/add'), {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.data && res.data.description || 'Add failed');
        if (btn) { btn.setAttribute('data-state', 'done'); btn.textContent = 'Added'; }
        var note = form.querySelector('[data-gift-message]');
        if (note) { note.value = ''; note.dispatchEvent(new Event('input')); }
        return fetchCart().then(function () {
          openCart();
          setTimeout(function () {
            if (btn) { btn.removeAttribute('data-state'); btn.textContent = label; }
          }, 1600);
        });
      })
      .catch(function () {
        if (btn) { btn.removeAttribute('data-state'); btn.textContent = label; }
        form.submit();                  // fall back to the normal POST
      });
  }

  document.querySelectorAll('form[data-quick-add]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      submitAdd(form, form.querySelector('button'));
    });
  });

  var pdpForm = document.querySelector('#product-form');
  if (pdpForm) {
    pdpForm.addEventListener('submit', function (e) {
      e.preventDefault();
      submitAdd(pdpForm, pdpForm.querySelector('[data-pdp-add]'));
    });
  }

  // paint the badge on load
  setCount(parseInt((document.querySelector('[data-cart-count]') || {}).textContent || '0', 10));

  /* ---------------- product gallery ---------------- */
  var thumbs = document.querySelector('[data-pdp-thumbs]');
  var mainImg = document.querySelector('[data-pdp-img]');
  if (thumbs && mainImg) {
    thumbs.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      mainImg.src = btn.getAttribute('data-full');
      thumbs.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-current', String(b === btn));
      });
    });
  }

  /* ---------------- variant / pack selector ---------------- */
  var pdp = document.querySelector('[data-product]');
  if (pdp) {
    var variants = [];
    try {
      variants = JSON.parse(pdp.getAttribute('data-variants') || '[]');
    } catch (err) {
      variants = [];
    }

    var optionRows = Array.prototype.slice.call(pdp.querySelectorAll('[data-option-index]'));
    var variantInput = pdp.querySelector('[data-variant-input]');
    var priceEl = pdp.querySelector('[data-pdp-price]');
    var compareEl = pdp.querySelector('[data-pdp-compare]');
    var addBtn = pdp.querySelector('[data-pdp-add]');

    function currentSelection() {
      return optionRows.map(function (row) {
        var on = row.querySelector('[aria-pressed="true"]');
        return on ? on.getAttribute('data-option-value') : null;
      });
    }

    function matchVariant(selection) {
      return variants.find(function (v) {
        return selection.every(function (val, i) {
          return val === null || v.options[i] === val;
        });
      });
    }

    function markAvailability(selection) {
      optionRows.forEach(function (row, rowIndex) {
        row.querySelectorAll('.pack').forEach(function (btn) {
          var trial = selection.slice();
          trial[rowIndex] = btn.getAttribute('data-option-value');
          var match = variants.find(function (v) {
            return trial.every(function (val, i) {
              return val === null || v.options[i] === val;
            });
          });
          btn.setAttribute('data-available', String(!!(match && match.available)));
        });
      });
    }

    function syncVariant() {
      var selection = currentSelection();
      var variant = matchVariant(selection);
      markAvailability(selection);

      if (!variant) {
        if (addBtn) { addBtn.disabled = true; addBtn.textContent = 'Unavailable'; }
        return;
      }

      if (variantInput) variantInput.value = variant.id;
      if (priceEl) priceEl.textContent = money(variant.price);

      if (compareEl) {
        if (variant.compare_at_price && variant.compare_at_price > variant.price) {
          compareEl.textContent = money(variant.compare_at_price);
          compareEl.hidden = false;
        } else {
          compareEl.hidden = true;
        }
      }

      if (addBtn) {
        addBtn.disabled = !variant.available;
        addBtn.textContent = variant.available ? 'Add to cart' : 'Sold out';
      }

      // keep the URL shareable without a reload
      var url = new URL(window.location.href);
      url.searchParams.set('variant', variant.id);
      window.history.replaceState({}, '', url);
    }

    optionRows.forEach(function (row) {
      row.addEventListener('click', function (e) {
        var btn = e.target.closest('.pack');
        if (!btn) return;
        row.querySelectorAll('.pack').forEach(function (b) {
          b.setAttribute('aria-pressed', String(b === btn));
        });
        syncVariant();
      });
    });

    if (optionRows.length) syncVariant();
  }

  /* ---------------- gift message counter ---------------- */
  document.querySelectorAll('[data-gift-message]').forEach(function (field) {
    var wrap = field.closest('.giftnote');
    var out = wrap && wrap.querySelector('[data-gift-count]');
    if (!out) return;
    var paint = function () { out.textContent = field.value.length; };
    field.addEventListener('input', paint);
    paint();
  });

  /* ---------------- entrance animation ---------------- */
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('.armed').forEach(function (el) { io.observe(el); });
  }
})();
