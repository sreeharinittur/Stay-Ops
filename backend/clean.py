"""
clean.py — Fernhill Stays Booking Data Cleaner
Reads raw CSV, fixes all 9 known issues, writes bookings_cleaned.json

Run:
    python clean.py

Output:
    data/bookings_cleaned.json
    data/cleaning_log.txt
"""

import pandas as pd
import json
import math
import os
from dateutil import parser as dateparser

# ─────────────────────────────────────────────
# 0. LOAD
# ─────────────────────────────────────────────
RAW_PATH = "data/bookings_jan_may_2026.csv"
OUT_PATH  = "data/bookings_cleaned.json"

df = pd.read_csv(RAW_PATH)
original_count = len(df)
print(f"Loaded {original_count} rows\n")

issues_log = []

# ─────────────────────────────────────────────
# ISSUE 1 — Exact duplicate rows
# ─────────────────────────────────────────────
# 8 booking IDs appear twice with completely identical data.
# These are double-submissions by staff at the property level.
# Decision: drop exact duplicates, keep first occurrence.

before = len(df)
df = df.drop_duplicates()
dupes_removed = before - len(df)
issues_log.append(f"[Issue 1] Exact duplicate rows: removed {dupes_removed} (kept first occurrence)")
print(f"Issue 1 — Duplicates removed: {dupes_removed}")

# ─────────────────────────────────────────────
# ISSUE 2 — Inconsistent property names
# ─────────────────────────────────────────────
# Same property appears in different casing and with trailing spaces.
# e.g. "cedar court", "Cedar Court", "MARIGOLD SUITES", "Marigold Suites "
# Decision: strip whitespace, lowercase, map to 5 canonical names.

PROPERTY_MAP = {
    "marigold suites":    "Marigold Suites",
    "cedar court":        "Cedar Court",
    "lakeview residency": "Lakeview Residency",
    "palm grove inn":     "Palm Grove Inn",
    "birchwood stay":     "Birchwood Stay",
}

df["property"] = (
    df["property"]
    .str.strip()
    .str.lower()
    .map(PROPERTY_MAP)
)

unmapped = df["property"].isna().sum()
issues_log.append(
    f"[Issue 2] Property name variants (case/spaces) normalised to 5 canonical names. "
    f"Unmapped after fix: {unmapped}"
)
print(f"Issue 2 — Property names normalised. Unmapped: {unmapped}")

# ─────────────────────────────────────────────
# ISSUE 3 — Inconsistent status values
# ─────────────────────────────────────────────
# "CHECKED OUT", "Checked-out", "confirmed", "Confirmed" etc.
# Decision: lowercase → strip → map to 4 canonical statuses.

STATUS_MAP = {
    "checked-out": "Checked-out",
    "checked out": "Checked-out",
    "confirmed":   "Confirmed",
    "cancelled":   "Cancelled",
    "no-show":     "No-show",
}

df["status"] = (
    df["status"]
    .str.strip()
    .str.lower()
    .map(STATUS_MAP)
)

unmapped_status = df["status"].isna().sum()
issues_log.append(
    f"[Issue 3] Status variants normalised to 4 canonical values "
    f"(Checked-out, Confirmed, Cancelled, No-show). Unmapped: {unmapped_status}"
)
print(f"Issue 3 — Status normalised. Unmapped: {unmapped_status}")

# ─────────────────────────────────────────────
# ISSUE 4 — Inconsistent booking channel values + NULLs
# ─────────────────────────────────────────────
# "direct" vs "Direct", "ota-mmt" vs "OTA-MMT"
# 29 rows have no channel at all — staff left blank.
# Decision: normalise case; fill NaN as "Unknown".

CHANNEL_MAP = {
    "direct":      "Direct",
    "walk-in":     "Walk-in",
    "corporate":   "Corporate",
    "ota-mmt":     "OTA-MMT",
    "ota-booking": "OTA-Booking",
    "unknown":     "Unknown",
}

