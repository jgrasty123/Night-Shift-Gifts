# Night Shift Gift Co. — basket catalog

Product and collection imports for the 13 launch baskets, plus ChatGPT image
prompts. **Lives on the `catalog/baskets-v1` branch on purpose**: `main` is
connected to Shopify and should only hold theme files.

Everything is generated from `build_catalog.py`. Edit the data there and rerun
it — don't hand-edit the CSVs.

```
python3 catalog/build_catalog.py
```

## Files

| File | Import as | What it does |
| --- | --- | --- |
| `matrixify_baskets_1of2.csv` | Products | Baskets NS-001 to NS-007 |
| `matrixify_baskets_2of2.csv` | Products | Baskets NS-008 to NS-013 |
| `matrixify_collections.csv` | Smart Collections | `gift-baskets`, `new-moms`, `new-dads`, `baby-shower`, `push-presents` — the handles the theme expects |
| `image_prompts.md` | — | ChatGPT prompts generated from the recipes by `build_prompts.py` |
| `recipes.json` | — | Source of truth: contents + packaging per basket |
| `nightshift_MASTER_bundles.xlsx` | SumTracker (Upload tab) | Built by `build_bundles.py` — recipes, costs, price worksheet |

Split in two because the Matrixify plan caps products per job.

## Safe by default

Every basket imports as **Draft, unpublished, price $0.00**, tagged
`needs-pricing` and `needs-photos`. Nothing can be bought until you set a real
price and switch it to Active.

## Before a basket goes Active

1. **Price and cost.** Set Variant Price (and Variant Cost for margin tracking),
   then remove the `needs-pricing` tag.
2. **Contents.** `custom.whats_inside` is the *plan*. Change it to what is
   actually in the box — it shows on the product page.
3. **Photos.** Add the image, remove `needs-photos`.
4. **Weight.** Set a real packed weight so shipping rates are right.
5. **SumTracker recipe.** Map the basket SKU to its components so Lil & Mil
   stock decrements. `custom.lil_mil_components` lists them (SKU x qty).
6. **Alcohol versions** (`NS-00x-ALC`: Midnight Toast, Off the Clock,
   Graveyard Shift, Nightcap, Lights Out). The booze-free version is always the
   first, default variant. Leave the ALC variants out of stock / unsellable until
   it is decided which store sells alcohol baskets. Delete them if they will
   live on another store.

## Import order

1. ~~Create the metafield definitions~~ — done 2026-09-16 via the Admin API
   (`custom.whats_inside`, `custom.lil_mil_components`).
2. Import `matrixify_baskets_1of2.csv`, check one product, then `2of2`.
   Confirm the What's inside list came through as separate lines.
3. Import `matrixify_collections.csv`.

## Tags

| Tag | Meaning |
| --- | --- |
| `gift-basket` | In the Gift Baskets collection |
| `for:new-moms` `for:new-dads` `for:baby-shower` `for:push-presents` | Drives the recipient collections |
| `booze-free` | Contains no alcohol at all — shows the Booze-free pill |
| `lm:leash` `lm:clips` `lm:tote` `lm:belt` `lm:cup` `lm:plates` | Which Lil & Mil stock it moves |
| `needs-pricing` `needs-photos` | Launch checklist; remove when done |
| `best-seller` `new` | Card flags (add later) |

## Lil & Mil stock per basket

| Item | Baskets |
| --- | --- |
| Stroller Saver leash (SA-003) | 001, 002, 003, 007, 009, 010, 011, 013 |
| Tot Tote (SA-005) | 005, 006, 008, 011 |
| Stroller clips 2-pack (SA-002) | 004, 006, 008, 011 |
| Car seat travel belt (TA-001) | 006, 011 |
| Silicone cup | 012, 013 |
| Silicone plates | 012 — only ~39 in stock |

Clips and belts are under 500 each, so baskets 006 and 011 will hit their limit
first. The Clock-In Kit (011) uses all four stroller items.
