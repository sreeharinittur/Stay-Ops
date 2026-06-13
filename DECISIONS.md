# DECISIONS.md

# Fernhill Stays Dashboard – Key Decisions

## Objective

The objective of this project was to audit a booking dataset, correct data quality issues, and build a dashboard that helps management answer three questions:

1. How is each property performing?
2. Which booking channels are most valuable?
3. Which properties require management attention?

All dashboard metrics are calculated from the cleaned dataset rather than the raw source file.

---

# Data Quality Audit

Before building any analytics, I audited the dataset for issues that could distort reporting and business decisions.

## 1. Duplicate Records

### Issue

The dataset contained duplicate booking records.

### Decision

Removed exact duplicate rows.

### Rationale

Each booking should appear exactly once in the analytical dataset. Keeping duplicates would artificially inflate booking counts, revenue, and operational metrics.

---

## 2. Property Name Inconsistencies

### Issue

Property names appeared in multiple formats due to differences in capitalization and spacing.

Examples:

- cedar court
- Cedar Court
- CEDAR COURT

### Decision

Standardized property names into a canonical format.

### Rationale

Without normalization, the same property would be treated as multiple properties during aggregation.

---

## 3. Booking Status Inconsistencies

### Issue

Booking statuses were represented in multiple formats.

Examples:

- checked out
- Checked-Out
- CHECKED OUT

### Decision

Mapped statuses into a controlled set of standardized values.

### Rationale

Revenue and operational metrics depend heavily on booking status. Consistent values are necessary for reliable reporting.

---

## 4. Booking Channel Inconsistencies

### Issue

Booking channels contained inconsistent naming conventions.

### Decision

Normalized booking channel names.

### Rationale

Channel performance analysis requires consistent grouping of bookings by acquisition source.

---

## 5. Room Type Inconsistencies

### Issue

Room categories appeared in abbreviated and inconsistent forms.

### Decision

Mapped room types to standardized labels.

### Rationale

Although room-level analysis was not part of the final dashboard, maintaining consistent dimensions improves overall data quality and future extensibility.

---

## 6. Mixed Date Formats

### Issue

Date fields used multiple formats.

### Decision

Converted all date values into a consistent format and parsed them into datetime objects.

### Rationale

Reliable date handling is required for stay-duration calculations and trend analysis.

---

## 7. Negative Booking Totals

### Issue

Some bookings contained negative total amounts.

### Decision

Flagged these as invalid and recalculated totals using available booking information where possible.

### Rationale

Negative revenue values would distort property and channel performance metrics.

---

## 8. Incorrect Booking Totals

### Issue

Some booking totals were inconsistent with nightly rate and stay duration.

### Decision

Recalculated totals using available booking attributes.

### Rationale

Derived totals were more reliable than inconsistent source values.

---

## 9. Invalid Stay Durations

### Issue

Some records resulted in zero-night stays or invalid durations.

### Decision

Where sufficient information existed, stay duration was inferred. Records that could not be corrected confidently were excluded.

### Rationale

Invalid durations affect occupancy-related calculations and revenue validation.

---

# Revenue Recognition Decision

## Problem

Not every booking represents realized revenue.

The dataset contained statuses such as:

- Confirmed
- Cancelled
- No-show
- Checked-out

## Decision

Only bookings with status = "Checked-out" are considered revenue-generating bookings.

## Rationale

Revenue should represent completed stays rather than reservations. Including cancelled or no-show bookings would overstate business performance.

---

# Health Score Definition

The client requested a property health score but did not define one.

I created a composite metric intended to summarize operational performance on a 0–100 scale.

## Formula

Health Score =

40% Revenue Performance

30% Booking Completion Rate

20% Cancellation Quality

10% Channel Diversity

---

## Revenue Performance (40%)

Measures revenue generated relative to the best-performing property.

### Why included?

Revenue remains the strongest indicator of business performance.

### Why not 100%?

Revenue alone can hide operational weaknesses such as high cancellation rates.

---

## Booking Completion Rate (30%)

Measures the percentage of bookings that result in completed stays.

### Why included?

A healthy property should consistently convert reservations into realized stays.

---

## Cancellation Quality (20%)

Measures resistance to cancellations.

### Why included?

High cancellation rates reduce realized revenue and create operational inefficiencies.

---

## Channel Diversity (10%)

Measures reliance on booking channels.

### Why included?

Properties dependent on a single channel face concentration risk.

A diversified channel mix is generally more resilient.

---

# What the Health Score Deliberately Excludes

The following factors were not included because the dataset does not contain sufficient information:

- Occupancy percentage
- Room inventory
- Profitability
- Operating expenses
- Guest review scores
- Customer satisfaction
- Competitive benchmarking

Including these metrics would require unsupported assumptions.

---

# Weaknesses of the Health Score

1. Revenue is not the same as profit.
2. The weighting scheme is subjective.
3. Occupancy cannot be measured accurately without room inventory data.
4. Guest experience is not represented because review data is unavailable.
5. Properties with intentionally concentrated channel strategies may score lower on diversity.

The score should therefore be treated as a decision-support metric rather than a definitive measure of business quality.

---

# Assumptions

The following assumptions were made during cleaning and analysis:

1. Checked-out bookings represent realized revenue.
2. Duplicate rows are accidental duplicates rather than intentional records.
3. Standardized property names refer to the same physical property.
4. Recalculated totals are more reliable than inconsistent source totals.
5. Date parsing after normalization correctly represents booking dates.

---

# What I Would Do Next With More Time

Given additional time and richer data, I would extend the solution with:

- Occupancy analysis
- ADR (Average Daily Rate)
- RevPAR
- Revenue forecasting
- Booking lead-time analysis
- Guest satisfaction analysis
- Property benchmarking
- Automated anomaly detection

These additions would provide a more complete view of operational and financial performance.
