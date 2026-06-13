# Fernhill Stays Operations Dashboard

## Live Deployment

### Dashboard (Streamlit)

https://stay-ops-dashboard.streamlit.app/

### Analytics API (Render)

https://stay-ops.onrender.com/

Sample endpoint:

https://stay-ops.onrender.com/summary

---

# Project Overview

The Fernhill Stays Operations Dashboard is an analytics solution designed to evaluate booking performance, channel effectiveness, operational health, and revenue trends across multiple properties.

The project demonstrates an end-to-end analytics workflow:

* Raw data auditing
* Data cleaning and standardization
* Business metric generation
* API development
* Interactive dashboard development
* Testing and validation
* Deployment to cloud platforms

---

# Business Objectives

The solution was built to answer key operational questions:

1. Which properties generate the highest revenue?
2. Which booking channels perform best?
3. What is the cancellation impact on operations?
4. How healthy is each property overall?
5. What operational insights can support business decisions?

---

# Technology Stack

### Backend

* Python
* Flask
* Pandas
* NumPy
* Gunicorn

### Frontend

* Streamlit
* Plotly

### Deployment

* Render (Backend API)
* Streamlit Community Cloud (Dashboard)

---

# Project Structure

```text
backend/
│
├── app.py
├── metrics.py
├── clean.py
├── requirements.txt
└── data/
    ├── bookings_jan_may_2026.csv
    ├── bookings_cleaned.json
    └── cleaning_log.txt

frontend/
│
└── dashboard.py

README.md
DECISIONS.md
AI-WORKFLOW.md
TEST-REPORT.md
requirements.txt
```

---

# Data Processing Workflow

## 1. Data Audit

The raw dataset was inspected for:

* Missing values
* Invalid booking records
* Revenue inconsistencies
* Duplicate entries
* Data type issues

---

## 2. Data Cleaning

The cleaning pipeline performs:

* Null value handling
* Data standardization
* Revenue validation
* Booking status normalization
* Export of cleaned dataset

Output:

```text
backend/data/bookings_cleaned.json
```

---

## 3. Metrics Generation

Business metrics are calculated for:

### Property Performance

* Total Revenue
* Booking Volume
* Average Revenue per Booking

### Channel Performance

* Revenue by Channel
* Booking Distribution
* Channel Effectiveness

### Operational Metrics

* Completion Rate
* Cancellation Rate
* Revenue Contribution

---

# Property Health Score

A composite score was designed to evaluate overall property performance.

| Component            | Weight |
| -------------------- | ------ |
| Revenue Performance  | 40%    |
| Completion Rate      | 30%    |
| Cancellation Quality | 20%    |
| Channel Diversity    | 10%    |

The score is normalized to enable comparison across all properties.

---

# Dashboard Features

## Executive Summary

* Total Revenue
* Total Bookings
* Completion Metrics
* Cancellation Insights

## Property Performance

* Revenue Ranking
* Booking Counts
* Property Comparison

## Channel Analysis

* Revenue by Channel
* Booking Distribution
* Channel Contribution

## Property Health Scores

* Health Score Ranking
* Operational Performance Comparison

---

# API Endpoints

### Summary Metrics

```http
GET /summary
```

Returns overall booking and revenue statistics.

---

### Property Metrics

```http
GET /properties
```

Returns property-level performance metrics.

---

### Channel Metrics

```http
GET /channels
```

Returns booking channel analytics.

---

### Health Scores

```http
GET /health
```

Returns calculated health scores for all properties.

---

# Testing

Validation was performed for:

* Data cleaning correctness
* Revenue calculations
* Aggregation accuracy
* API response structure
* Dashboard rendering
* Edge case handling

Detailed testing evidence is available in:

```text
TEST-REPORT.md
```

---

# AI-Assisted Development

AI tools were used to accelerate:

* Code generation
* Refactoring
* Documentation drafting
* Validation support

The complete workflow is documented in:

```text
AI-WORKFLOW.md
```

---

# Key Design Decisions

Important implementation and architectural decisions are documented in:

```text
DECISIONS.md
```

---

# Local Setup

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Backend

```bash
cd backend
python app.py
```

Backend:

```text
http://localhost:5000
```

## Run Dashboard

```bash
cd frontend
streamlit run dashboard.py
```

Dashboard:

```text
http://localhost:8501
```

---

# Author

Shrihari A M


