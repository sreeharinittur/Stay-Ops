# Fernhill Stays Operations Dashboard

## Overview

This project analyzes booking performance for Fernhill Stays.

The solution includes:

- Data auditing and cleaning
- Property performance analysis
- Booking channel analysis
- Property health scoring
- Interactive dashboard

The dashboard is built using:

- Python
- Flask
- Streamlit
- Pandas
- Plotly

All analytics are generated from the cleaned dataset.

---

## Project Structure

backend/
│
├── app.py
├── metrics.py
├── clean.py
└── data/
└── bookings_cleaned.json

frontend/
│
└── dashboard.py

DECISIONS.md
AI-WORKFLOW.md
TEST-REPORT.md
README.md

---

## Setup

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run backend

cd backend

python app.py

API runs at:

http://localhost:5000

### 3. Run dashboard

cd frontend

streamlit run dashboard.py

Dashboard runs at:

http://localhost:8501

---

## Dashboard Features

### Property Performance

- Revenue by property
- Booking counts
- Property ranking

### Channel Analysis

- Revenue by channel
- Booking distribution
- Channel effectiveness

### Health Score

Composite metric based on:

- Revenue Performance (40%)
- Booking Completion Rate (30%)
- Cancellation Quality (20%)
- Channel Diversity (10%)

### Data Audit

Summary of cleaning issues identified and corrected.

---

## Documentation

See:

- DECISIONS.md
- AI-WORKFLOW.md
- TEST-REPORT.md
