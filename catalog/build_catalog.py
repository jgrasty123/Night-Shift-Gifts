#!/usr/bin/env python3
"""Night Shift Gift Co. — basket catalog source of truth.

Run from repo root:  python3 catalog/build_catalog.py

Writes:
  catalog/matrixify_baskets_1of2.csv   products 1-7   (Matrixify, Products entity)
  catalog/matrixify_baskets_2of2.csv   products 8-13
  catalog/matrixify_collections.csv     smart collections (Smart Collections entity)
  catalog/image_prompts.md              ChatGPT image prompts, one per basket

Everything imports as DRAFT, unpublished, price 0.00 and tagged `needs-pricing`.
Nothing here can be bought until prices are filled in and the product is set
Active. Contents lists are the PLAN — update them to what is actually sourced
before activating, because they feed the "What's inside" section on the page.
"""
import csv, pathlib

OUT = pathlib.Path(__file__).resolve().parent
VENDOR = "Night Shift Gift Co."
TYPE = "Gift Basket"

# Lil & Mil stock (real SKUs). Qty is what one basket uses.
LM = {
    "leash": ("SA-003", "Stroller Saver stroller safety leash"),
    "clips": ("SA-002", "Stroller clips (2-pack)"),
    "tote":  ("SA-005", "Tot Tote stroller organizer & crossbody bag"),
    "belt":  ("TA-001", "Car seat travel belt"),
    "cup":   ("2000",   "Silicone baby & toddler cup"),
    "plates":("1010",   "Silicone baby & toddler plates, set of 2"),
}