df["booking_channel"] = (
    df["booking_channel"]
    .fillna("unknown")
    .str.strip()
    .str.lower()
    .map(CHANNEL_MAP)
    .fillna("Unknown")
)

issues_log.append(
    "[Issue 4] Booking channel variants normalised; 29 blank values filled as 'Unknown'"
)
print("Issue 4 — Booking channels normalised")

# ─────────────────────────────────────────────
# ISSUE 5 — Inconsistent room type abbreviations
# ─────────────────────────────────────────────
# "Std" and "Standard" are the same. "DLX" and "Deluxe" are the same.
# Decision: map all abbreviations to full canonical names.

ROOM_MAP = {
    "std":      "Standard",
    "standard": "Standard",
    "dlx":      "Deluxe",
    "deluxe":   "Deluxe",
    "suite":    "Suite",
}

df["room_type"] = (
    df["room_type"]
    .str.strip()
    .str.lower()
    .map(ROOM_MAP)
)

unmapped_room = df["room_type"].isna().sum()
issues_log.append(
    f"[Issue 5] Room type abbreviations normalised (Std→Standard, DLX→Deluxe). "
    f"Unmapped: {unmapped_room}"
)
print(f"Issue 5 — Room types normalised. Unmapped: {unmapped_room}")

# ─────────────────────────────────────────────
# ISSUE 6 — Mixed date formats
# ─────────────────────────────────────────────
# Dates appear as "21/01/2026", "2026-03-18", "03-26-2026", "7 Mar 2026"
# Decision: parse with dateutil (handles all formats); dayfirst=True
# for DD/MM/YYYY ambiguous cases; output ISO YYYY-MM-DD.

def safe_parse_date(val):
    try:
        return dateparser.parse(str(val), dayfirst=True).strftime("%Y-%m-%d")
    except Exception:
        return None

df["check_in_date"] = df["check_in_date"].apply(safe_parse_date)

bad_dates = df["check_in_date"].isna().sum()
issues_log.append(
    f"[Issue 6] Mixed date formats (DD/MM/YYYY, YYYY-MM-DD, MM-DD-YYYY, 'D Mon YYYY') "
    f"all parsed to ISO YYYY-MM-DD using dateutil. Unparseable: {bad_dates}"
)
print(f"Issue 6 — Dates normalised. Unparseable: {bad_dates}")

# ─────────────────────────────────────────────
# ISSUE 7 — Negative total amounts
# ─────────────────────────────────────────────
# 5 rows have a negative total_amount_inr (e.g. -28497).
# nightly_rate and nights are both positive — this is a sign error.
# Decision: take absolute value. These are not refund records;
# there is no refund/credit_note status in the dataset.

neg_mask = df["total_amount_inr"] < 0
neg_count = neg_mask.sum()
df.loc[neg_mask, "total_amount_inr"] = df.loc[neg_mask, "total_amount_inr"].abs()

issues_log.append(
    f"[Issue 7] {neg_count} rows had negative total_amount_inr — "
    "sign error corrected (abs value taken). Rationale: rate and nights both positive."
)
print(f"Issue 7 — Negative amounts fixed: {neg_count}")

# ─────────────────────────────────────────────
# ISSUE 8 — total_amount ≠ nightly_rate × nights
# ─────────────────────────────────────────────
# After fixing negatives, some totals are still wrong.
# e.g. rate=2725, nights=3, total=81750 (should be 8175 — extra zero entered).
# Decision: recompute total_amount = rate × nights as ground truth.
# Only applies where nights > 0 and both rate and total exist.

mismatch_mask = (
    df["nightly_rate_inr"].notna() &
    df["total_amount_inr"].notna() &
    (df["nights"] > 0) &
    (abs(df["nightly_rate_inr"] * df["nights"] - df["total_amount_inr"]) > 1)
)
mismatch_count = mismatch_mask.sum()
df.loc[mismatch_mask, "total_amount_inr"] = (
    df.loc[mismatch_mask, "nightly_rate_inr"] * df.loc[mismatch_mask, "nights"]
)

