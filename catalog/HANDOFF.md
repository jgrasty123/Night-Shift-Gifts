# Night Shift Gift Co. + Lil & Mil — Cowork Handoff

Prepared: September 16, 2026 · Owner: James Grasty (Go-To Gifting LLC)
Store: `lil-and-mil.myshopify.com` — now named **Night Shift Gifts Co.** (nightshiftgifts.com)

Read "Pick up here" first. Everything else is reference.

---

## Pick up here

**Catalog is live in the store as drafts (Sep 16, 3:00pm PT).** All three imports finished with 0 failures.

| Step | Status |
| --- | --- |
| 1. Products file 1 of 2 (NS-001–NS-007) | ✅ Matrixify job `746994786` — 7 new, 0 failed |
| 2. Spot-check | ✅ All Draft, $0.00, booze-free = variant 1, **What's inside came in as separate list lines** |
| 3. Products file 2 of 2 (NS-008–NS-013) | ✅ Job `746998920` — 6 new, 0 failed |
| 4. Smart collections (6) | ✅ Job `746998994` — 6 new, 0 failed. Rules verified. Matrixify warns the "Smart Collections" sheet is deprecated; use the "Collections" sheet next time |
| 5. Theme editor → home → "Shop booze-free" button | **Open** — link to `/collections/booze-free` |

Note: the `booze-free` collection matches tag `booze-free-option`, which every basket carries, so it lists all 13.

Next: packaging SKUs + component costs → prices → images → SumTracker recipes (Open items below).

---

## Where everything lives

| What | Location |
| --- | --- |
| Night Shift Shopify theme | `github.com/jgrasty123/Night-Shift-Gifts`, branch `main` — **connected to Shopify** (sync commits already arriving) |
| Basket catalog + bundles + prompts | Same repo, branch **`catalog/baskets-v1`**, folder `catalog/`. Kept off `main` so Shopify never reads it as theme files |
| Headless lilandmil.com | `github.com/jgrasty123/Lil-n-Mil`, branch `main`, commit `9e230a8`. Not yet on Netlify |
| Planning / punch list | Asana project "Lil & Mil → New Parent Gift Store + Headless lilandmil.com" (21 tasks, assigned to James). **The chat link in every task's notes points to the wrong chat** — replace or remove |
| Bounty bundle reference | Google Drive: `bounty_MASTER_bundles_4 - Sept 2026` (component names + costs came from here) |

### Files in `catalog/` (branch `catalog/baskets-v1`)

| File | Purpose |
| --- | --- |
| `build_catalog.py` | Source of truth for basket titles, copy, tags, What's inside. Regenerates the three CSVs |
| `matrixify_baskets_1of2.csv` / `2of2.csv` | Products import (split for the Matrixify per-job product cap) |
| `matrixify_collections.csv` | 6 smart collections on tags |
| `recipes.json` | **Source of truth for basket contents and packaging** (white or black, small or large) |
| `build_bundles.py` | Regenerates `nightshift_MASTER_bundles.xlsx` from recipes.json |
| `nightshift_MASTER_bundles.xlsx` | Recipes, SumTracker upload, new components, price worksheet, open flags — same layout as the Bounty master |
| `build_prompts.py` | Reads recipes.json and writes `image_prompts.md` |
| `image_prompts.md` | 18 ChatGPT prompts (13 baskets + 5 alcohol versions) |
| `README.md` | Import order, tags, launch checklist |

---

## Done this session

**Store**
- Metafield definitions created via Admin API: `custom.whats_inside` (list.single_line_text_field, storefront read, pinned) and `custom.lil_mil_components` (list.single_line_text_field, internal, pinned).