# Alcohol versions are listed so the plan is complete, but every basket's FIRST
# variant is booze-free and is the default. Alcohol variants must not be made
# sellable until it is decided which store/entity sells alcohol.
BASKETS = [
    dict(sku="NS-001", handle="midnight-toast-push-present", title="Midnight Toast — Push Present Gift Set",
         collections=["push-presents", "new-moms"], alc="With sparkling wine",
         lm=["leash"],
         inside=["Sparkling cider (booze-free) or sparkling wine", "Engraved flute", "Luxe chocolate bar", "Silk sleep mask"],
         blurb="For the one who did the hard part. A toast for the first quiet minute after the big day, whether that's 2pm or 2am.",
         scene="an engraved flute beside a bottle of sparkling cider, a chocolate bar and a folded silk sleep mask"),
    dict(sku="NS-002", handle="off-the-clock-new-mom-gift", title="Off the Clock — Gifts for New Moms (Not for the Baby)",
         collections=["new-moms"], alc="With wine", lm=["leash"],
         inside=["Spa set", "Chocolate", "Cozy socks", "Candle"],
         blurb="Everyone brings something for the baby. This one is for her: a small, deliberate break from the night shift.",
         scene="a soft spa set, cozy knit socks, a lit candle and a chocolate box"),
    dict(sku="NS-003", handle="recovery-shift-postpartum-care-package", title="Recovery Shift — Postpartum Care Package",
         collections=["new-moms"], alc=None, lm=["leash"],
         inside=["Soft throw or robe", "Lip balm", "Dry shampoo", "Large water tumbler", "Snacks"],
         blurb="The weeks after birth are a shift of their own. Comfort basics for the recovery, packed so she doesn't have to think about any of it.",
         scene="a folded soft robe, an oversized water tumbler, lip balm and a few wrapped snacks"),
    dict(sku="NS-004", handle="the-3am-feed-new-mom-gift-basket", title="The 3AM Feed — New Mom Gift Basket",
         collections=["new-moms", "baby-shower"], alc=None, lm=["clips"],
         inside=["One-handed snacks", "Lactation cookies", "Insulated tumbler", "Night-light"],
         blurb="Everything within one arm's reach for the feeds nobody else sees. Snacks you can eat with one hand and a light that won't wake anyone.",
         scene="a small warm night-light glowing beside a tumbler, cookies and one-handed snack packs"),
    dict(sku="NS-005", handle="before-the-night-shift-mom-to-be-gift-box", title="Before the Night Shift — Mom-to-Be Gift Box",
         collections=["new-moms", "baby-shower"], alc=None, lm=["tote"],
         inside=["Belly butter", "Pregnancy-safe spa items", "Zero-proof mocktail kit", "Cozy socks", "Tot Tote stroller organizer & crossbody bag"],
         blurb="For the last calm stretch before baby arrives. Pampering she can use now, and a bag she'll carry every day after.",
         scene="a jar of belly butter, a zero-proof mocktail kit, cozy socks and a black crossbody stroller organizer bag"),
    dict(sku="NS-006", handle="graveyard-shift-survival-kit-new-dad-gift", title="Graveyard Shift Survival Kit — New Dad Gift",
         collections=["new-dads"], alc="With craft beer", lm=["clips", "belt", "tote"],
         inside=["Jerky", "Craft root beer (booze-free) or craft beer", "Stroller clips (2-pack)", "Car seat travel belt", "Tot Tote stroller organizer & crossbody bag"],
         blurb="Fuel and gear for the new guy on the graveyard shift. Snacks for the 3am wake-ups and the stroller kit he'll actually use.",
         scene="jerky packs, two bottles of craft root beer, black stroller clips, a car seat travel strap and a black crossbody stroller organizer"),
    dict(sku="NS-007", handle="nightcap-first-time-dad-gift", title="Nightcap — First-Time Dad Gift",
         collections=["new-dads"], alc="With whiskey", lm=["leash"],
         inside=["Craft coffee (booze-free) or whiskey", "Engraved rocks glass", "Jerky", "Stroller Saver stroller safety leash"],
         blurb="One good drink for the end of a long first week. Coffee or whiskey, his call, poured in a glass with the year the family grew.",
         scene="an engraved rocks glass, a bag of craft coffee beans, jerky and a coiled stroller leash"),
    dict(sku="NS-008", handle="night-shift-dad-diaper-duty-gift-pack", title="Night Shift Dad — Diaper Duty Gift Pack",
         collections=["new-dads", "baby-shower"], alc=None, lm=["tote", "clips"],
         inside=["Tot Tote stroller organizer & crossbody bag", "Stroller clips (2-pack)", "Coffee", "Snacks"],
         blurb="A dad-proof diaper bag setup that clips to the stroller and slings over a shoulder, plus the coffee to get through the handoff.",
         scene="a black crossbody stroller organizer bag clipped with carabiners, a coffee bag and snacks"),
    dict(sku="NS-009", handle="lights-out-date-night-new-parents-gift-basket", title="Lights Out Date Night — New Parents Gift Basket",
         collections=["new-moms", "new-dads"], alc="With wine", lm=["leash"],
         inside=["Sparkling juice (booze-free) or wine", "Two glasses", "Gourmet snacks", "Card game"],
         blurb="A night in for two, once the baby is finally down. Everything for a date that doesn't require a sitter or leaving the couch.",
         scene="two stemmed glasses, a bottle of sparkling juice, a small card game box and gourmet snacks"),
    dict(sku="NS-010", handle="the-morning-after-new-parents-coffee-gift-box", title="The Morning After — New Parents Coffee Gift Box",
         collections=["new-moms", "new-dads"], alc=None, lm=["leash"],
         inside=["Craft coffee", "Two mugs", "Breakfast snacks", "Stroller Saver stroller safety leash"],
         blurb="For the morning after the longest night. Two mugs and good coffee, for whoever is on the early shift.",
         scene="two matching mugs, a bag of coffee beans and breakfast snacks"),
    dict(sku="NS-011", handle="clock-in-kit-baby-shower-gift-basket", title="Clock-In Kit — Baby Shower Gift Basket",
         collections=["baby-shower"], alc=None, lm=["tote", "leash", "clips", "belt"],
         inside=["Tot Tote stroller organizer & crossbody bag", "Stroller Saver stroller safety leash", "Stroller clips (2-pack)", "Car seat travel belt"],
         blurb="The practical shower gift: the stroller and travel kit new parents reach for every single day, ready before their first shift starts.",
         scene="a black crossbody stroller organizer, a coiled stroller leash, black stroller clips and a car seat travel strap"),
    dict(sku="NS-012", handle="midnight-snack-babys-first-feeding-set", title="Midnight Snack — Baby's First Feeding Set",
         collections=["baby-shower"], alc=None, lm=["plates", "cup"],
         inside=["Silicone baby & toddler plates, set of 2", "Silicone baby & toddler cup", "Bibs", "Board book"],
         blurb="For when the milk-only days end. Soft silicone plates and a cup that grows with them, plus a book for the table.",
         scene="stacked soft silicone baby plates, a small silicone toddler cup, a folded bib and a board book"),
    dict(sku="NS-013", handle="double-shift-mom-and-baby-gift-set", title="Double Shift — Mom & Baby Gift Set",
         collections=["new-moms", "baby-shower"], alc=None, lm=["cup", "leash"],
         inside=["Pampering items for mom", "Silicone baby & toddler cup", "Stroller Saver stroller safety leash"],
         blurb="Half for mom, half for baby, because they're both working the same shift.",
         scene="a small spa set on one side and a silicone toddler cup with a coiled stroller leash on the other"),
]

