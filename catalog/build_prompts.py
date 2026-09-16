#!/usr/bin/env python3
"""Build ChatGPT image prompts from the real basket recipes.

Reads 'Night Shift Master Bundles' in nightshift_MASTER_bundles.xlsx, so the
photo shows exactly what the SumTracker recipe packs. Rerun after any recipe
change:  python3 catalog/build_prompts.py
"""
import pathlib, collections, openpyxl

HERE = pathlib.Path(__file__).resolve().parent
WB = HERE / "nightshift_MASTER_bundles.xlsx"

# How each component should LOOK in the photo, keyed by SKU and quantity.
# Brand names stay out of the prompt text: image models garble label text and
# we do not want other companies' logos generated. Upload real photos instead.
LOOK = {
    ("AL-302", 1): "a dark green sparkling bottle with a gold foil neck",
    ("ACC-NS-FLUTE", 1): "a clear champagne flute",
    ("FD-041", 1): "a dark chocolate bar in a dark brown wrapper",
    ("ACC-NS-MASK", 1): "a folded champagne-colored silk sleep mask",
    ("SA-003", 1): "a coiled black stroller safety wrist leash with a metal clip",
    ("ACC-201", 1): "a round pink rose bath bomb",
    ("ACC-203", 1): "a flat foil sheet face-mask packet",
    ("FD-034", 2): "two small clear boxes of three gold-foil-wrapped hazelnut chocolates",
    ("ACC-NS-SOCKS", 1): "a pair of folded cream knit socks",
    ("ACC-SPA-04", 1): "a lavender soy candle in a lidded glass jar",
    ("ACC-NS-ROBE", 1): "a neatly folded soft white waffle robe",
    ("ACC-NS-LIPBALM", 1): "a lip balm tube",
    ("ACC-NS-DRYSHAMPOO", 1): "a slim dry shampoo can",
    ("ACC-NS-TUMBLER", 1): "an insulated tumbler with a straw lid",
    ("FD-119", 1): "a small bag of sea salt almonds",
    ("FD-071", 2): "two individually wrapped chocolate-dipped biscotti",
    ("FD-077", 1): "a bag of gourmet popcorn",
    ("FD-NS-LACTATION", 1): "a pouch of soft-baked cookies",
    ("ACC-NS-NIGHTLIGHT", 1): "a small round portable night-light glowing warm amber",
    ("SA-002", 1): "a pair of black stroller clips with carabiners",
    ("ACC-NS-BELLYBUTTER", 1): "a jar of belly butter",
    ("MXR-NS-MOCKTAIL", 1): "a zero-proof mocktail kit: a small bottle of mixer and a tin of dried citrus garnish",
    ("SA-005", 1): "a black crossbody stroller organizer bag with mesh side pockets",
    ("FD-026", 1): "a bag of beef jerky",
    ("FD-026", 2): "two bags of beef jerky",
    ("MXR-NS-ROOTBEER", 2): "two brown glass bottles of craft root beer",
    ("TA-001", 1): "a black nylon car seat travel strap with metal buckles",
    ("FD-086", 1): "a bag of whole-bean coffee",
    ("ACC-025", 1): "a heavy clear rocks glass",
    ("FD-005", 1): "a bag of ground coffee",
    ("FD-081", 2): "two snack packs of pretzels",
    ("ACC-033", 2): "two stemmed wine glasses",
    ("FD-062", 1): "a small bag of dark-chocolate-covered blueberries",
    ("FD-065", 1): "a small bag of chocolate toffee caramels",
    ("ACC-GAME-CARDS", 1): "a small boxed card game",
    ("ACC-MUG-PAIR", 1): "two matching cream ceramic mugs",
    ("1010", 1): "a stacked set of two black silicone suction baby plates",
    ("2000", 1): "a black silicone toddler cup with two handles",
    ("ACC-NS-BIBS", 1): "two folded baby bibs",
    ("ACC-NS-BOARDBOOK", 1): "a small baby board book with a blank cover",
    ("WINE-013", 1): "a sparkling wine bottle with gold foil",
    ("WINE-001", 1): "a bottle of red wine",
    ("ACC-034", 1): "a waiter's corkscrew",
    ("BEER-TBD", 2): "two brown craft beer bottles",
    ("AL-TBD-WHISKEY", 1): "a small bottle of whiskey",
}
LIL_MIL = {"SA-003", "SA-002", "SA-005", "TA-001", "2000", "1010"}

