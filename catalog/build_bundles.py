#!/usr/bin/env python3
"""Build nightshift_MASTER_bundles.xlsx from recipes.json.

recipes.json is the source of truth for what goes in every basket.
Edit it, then run:
    python3 catalog/build_bundles.py
    python3 catalog/build_prompts.py
and recalculate the workbook (open it in Excel/Sheets, or LibreOffice recalc).

Unit costs for components without a known cost are typed into the yellow
cells on the New Components tab of the generated workbook. If you have filled
some in, copy them into recipes.json ("cost") before regenerating, or they
will be lost.
"""
import json, pathlib, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

HERE = pathlib.Path(__file__).resolve().parent
recipes = json.loads((HERE / "recipes.json").read_text())

F = Font(name="Arial", size=10)
BLUE = Font(name="Arial", size=10, color="0000FF")
YEL = PatternFill("solid", fgColor="FFFF00")
HEAD = PatternFill("solid", fgColor="1F2A44")
HF = Font(name="Arial", size=10, bold=True, color="FFFFFF")


def header(ws, cols, widths):
    ws.append(cols)
    for i, c in enumerate(ws[1], 1):
        c.font, c.fill = HF, HEAD
        ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
    ws.freeze_panes = "A2"


wb = openpyxl.Workbook()

# ── Read Me ──────────────────────────────────────────────────────────────
rm = wb.active
rm.title = "Read Me"
for line in [
    "Night Shift Gift Co. — Master Bundles (same layout as bounty_MASTER_bundles)",
    "",
    "Packaging: white box + white fill for mom, baby, shower and couples baskets. Black box + black fill for the dad baskets (NS-006, NS-007, NS-008).",
    "",
    "Tabs",
    "  Night Shift Master Bundles — one row per component per basket. Unit cost pulls from New Components when blank.",
    "  SumTracker Upload — Parent sku, component_sku, quantity. Upload once every NEW / Confirm SKU item exists in SumTracker.",
    "  New Components — SKUs to create or confirm. Fill the yellow Unit Cost column; costs flow into every basket.",
    "  Price Worksheet — cost roll-up per basket. Fill the yellow Target Margin and Your Price cells.",
    "  Open Flags — decisions needed before upload.",
    "",
    "Colors: yellow = you fill in. Blue = hardcoded cost (Bounty master sheet, BroBasket cost sheet, or Shopify variant cost). Black = formula.",
    "Generated from catalog/recipes.json by catalog/build_bundles.py.",
]:
    rm.append([line])
for r in rm.iter_rows():
    for c in r:
        c.font = F
rm["A1"].font = Font(name="Arial", size=12, bold=True)
rm.column_dimensions["A"].width = 130

# ── New Components ───────────────────────────────────────────────────────
nc = wb.create_sheet("New Components")
header(nc, ["component_sku", "Component Name", "Status", "Used in (parent skus)", "Unit Cost ($)", "Notes"], [22, 42, 30, 60, 14, 50])
needed = {}
for r in recipes:
    for it in r["items"]:
        if it["cost"] is None:
            needed.setdefault(it["sku"], [it["name"], it["status"], set()])[2].add(r["sku"])
for sku, (name, status, used) in sorted(needed.items()):
    note = ""
    if status.startswith("Placeholder"):
        note = "Listed in the Bounty sheet but not in SumTracker"
    elif status == "Confirm SKU":
        note = "You stock this already — replace with the real SKU in recipes.json"
    nc.append([sku, name, status, ", ".join(sorted(used)), None, note])
    nc.cell(nc.max_row, 5).fill = YEL
    nc.cell(nc.max_row, 5).number_format = "$#,##0.00"
for row in nc.iter_rows(min_row=2):
    for c in row:
        c.font = F
nc_last = max(nc.max_row, 2)

# ── Master bundles ───────────────────────────────────────────────────────
mb = wb.create_sheet("Night Shift Master Bundles", 1)
header(mb, ["Parent Name", "Parent sku", "Variant", "Packaging", "Component Name", "component_sku", "quantity", "Unit Cost ($)", "Line Total ($)", "Status"],
       [46, 14, 20, 16, 48, 20, 9, 13, 13, 30])
NCR = f"'New Components'!$E$2:$E${nc_last}"
NCK = f"'New Components'!$A$2:$A${nc_last}"
for r in recipes:
    pack = f"{r['packaging']} {'large' if r['large_box'] else 'small'}"
    for it in r["items"]:
        mb.append([r["name"], r["sku"], r["variant"], pack, it["name"], it["sku"], it["qty"], None, None, it["status"]])
        n = mb.max_row
        for c in mb[n]:
            c.font = F
        mb.cell(n, 7).font = BLUE
        if it["cost"] is None:
            mb.cell(n, 8).value = (f'=IFERROR(IF(INDEX({NCR},MATCH(F{n},{NCK},0))="","",'
                                   f'INDEX({NCR},MATCH(F{n},{NCK},0))),"")')
        else:
            mb.cell(n, 8).value = float(it["cost"])
            mb.cell(n, 8).font = BLUE
        mb.cell(n, 9).value = f'=IF(H{n}="","",G{n}*H{n})'
        mb.cell(n, 8).number_format = mb.cell(n, 9).number_format = "$#,##0.00"
