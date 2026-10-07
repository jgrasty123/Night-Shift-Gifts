// Add-on pairing regression tests — audit FIX-06 (2026-10-07).
// A paid add-on (card, engraving, glass) added with a basket carries
// properties._ns_parent = the basket's properties._ns_pair. Removing or
// re-quantifying the basket must take its add-ons with it, and orphaned
// add-ons must be swept on cart load.
// Run: node tests/cart-addons.test.mjs   (needs `playwright` + chromium)
import { chromium } from 'playwright';
import { readFileSync } from 'fs';

const JS = readFileSync(new URL('../assets/night-shift.js', import.meta.url), 'utf8');
const PAGE = (count) => `<!doctype html><html><body>
<a class="bag" href="/cart"><span data-cart-count>${count}</span></a><div data-scrim hidden></div>
<aside data-cart-drawer data-open="false"><button data-cart-close>x</button><div data-cart-body></div><div data-cart-foot hidden><span data-cart-subtotal></span></div></aside>
<script src="/theme.js"></script></body></html>`;

const line = (key, title, qty, properties) => ({
  key, product_title: title, variant_title: null, quantity: qty, final_line_price: 1000 * qty,
  image: null, properties, selling_plan_allocation: null,
});

function scenario(name) {
  switch (name) {
    case 'remove':  // basket + card + engraving, plus an unrelated plain item
    case 'step':
    case 'stepper':
      return [
        line('k-basket', 'Nightcap', 1, { _ns_pair: 'p1', 'Gift message': 'Hi' }),
        line('k-card', 'Greeting Card', 1, { For: 'Nightcap', Message: 'Congrats', _ns_parent: 'p1' }),
        line('k-engr', 'Engraving', 1, { For: 'Nightcap', 'Engraving Text': 'Dad', _ns_parent: 'p1' }),
        line('k-plain', 'Clock-In Kit', 1, null),
      ];
    case 'orphan':  // basket already gone (e.g. removed on /cart page)
      return [
        line('k-card', 'Greeting Card', 1, { For: 'Nightcap', Message: 'x', _ns_parent: 'gone' }),
        line('k-plain', 'Clock-In Kit', 1, null),
      ];
    case 'legacy':  // pre-fix add-on without pairing keys must be left alone
      return [
        line('k-basket', 'Nightcap', 1, null),
        line('k-card', 'Greeting Card', 1, { For: 'Nightcap', Message: 'x' }),
      ];
  }
}

async function run(name) {
  let items = scenario(name);
  const cart = () => ({ item_count: items.reduce((a, i) => a + i.quantity, 0), total_price: 0, items });
  const updateCalls = [];
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.route('**/*', async (r) => {
    const u = r.request().url();
    if (u.endsWith('/cart.js')) return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(cart()) });
    if (u.endsWith('/cart/update.js')) {
      const { updates } = JSON.parse(r.request().postData());
      updateCalls.push(updates);
      items = items.map((i) => (i.key in updates ? { ...i, quantity: updates[i.key] } : i)).filter((i) => i.quantity > 0);
      return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(cart()) });
    }
    if (u.endsWith('/cart/change.js')) {
      const { line: l, quantity } = JSON.parse(r.request().postData());
      items = items.map((i, idx) => (idx === l - 1 ? { ...i, quantity } : i)).filter((i) => i.quantity > 0);
      return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(cart()) });
    }
    if (u.endsWith('/theme.js')) return r.fulfill({ status: 200, contentType: 'application/javascript', body: JS });
    return r.fulfill({ status: 200, contentType: 'text/html', body: PAGE(cart().item_count) });
  });
  await page.goto('https://store.test/');
  await page.waitForTimeout(400);
  await page.click('.bag');
  await page.waitForTimeout(400);

  let steppers = null;
  if (name === 'remove') await page.click('[data-line="1"] [data-line-remove]');
  if (name === 'step') await page.click('[data-line="1"] [data-line-step="1"]');
  if (name === 'stepper') steppers = await page.evaluate(() =>
    [...document.querySelectorAll('[data-line]')].map((l) => !!l.querySelector('[data-line-step]')));
  await page.waitForTimeout(500);
  await browser.close();
  return { keys: items.map((i) => `${i.key}x${i.quantity}`), updateCalls: updateCalls.length, steppers };
}

const cases = {
  remove:  (r) => r.keys.join() === 'k-plainx1' && r.updateCalls === 1,
  step:    (r) => r.keys.join() === 'k-basketx2,k-cardx2,k-engrx2,k-plainx1',
  stepper: (r) => JSON.stringify(r.steppers) === '[true,false,false,true]',
  orphan:  (r) => r.keys.join() === 'k-plainx1' && r.updateCalls === 1,
  legacy:  (r) => r.keys.join() === 'k-basketx1,k-cardx1' && r.updateCalls === 0,
};
let failed = 0;
for (const [name, ok] of Object.entries(cases)) {
  const r = await run(name);
  const pass = ok(r);
  if (!pass) failed++;
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name.padEnd(8)} ${JSON.stringify(r)}`);
}
process.exit(failed ? 1 : 0);
