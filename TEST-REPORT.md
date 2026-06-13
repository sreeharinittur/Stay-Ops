# TEST-REPORT.md

# Test Report

## Objective

The objective of testing was to verify that:

1. Data cleaning rules were applied correctly.
2. Business metrics were calculated from cleaned data.
3. API endpoints returned expected results.
4. Dashboard visualizations displayed correct information.

---

# Part 1: Data Cleaning Validation

## Test 1 — Duplicate Record Removal

### Expected Result

Duplicate bookings should appear only once in the cleaned dataset.

### Validation

Compared row counts before and after cleaning and verified duplicate removal logic.

### Result

PASS

---

## Test 2 — Property Name Standardization

### Expected Result

Property names should be represented consistently.

Examples:

- cedar court
- Cedar Court
- CEDAR COURT

should become a single value.

### Validation

Reviewed unique property values after cleaning.

### Result

PASS

---

## Test 3 — Booking Status Standardization

### Expected Result

Booking statuses should be normalized into a controlled set.

### Validation

Reviewed unique status values after cleaning.

### Result

PASS

---

## Test 4 — Channel Standardization

### Expected Result

Booking channels should use consistent naming.

### Validation

Reviewed unique channel values after cleaning.

### Result

PASS

---

## Test 5 — Date Parsing

### Expected Result

Date fields should be converted into valid datetime values.

### Validation

Verified successful parsing and stay-duration calculations.

### Result

PASS

---

## Test 6 — Negative Revenue Values

### Expected Result

Negative booking totals should not remain in the analytical dataset.

### Validation

Checked cleaned dataset for remaining negative values.

### Result

PASS

---

## Test 7 — Invalid Booking Totals

### Expected Result

Totals should align with stay duration and nightly rate.

### Validation

Reviewed corrected records after recalculation.

### Result

PASS

---

## Test 8 — Invalid Stay Durations

### Expected Result

Zero-night and invalid stays should be corrected or excluded.

### Validation

Reviewed stay-duration calculations after cleaning.

### Result

PASS

---

# Part 2: Metric Validation

## Test 9 — Revenue Calculation

### Expected Result

Revenue should include only completed stays.

### Validation

Confirmed that only bookings with status = "Checked-out" contribute to revenue metrics.

### Result

PASS

---

## Test 10 — Property Aggregation

### Expected Result

Property-level revenue and booking counts should match grouped data.

### Validation

Manually compared sample calculations against dashboard output.

### Result

PASS

---

## Test 11 — Channel Aggregation

### Expected Result

Channel metrics should match grouped booking data.

### Validation

Verified booking and revenue totals by channel.

### Result

PASS

---

## Test 12 — Health Score Ranking

### Expected Result

Properties should be ranked in descending health score order.

### Validation

Reviewed calculated scores and ranking output.

### Result

PASS

---

# Part 3: API Testing

The Flask API was tested using a browser and direct endpoint requests.

| Endpoint    | Purpose                      | Result |
| ----------- | ---------------------------- | ------ |
| /summary    | Dashboard KPIs               | PASS   |
| /properties | Property performance metrics | PASS   |
| /channels   | Channel metrics              | PASS   |
| /health     | Health score rankings        | PASS   |
| /monthly    | Revenue trend data           | PASS   |
| /audit      | Data quality summary         | PASS   |

---

# Part 4: Dashboard Testing

## Dashboard Startup

### Expected Result

Dashboard loads successfully when API is running.

### Result

PASS

---

## Property Filter

### Expected Result

Selecting a property updates visualizations and tables.

### Result

PASS

---

## Property Performance Charts

### Expected Result

Revenue and booking charts display correctly.

### Result

PASS

---

## Channel Analysis Charts

### Expected Result

Channel contribution and booking charts render correctly.

### Result

PASS

---

## Health Score Dashboard

### Expected Result

Leaderboard and rankings display correctly.

### Result

PASS

---

## Data Audit Tab

### Expected Result

Audit information displays successfully.

### Result

PASS

---

# Known Limitations

1. Health Score weights are based on business judgment and may be adjusted depending on management priorities.
2. Occupancy metrics cannot be calculated because room inventory data is unavailable.
3. Profitability cannot be measured because operating cost data is unavailable.
4. Customer satisfaction metrics cannot be included because review data is unavailable.

---

# Conclusion

Testing confirmed that:

- Data cleaning rules were applied successfully.
- Metrics were calculated from the cleaned dataset.
- API endpoints returned expected outputs.
- Dashboard functionality operated as intended.

No critical issues remained at the time of submission.