mb_last = mb.max_row

# ── SumTracker upload ────────────────────────────────────────────────────
st = wb.create_sheet("SumTracker Upload", 2)
header(st, ["Parent sku", "component_sku", "quantity"], [16, 22, 10])
for r in recipes:
    for it in r["items"]:
        st.append([r["sku"], it["sku"], it["qty"]])
for row in st.iter_rows(min_row=2):
    for c in row:
        c.font = F

# ── Price worksheet ──────────────────────────────────────────────────────
pw = wb.create_sheet("Price Worksheet", 3)
header(pw, ["Parent sku", "Parent Name", "Variant", "Known Cost ($)", "Components Missing Cost", "Target Margin", "Suggested Price ($)", "Your Price ($)", "Margin at Your Price"],
       [14, 46, 20, 14, 12, 13, 16, 14, 16])
MB = "'Night Shift Master Bundles'"
for r in recipes:
    pw.append([r["sku"], r["name"], r["variant"]])
    n = pw.max_row
    pw.cell(n, 4).value = f"=SUMIFS({MB}!$I$2:$I${mb_last},{MB}!$B$2:$B${mb_last},A{n})"
    pw.cell(n, 5).value = f'=COUNTIFS({MB}!$B$2:$B${mb_last},A{n},{MB}!$H$2:$H${mb_last},"")'
    pw.cell(n, 6).value = 0.60
    pw.cell(n, 7).value = f'=IF(E{n}>0,"Fill costs first",IF(F{n}>=1,"",CEILING(D{n}/(1-F{n}),1)-0.05))'
    pw.cell(n, 9).value = f'=IF(OR(H{n}="",H{n}=0),"",(H{n}-D{n})/H{n})'
    for col in range(1, 10):
        pw.cell(n, col).font = F
    pw.cell(n, 6).font = BLUE
    pw.cell(n, 6).fill = pw.cell(n, 8).fill = YEL
    for col, fmt in ((4, "$#,##0.00"), (6, "0.0%"), (7, "$#,##0.00"), (8, "$#,##0.00"), (9, "0.0%")):
        pw.cell(n, col).number_format = fmt
pw.cell(1, 6).comment = Comment("Assumption: 60% product margin as a starting point. Change per basket.", "Claude")
pw.cell(1, 8).comment = Comment("Enter the retail price. Known cost excludes shipping, adult signature and payment fees.", "Claude")

# ── Open flags ───────────────────────────────────────────────────────────
fl = wb.create_sheet("Open Flags")
header(fl, ["Check", "Detail"], [36, 120])
for a, b in [
    ("Packaging SKUs to confirm", "Every basket uses PKG-059 Krinkle Cut Fill ($0.50) — one fill SKU regardless of color (James, Sep 16). Small black box = PKG-082. The large black box exists in SumTracker but its SKU was not in the Bounty or BroBasket sheets: placeholder PKG-BOX-BLACK-L until confirmed."),
    ("Box size", "White baskets use PKG-100 White Bounty Basket Box ($4.58). NS-003, NS-005 and NS-011 carry the Tot Tote or a robe — confirm PKG-100 fits or add a larger white box SKU. Dad baskets NS-006 and NS-008 need the large black box; NS-007 uses PKG-082 Small Black Box ($1.00)."),
    ("Couples baskets", "NS-009 Lights Out Date Night and NS-010 The Morning After are packed white. Switch them to black in recipes.json if you'd rather."),
    ("Lil & Mil SKUs in SumTracker", "SA-003, SA-002, SA-005, TA-001, 2000, 1010 must exist in SumTracker with correct stock before uploading recipes."),
    ("Alcohol variants (-ALC)", "Upload -ALC recipes only once it is decided which store sells alcohol baskets. BEER-TBD and AL-TBD-WHISKEY need real SKUs."),
    ("Zero-proof sparkling", "AL-302 Fre Sparkling Brut Alcohol Removed ($9.00) in NS-001 and NS-009."),
    ("Pregnancy-safe items (NS-005)", "ACC-203 face mask is in the Mom-to-Be box — confirm it is suitable in pregnancy."),
    ("Cup and plate colors", "Recipes use Black (2000 cup, 1010 plates). Only ~39 plate sets remain."),
    ("Bounty placeholders reused", "ACC-GAME-CARDS (NS-009) and ACC-MUG-PAIR (NS-010) are in the Bounty sheet but not in SumTracker."),
]:
    fl.append([a, b])
for row in fl.iter_rows(min_row=2):
    for c in row:
        c.font = F
        c.alignment = Alignment(wrap_text=True, vertical="top")

wb.save(HERE / "nightshift_MASTER_bundles.xlsx")
print(f"recipes {len(recipes)}, component rows {mb_last - 1}, to create/confirm {len(needed)}")