STYLE = (
    "Square 1:1 product photo, 2048x2048, overhead three-quarter angle. {box} with its deep "
    "midnight-blue (#1F2A44) lid leaning against the side, lamplight-gold (#E8B45A) tissue "
    "paper and gold crinkle-cut paper shred inside. Seamless warm cream (#FAF5EA) background. "
    "Soft warm light from one side like a bedside lamp at night, gentle shadows. A small card "
    "tucked in the tissue with a simple crescent moon icon and no other text. Every item clearly "
    "visible, not overlapping, arranged neatly in and just in front of the box. Clean, premium, "
    "cozy. No people, no hands. No readable text, brand names or logos on any item; keep labels "
    "plain. No watermark."
)


def load():
    ws = openpyxl.load_workbook(WB, data_only=True)["Night Shift Master Bundles"]
    recipes = collections.OrderedDict()
    for name, psku, variant, cname, csku, qty, *_ in ws.iter_rows(min_row=2, values_only=True):
        if not psku:
            continue
        recipes.setdefault(psku, {"name": name, "variant": variant, "rows": []})["rows"].append((str(csku), int(qty), cname))
    return recipes


def scene(rows):
    items, refs, large = [], [], False
    for sku, qty, cname in rows:
        if sku.startswith("PKG"):
            large = large or sku == "PKG-NS-BOX-L"
            continue
        look = LOOK.get((sku, qty))
        if not look:
            raise SystemExit(f"No LOOK entry for {sku} x{qty} — add one to build_prompts.py")
        items.append(look)
        if sku in LIL_MIL:
            refs.append(f"{cname} (Lil & Mil, {sku})")
        elif "-NS-" not in sku and "TBD" not in sku:
            refs.append(f"{cname} ({sku})")
    box = "A large kraft gift box" if large else "A kraft gift box"
    listing = ", ".join(items[:-1]) + ", and " + items[-1] if len(items) > 1 else items[0]
    return listing, refs, box


def main():
    r = load()
    out = ["# Night Shift Gift Co. — ChatGPT image prompts", "",
           "Generated from `nightshift_MASTER_bundles.xlsx`, so each photo shows what the recipe actually packs. "
           "Rerun `python3 catalog/build_prompts.py` after changing a recipe.", "",
           "## How to use", "",
           "1. New ChatGPT chat per basket so the style doesn't drift.",
           "2. **Upload the reference photos listed under each basket first**, then say: "
           "*\"Match the shape, color and packaging of these products, but keep their labels plain.\"* "
           "Lil & Mil photos matter most — the bag, leash, clips and belt must look exactly like what ships.",
           "3. Paste the prompt. Revise in plain words (\"bag more to the front\", \"less shred\").",
           "4. Save as `<handle>.png` and add it to the product, or send the files and I'll attach them.",
           "5. Items marked *not sourced yet* are placeholders — regenerate once you pick the real product.", ""]
    handles = {}
    import csv
    for f in sorted(HERE.glob("matrixify_baskets_*.csv")):
        for row in csv.DictReader(open(f, encoding="utf-8")):
            if row["Variant SKU"]:
                handles[row["Variant SKU"]] = row["Handle"]
    for psku, rec in r.items():
        listing, refs, box = scene(rec["rows"])
        short = rec["name"].split(" — ")[0]
        alc = psku.endswith("-ALC")
        heading = f"{rec['name']}" + (f" — {rec['variant']} version" if alc else "")
        new = [c for s, q, c in rec["rows"] if "-NS-" in s and not s.startswith("PKG")] + \
              [c for s, q, c in rec["rows"] if "TBD" in s]
        out += [("### " if alc else "## ") + heading, "",
                f"Handle: `{handles.get(psku, handles.get(psku.replace('-ALC', ''), '?'))}`  ·  SKU `{psku}`", ""]
        if alc:
            out += ["*Only make this image if you'll sell the alcohol version. Use it as the variant image.*", ""]
        out += ["**Reference photos to upload:** " + ("; ".join(refs) if refs else "none"), ""]
        if new:
            out += ["**Not sourced yet:** " + "; ".join(new), ""]
        out += ["```", f"Gift basket product photo for \"{short}\". In the box: {listing}. " + STYLE.format(box=box), "```", ""]
    (HERE / "image_prompts.md").write_text("\n".join(out))
    print("prompts:", len(r))


if __name__ == "__main__":
    main()
