# Night Shift Gift Co. — Shopify theme

Online Store 2.0 theme for **Night Shift Gift Co.**, the new-parent and baby
shower gift basket store on `lil-and-mil.myshopify.com`. Built from the
Brew Hunters theme (`The-Bev-Connect-Portals/Brew_Hunters`): same construction
and section system, new palette, type and a gift-product layout.

Plain Liquid, CSS and vanilla JS. No framework, no build step.

The Lil & Mil products stay in this store but are sold through the headless
site at `jgrasty123/Lil-n-Mil` (lilandmil.com).

## Branches

| Branch | Contents |
| --- | --- |
| `main` | This theme. Connect it to Shopify with the GitHub integration. |

## File layout

```
assets/       base.css, night-shift.js
config/       settings_schema.json, settings_data.json
layout/       theme.liquid
locales/      en.default.json
sections/     custom sections + main-* templates + header/footer groups
snippets/     product-card, arc-sticker, icon-sprite, cart-drawer, meta-tags
templates/    index, product, collection, list-collections, cart, page, search, 404
```

## Colour system

Every section has a `color_scheme` select that sets `--bg`/`--fg` through
`.scheme--*` in `base.css`. Sections never hard-code a background.

| Token | Hex | Use |
| --- | --- | --- |
| `--midnight` | `#1F2A44` | Hero, promo bar, footer, borders |
| `--ink` | `#262A36` | Body text on light grounds |
| `--gold` | `#E8B45A` | Lamplight. Buttons, stickers, moon. Always midnight text on it |
| `--cream` | `#FAF5EA` | Moon cream, the page ground |
| `--paper` | `#FFFDF7` | Cards, product grids |
| `--nightlight` | `#DCE3F0` | Soft blue tiles and banners |
| `--blush` | `#EBC9BC` | Dawn blush, mom-side accents |
| `--wick` | `#8A5A1C` | Gold darkened for small text on light grounds (5.4:1) |

Gold on cream is only 1.7:1, so gold is never used for text or icons on a
light ground — that is what `--wick` is for.

Type: **Nunito** 800 (display, sentence case) and **Figtree** (body), both free
on Google Fonts. The Brew Hunters all-caps and monospace labels were removed.

`wave-divider`: the front layer must match the `color_scheme` of the section
directly below it, or you get a visible seam.

## Sections

| Section | Notes |
| --- | --- |
| `promo-marquee` | Blocks are messages. |
| `header` | Sticky, uses `main-menu`. Wordmark with a moon when no logo is set. |
| `split-hero` | Line 2 renders in lamplight gold. With no image, shows a moon and stars instead of a stock placeholder. |
| `wave-divider` | Two shapes, three colour layers. |
| `value-props` | Up to 4, icons: gift, card, moon, delivery, heart. |
| `collection-tiles` | Shop by recipient. Each tile points at a collection; count auto-fills. |
| `featured-products` | Placeholder cards when the collection is empty. |
| `feature-banner` | Image + copy + button. Replaces the Brew Hunters build-a-box banner. |
| `main-product` | Gallery, variant buttons, gift message, metafield accordions. |
| `review-block` | Ships in placeholder mode — see content rules. |
| `footer` | Text / menu / newsletter blocks. |

Removed from Brew Hunters: the 12-can `build-a-box` section, its page
template, script and styles, and the beer imagery.

## Collections the home page expects

Create these (smart collections on tags are easiest). Until they exist, the
tiles show 0 and the grid shows placeholder cards.

| Handle | Used by |
| --- | --- |
| `new-moms` | Home tile |
| `new-dads` | Home tile |
| `baby-shower` | Home tile |
| `push-presents` | Home tile |
| `gift-baskets` | Home grid, "More gifts" on product pages |

The "Shop booze-free" banner button has no link yet; point it at a
`booze-free` collection in the theme editor once one exists.

## Products

**Card flags** come from tags: `best-seller`, `new`. The `booze-free` tag adds
a "Booze-free" pill on cards and product pages.

**Products with options** (e.g. with/without alcohol) show a *Choose* link on
cards instead of quick-add, so nobody adds the wrong version from the grid.

**What's inside** accordion reads `custom.whats_inside`. Create it under
Settings → Custom data → Products as a *list of single line text* (one line per
item); multi-line text and rich text also work. No value, no accordion.

**Gift message.** The product page has an optional gift message box (on by
default, 200 characters). It is saved on the order as the line item property
**Gift message** and shows in the cart. Fulfillment has to print it — confirm
it comes through to the packing slip / ShipStation before advertising it.

## Store notices

Theme settings → Store notices. `shipping_notice`, `age_notice` and
`signature_notice` are display only and hidden when blank. Fill the age and
signature notices only if baskets containing alcohol sell on this store.
Eligibility and age checks happen at checkout, never in theme copy.

## Working on this theme

1. `config/settings_data.json` is owned by Shopify once connected and is
   force-pushed back on every theme-editor save.
2. `url` settings cannot carry defaults — Shopify silently rejects the section.
3. Always `git pull --rebase origin main` before pushing; the GitHub sync pushes
   "Update from Shopify" commits.

## Content rules

No invented reviews, awards, ratings or product claims. The review block stays
in placeholder mode until a review app supplies real reviews.
