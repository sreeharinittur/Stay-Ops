# AI-WORKFLOW.md

# AI-Assisted Development Workflow

## Overview

AI tools were used as development assistants throughout the project. Their role was to accelerate implementation, generate alternative approaches, review logic, and improve documentation.

All outputs were reviewed manually before being incorporated into the final solution.

---

# AI Tools Used

## ChatGPT

Used for:

- Reviewing cleaning logic
- Designing Flask API endpoints
- Structuring Streamlit dashboard components
- Discussing health score alternatives
- Generating documentation drafts
- Reviewing project architecture

---

## Claude

Used for:

- UI refinement ideas
- Streamlit layout improvements
- Dashboard presentation improvements
- Improving visual hierarchy and readability

---

# Prompts That Influenced The Project

## Prompt 1

> Review my data-cleaning approach and identify hidden assumptions or edge cases that could affect reporting accuracy.

### Outcome

This helped identify several areas requiring explicit documentation, including:

- Revenue recognition assumptions
- Handling of invalid booking totals
- Treatment of cancelled bookings
- Risks associated with mixed date formats

---

## Prompt 2

> Design a property health score using only the fields available in this dataset. Explain the trade-offs of each component.

### Outcome

Several candidate metrics were explored.

The final health score incorporated:

- Revenue Performance
- Booking Completion Rate
- Cancellation Quality
- Channel Diversity

This process helped balance financial and operational performance rather than relying solely on revenue.

---

## Prompt 3

> Suggest a minimal architecture for a hotel operations dashboard using Flask and Streamlit.

### Outcome

This led to the final architecture:

Raw Dataset

→ Cleaning Pipeline

→ Cleaned JSON Dataset

→ Flask API

→ Streamlit Dashboard

Separating cleaning, business logic, and presentation made the solution easier to maintain and test.

---

# Example Of An AI Suggestion That Was Rejected

## Initial Suggestion

An AI-generated proposal recommended ranking properties using revenue alone.

### Why It Was Incorrect

Revenue does not fully capture operational health.

For example:

Property A may generate high revenue while experiencing significant cancellations.

Property B may generate slightly lower revenue but have a much stronger booking completion rate.

A revenue-only ranking would incorrectly treat Property A as healthier.

### How I Identified The Problem

I compared the proposed metric against the client's business question:

> "Which properties need attention?"

A revenue-only score would fail to identify operational issues.

### Correction

The final health score became a weighted composite metric incorporating:

- Revenue Performance
- Booking Completion Rate
- Cancellation Quality
- Channel Diversity

This better reflects overall property health.

---

# Example Of Manual Validation

AI-generated cleaning recommendations were not accepted automatically.

For each cleaning rule:

1. The issue was verified in the dataset.
2. The business impact was evaluated.
3. The correction method was reviewed manually.
4. Results were checked after cleaning.

Examples included:

- Duplicate removal
- Property normalization
- Booking status normalization
- Invalid total corrections

---

# Lessons Learned

AI significantly accelerated implementation and documentation, but successful use required continuous verification.

The most valuable contributions were:

- Architectural suggestions
- Alternative metric definitions
- Documentation support

The most important human responsibilities remained:

- Defining business logic
- Validating assumptions
- Evaluating trade-offs
- Ensuring analytical correctness

The final decisions, assumptions, and metric definitions were made manually after reviewing AI-generated suggestions.