PRODUCT_COLS = [
    "Handle", "Command", "Title", "Body HTML", "Vendor", "Type", "Tags", "Tags Command",
    "Status", "Published", "Published Scope",
    "Option1 Name", "Option1 Value", "Variant Command", "Variant Position", "Variant SKU",
    "Variant Price", "Variant Compare At Price", "Variant Taxable", "Variant Requires Shipping",
    "Variant Inventory Tracker", "Variant Inventory Policy",
    "Metafield: custom.whats_inside [list.single_line_text_field]",
    "Metafield: custom.lil_mil_components [list.single_line_text_field]",
]


LM_LOOK = {
    "leash": "a coiled black stroller safety wrist leash",
    "clips": "a pair of black stroller clips with carabiners",
    "tote": "a black crossbody stroller organizer bag",
    "belt": "a black nylon car seat travel strap",
    "cup": "a small silicone toddler cup",
    "plates": "a set of two soft silicone baby plates",
}
for b in BASKETS:
    for k in b["lm"]:
        name = LM[k][1]
        if name not in b["inside"]:
            b["inside"].append(name)
        look = LM_LOOK[k]
        key = {"leash": "leash", "clips": "clips", "tote": "organizer", "belt": "strap", "cup": "cup", "plates": "plates"}[k]
        if key not in b["scene"]:
            b["scene"] += ", and " + look


def body(b):
    return f"<p>{b['blurb']}</p>"


def product_rows(b):
    tags = ["gift-basket", "night-shift", "needs-pricing", "needs-photos"]
    tags += [f"for:{c}" for c in b["collections"]]
    tags.append("booze-free-option")
    if not b["alc"]:
        tags.append("booze-free")
    tags.append("lm:" + ",lm:".join(b["lm"]))
    components = [f"{LM[k][0]} x1 — {LM[k][1]}" for k in b["lm"]]
    variants = [("Booze-free", b["sku"])]
    if b["alc"]:
        variants.append((b["alc"], b["sku"] + "-ALC"))
    rows = []
    for i, (label, sku) in enumerate(variants):
        first = i == 0
        inside = b["inside"]
        rows.append({
            "Handle": b["handle"],
            "Command": "NEW" if first else "",
            "Title": b["title"] if first else "",
            "Body HTML": body(b) if first else "",
            "Vendor": VENDOR if first else "",
            "Type": TYPE if first else "",
            "Tags": ", ".join(tags) if first else "",
            "Tags Command": "REPLACE" if first else "",
            "Status": "Draft" if first else "",
            "Published": "FALSE" if first else "",
            "Published Scope": "global" if first else "",
            "Option1 Name": "Version" if b["alc"] else "Title",
            "Option1 Value": label if b["alc"] else "Default Title",
            "Variant Command": "MERGE",
            "Variant Position": i + 1,
            "Variant SKU": sku,
            "Variant Price": "0.00",
            "Variant Compare At Price": "",
            "Variant Taxable": "TRUE",
            "Variant Requires Shipping": "TRUE",
            "Variant Inventory Tracker": "shopify",
            "Variant Inventory Policy": "deny",
            "Metafield: custom.whats_inside [list.single_line_text_field]": "\n".join(inside) if first else "",
            "Metafield: custom.lil_mil_components [list.single_line_text_field]": "\n".join(components) if first else "",
        })
    return rows