**Theme (`Night-Shift-Gifts/main`)**
- Built from the Brew Hunters theme. Night palette (midnight `#1F2A44`, lamplight gold `#E8B45A`, moon cream `#FAF5EA`, nightlight `#DCE3F0`, dawn blush `#EBC9BC`, wick `#8A5A1C` for small text on light). Nunito 800 + Figtree, sentence case.
- Home: midnight hero with moon fallback, value props, "Who's on the night shift?" recipient tiles, gift grid, booze-free banner, review block (placeholder mode).
- Product page: variant buttons, **gift message** line-item property (`Gift message`, 200 chars), metafield accordions (What's inside).
- Removed: build-a-box builder, beer images, ABV/pack specs. Alcohol notices blank by default.
- Passes Shopify theme-check (only Google Fonts CDN warnings).

**Catalog (13 baskets, all Draft / $0.00 / tagged `needs-pricing` `needs-photos`)**

| SKU | Basket | Versions | Lil & Mil stock used |
| --- | --- | --- | --- |
| NS-001 | Midnight Toast — Push Present | Booze-free / With sparkling wine | leash |
| NS-002 | Off the Clock — New Moms (Not for the Baby) | Booze-free / With wine | leash |
| NS-003 | Recovery Shift — Postpartum Care Package | — | leash |
| NS-004 | The 3AM Feed — New Mom | — | clips |
| NS-005 | Before the Night Shift — Mom-to-Be | — | Tot Tote |
| NS-006 | Graveyard Shift Survival Kit — New Dad | Booze-free / With craft beer | clips, belt, Tot Tote |
| NS-007 | Nightcap — First-Time Dad | Booze-free / With whiskey | leash |
| NS-008 | Night Shift Dad — Diaper Duty | — | Tot Tote, clips |
| NS-009 | Lights Out Date Night — New Parents | Booze-free / With wine | leash |
| NS-010 | The Morning After — Coffee | — | leash |
| NS-011 | Clock-In Kit — Baby Shower (hero) | — | Tot Tote, leash, clips, belt |
| NS-012 | Midnight Snack — First Feeding Set | — | plates, cup |
| NS-013 | Double Shift — Mom & Baby | — | cup, leash |

Booze-free is always variant 1 (default). Alcohol variants are `NS-00x-ALC`.

**Bundles workbook** — 18 recipes, 204 component rows, 22 new components without SKUs. Existing components and costs reuse Bounty/BroBasket SKUs (Ferrero FD-034, Ghirardelli FD-041, Marich FD-062/065/119, Popcornopolis FD-077, coffees FD-005/086, Fre AL-302, glasses ACC-025/033, spa ACC-201/203/SPA-04, packaging PKG-059/005/002/073/063). Lil & Mil costs from Shopify variant cost.

**Image prompts** — generated from the recipes; each lists reference photos to upload and items not sourced yet. Brand names deliberately left out of prompt text.

**Headless lilandmil.com (`Lil-n-Mil`)** — static site, same URL structure as old Shopify theme; 8 products, 4 collections, 19 blog posts, About/Contact/Partners/Register pages, 4 policies. Checkout via cart permalink to `lil-and-mil.myshopify.com` with `attributes[portal]=lilandmil`; optional Storefront token for live stock. Only imports vendor `Lil and Mil`. `LAUNCHED=False` (noindex) until cutover.

---

## Decisions made

- **Packaging (Sep 16):** white box + white fill for mom, baby, shower and couples baskets; black box + black fill for dad baskets NS-006/007/008. No gold tissue, no custom Night Shift box. White box = PKG-100; small black = PKG-082. White baskets use **PKG-059 Krinkle Cut Fill ($0.50)** — the fill in the official bundle list (James, Sep 16). Black fill and the large black box still use placeholders PKG-FILL-BLACK, PKG-BOX-BLACK-L.

- Store name **Night Shift Gift Co.** James confirmed availability; trademark clearance still recommended (Night Shift Brewing holds beer-class marks).
- Every basket carries a leash, clips or Tot Tote to move stock.
- NS-001 alcohol version is "With sparkling wine" (WINE-013 Mumm Brut Prestige), not champagne.
- No engraving claims anywhere (store has no engraving add-on).
- Jerky uses FD-026 Country Archer, not the Carnivore Candy "Tequila" jerky.
- Catalog files live on a branch, never on the Shopify-connected `main`.
- **Alcohol versions sell on this store** (James, Sep 16). ALC variants stay draft until priced.
- **Image prompts name the real brands** (James, Sep 16): stocked items must match the uploaded reference photos, labels included. Only not-yet-sourced items are generic.

## Corrected inventory facts (James, Sep 15)

- **Nevada Pack removed (Sep 16).** Moved the 800 Tot Totes (SA-005) to BB Warehouse, zeroed the rest (SA-003 1,789 · SA-002 760 · SA-001 12), then deactivated and deleted the location.
- A second, hidden fulfillment-service location **"Navada Pac"** held a duplicate 445 car seat belts (TA-001). Zeroed. The connector can't delete it (it belongs to another app) — remove it in Settings → Locations or by uninstalling that app.
- Counts now in Shopify (BB Warehouse): leash SA-003 1,646 · clips SA-002 757 + SA-002-1 500 · Tot Tote 800 · belt TA-001 445 · SA-001 0 · cup 2000 56 · plates 1010 18.
- Leash ~1,500 · Clips under 500 pairs (only 500 ever bought; 1-pack and 2-pack SKUs both claim stock) · Tot Tote 800 · Car seat belt under 500 · Silicone cups ~310, not reordering · Plates ~39.

---

## Open items

**Needs James**
1. Theme editor → Home → "Every basket, booze-free or not" banner → **Button link** = `/collections/booze-free` (currently blank, so it goes to all products). The Shopify connector can't write the live theme and this session can't push to the repo.
2. SKUs for black fill and the large black box (and whether PKG-100 fits the Tot Tote baskets). Then fill costs for the remaining new components.
3. Set prices in the Price Worksheet, then push prices to the products.
4. Real SKUs for BEER-TBD (Brew Hunters) and AL-TBD-WHISKEY (BroBasket).
5. Upload the SumTracker Upload tab once Lil & Mil SKUs and counts are confirmed there. Clip counts in Shopify (757 + 500) still exceed the ~500 pairs on hand.
6. Photos in ChatGPT with the regenerated brand-named prompts; send files to attach.
7. Confirm the gift message line-item property reaches the packing slip / ShipStation.
8. Netlify for `Lil-n-Mil` is set up; domain in progress. Headless-channel Storefront token still needed for live stock.
9. Delete the leftover "Navada Pac" location in admin.
10. TA-001 car seat belt is set to keep selling at 0 stock (CONTINUE); switch to deny if that isn't intended.

**Flags in the workbook's Open Flags tab** — packaging fit for Tot Tote baskets, pregnancy-safe check on ACC-203 in NS-005, placeholder SKUs ACC-GAME-CARDS / ACC-MUG-PAIR not in SumTracker, plate/cup colors (Black) and plate stock.

---

## Conventions to keep

- Matrixify connector to use: **Matrixify – Lil and Mil** (this store). Plan caps products per job — keep imports ≤10 products.
- Shopify MCP: run `get-shop-info` first and confirm `lil-and-mil.myshopify.com` before any write (earlier in this session it was pointed at Brew Hunters).
- Git: fine-grained PAT in clone URL, redact `github_pat_` from output, `git pull --rebase` before every push; commit identity James Grasty / james@gotogifting.com.
- `settings_data.json` and template JSON keep their `/* */` comment header.
- No invented reviews, awards, prices or product claims. Draft until real.
- Support email for configs: james@thebevconnect.com.