issues_log.append(
    f"[Issue 8] {mismatch_count} rows: total_amount ≠ rate × nights — "
    "recomputed total as rate × nights (typos: extra zeros, off-by-10x entries)."
)
print(f"Issue 8 — Mismatched totals recomputed: {mismatch_count}")

# ─────────────────────────────────────────────
# ISSUE 9 — Zero-night bookings
# ─────────────────────────────────────────────
# 4 rows have nights=0, which is physically impossible.
# Two have valid rate and total → infer nights = round(total/rate).
# Two are Cancelled with total matching 1 night → treat as 1-night cancelled.
# Decision: infer where possible; exclude if nights still 0.

def fix_zero_nights(row):
    if row["nights"] == 0:
        rate = row["nightly_rate_inr"]
        total = row["total_amount_inr"]
        if rate and rate > 0 and total and total > 0:
            inferred = round(total / rate)
            if 1 <= inferred <= 30:
                return int(inferred)
        return 0
    return int(row["nights"])

df["nights"] = df.apply(fix_zero_nights, axis=1)

still_zero = (df["nights"] == 0).sum()
df = df[df["nights"] > 0].copy()

issues_log.append(
    f"[Issue 9] Zero-nights rows: nights inferred from total/rate where possible. "
    f"{still_zero} rows excluded (could not be reliably fixed)."
)
print(f"Issue 9 — Zero-nights remaining (excluded): {still_zero}")

# ─────────────────────────────────────────────
# DERIVED COLUMNS
# ─────────────────────────────────────────────
# is_revenue: only Checked-out = actual earned revenue.
# Cancelled / No-show / Confirmed must NOT count as revenue.

df["is_revenue"] = df["status"] == "Checked-out"

df["check_in_date"] = pd.to_datetime(df["check_in_date"])
df["month"]     = df["check_in_date"].dt.strftime("%b %Y")
df["month_num"] = df["check_in_date"].dt.to_period("M").astype(str)

# Restore check_in_date to string for JSON
df["check_in_date"] = df["check_in_date"].dt.strftime("%Y-%m-%d")

# Fill numeric NaNs with None so they serialise as null, not NaN
for col in ["nightly_rate_inr", "total_amount_inr"]:
    df[col] = df[col].where(df[col].notna(), other=None)

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"Original rows  : {original_count}")
print(f"Cleaned rows   : {len(df)}")
print(f"Rows removed   : {original_count - len(df)}")
print(f"\nStatus distribution:")
print(df["status"].value_counts())
print(f"\nProperty distribution:")
print(df["property"].value_counts())
print(f"\nRevenue-generating (Checked-out): {df['is_revenue'].sum()}")

# ─────────────────────────────────────────────
# WRITE OUTPUT — custom encoder so NaN → null
# ─────────────────────────────────────────────
class SafeEncoder(json.JSONEncoder):
    def default(self, obj):
        return super().default(obj)
    def iterencode(self, obj, _one_shot=False):
        # pandas None → null already; intercept float nan just in case
        return super().iterencode(obj, _one_shot)

def nan_to_none(obj):
    """Recursively replace float nan with None in dicts/lists."""
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, dict):
        return {k: nan_to_none(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [nan_to_none(v) for v in obj]
    return obj

os.makedirs("data", exist_ok=True)

records = df.to_dict(orient="records")
records = nan_to_none(records)

with open(OUT_PATH, "w") as f:
    json.dump(records, f, indent=2)

# Write issues log
with open("data/cleaning_log.txt", "w",encoding="utf-8") as f:
    f.write("DATA CLEANING ISSUES LOG — Fernhill Stays\n")
    f.write("=" * 50 + "\n\n")
    for line in issues_log:
        f.write(line + "\n\n")
    f.write(f"\nFinal: {original_count} → {len(df)} rows\n")

print(f"\n✓ Written: {OUT_PATH}")
print("✓ Written: data/cleaning_log.txt")