def write_products(name, baskets):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PRODUCT_COLS)
        w.writeheader()
        for b in baskets:
            for r in product_rows(b):
                w.writerow(r)


COLLECTIONS = [
    ("gift-baskets", "Gift Baskets", "tag", "equals", "gift-basket"),
    ("new-moms", "Gifts for New Moms", "tag", "equals", "for:new-moms"),
    ("new-dads", "Gifts for New Dads", "tag", "equals", "for:new-dads"),
    ("baby-shower", "Baby Shower Gifts", "tag", "equals", "for:baby-shower"),
    ("push-presents", "Push Presents", "tag", "equals", "for:push-presents"),
    ("booze-free", "Booze-Free Gift Baskets", "tag", "equals", "booze-free-option"),
]


def write_collections():
    cols = ["Handle", "Command", "Title", "Body HTML", "Sort Order", "Published", "Must Match",
            "Rule: Product Column", "Rule: Relation", "Rule: Condition"]
    with open(OUT / "matrixify_collections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for h, t, col, rel, cond in COLLECTIONS:
            w.writerow({"Handle": h, "Command": "NEW", "Title": t, "Body HTML": "", "Sort Order": "best-selling",
                        "Published": "TRUE", "Must Match": "all conditions",
                        "Rule: Product Column": col, "Rule: Relation": rel, "Rule: Condition": cond})


STYLE = (
    "Square 1:1 product photo, 2048x2048. Overhead three-quarter angle. A kraft gift box with a "
    "deep midnight-blue (#1F2A44) lid set to one side and warm lamplight-gold (#E8B45A) tissue paper "
    "inside. Background: seamless warm cream (#FAF5EA). Soft warm light from one side like a bedside "
    "lamp at night, gentle shadows. A small printed card tucked in the tissue with a simple crescent "
    "moon icon and no other text. Clean, premium, cozy. No people, no hands, no brand logos or label "
    "text on any item, no watermarks."
)


def write_prompts():
    lines = ["# Night Shift Gift Co. — ChatGPT image prompts", "",
             "One prompt per basket. Same style block every time so the catalog looks like a set.", "",
             "## How to use", "",
             "1. Open ChatGPT and start a new chat for each basket (keeps styles from drifting).",
             "2. **For any basket with Lil & Mil items, upload the real Lil & Mil product photos first** "
             "(from lilandmil.com or the Shopify product) and say: *\"Use these exact products as they look "
             "in the photos.\"* Otherwise ChatGPT invents a different-looking bag, leash or clip, and the "
             "photo will not match what the customer receives.",
             "3. Paste the prompt. Ask for revisions in plain words (\"move the bag to the front\", \"less clutter\").",
             "4. Download the PNG, name it `<handle>.png`, and upload it to the product in Shopify "
             "(or send the files and I will attach them via Matrixify).",
             "5. Generated images show *planned* contents. Reshoot or regenerate once real items are sourced "
             "if anything looks different.", "",
             "## Style block (already included below)", "", "> " + STYLE, ""]
    for b in BASKETS:
        lm_note = ", ".join(LM[k][1] for k in b["lm"])
        lines += [f"## {b['title']}", "", f"Handle: `{b['handle']}`  ·  Lil & Mil photos to upload: {lm_note}", "",
                  "```", f"Gift basket product photo for \"{b['title'].split(' — ')[0]}\". Inside the box: {b['scene']}. "
                  "Arrange the items so every one is clearly visible and not overlapping. " + STYLE, "```", ""]
        if b["alc"]:
            lines += [f"*Booze-free version image:* same prompt, and say the bottle is clearly a non-alcoholic "
                      f"sparkling drink or coffee with no alcohol cues. Make a second image only if you plan to "
                      f"sell the \"{b['alc']}\" version.", ""]
    (OUT / "image_prompts.md").write_text("\n".join(lines))


if __name__ == "__main__":
    write_products("matrixify_baskets_1of2.csv", BASKETS[:7])
    write_products("matrixify_baskets_2of2.csv", BASKETS[7:])
    write_collections()
    write_prompts()
    print("products:", len(BASKETS), "collections:", len(COLLECTIONS))
