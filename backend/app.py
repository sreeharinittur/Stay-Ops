from flask import Flask, jsonify
import pandas as pd

from metrics import (
    property_metrics,
    channel_metrics,
    health_scores,
    dashboard_summary
)

app = Flask(__name__)

# --------------------------------------------------
# LOAD CLEANED DATA
# --------------------------------------------------

df = pd.read_json(
    "data/bookings_cleaned.json"
)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

@app.route("/summary")
def summary():

    return jsonify(
        dashboard_summary(df)
    )

# --------------------------------------------------
# PROPERTY PERFORMANCE
# --------------------------------------------------

@app.route("/properties")
def properties():

    return jsonify(
        property_metrics(df)
        .to_dict(
            orient="records"
        )
    )

# --------------------------------------------------
# CHANNEL ANALYSIS
# --------------------------------------------------

@app.route("/channels")
def channels():

    return jsonify(
        channel_metrics(df)
        .to_dict(
            orient="records"
        )
    )

# --------------------------------------------------
# HEALTH SCORES
# --------------------------------------------------

@app.route("/health")
def health():

    return jsonify(
        health_scores(df)
        .to_dict(
            orient="records"
        )
    )

# --------------------------------------------------
# MONTHLY TREND
# --------------------------------------------------

@app.route("/monthly")
def monthly():

    revenue_df = df[
        df["is_revenue"] == True
    ].copy()

    monthly_data = (
        revenue_df
        .groupby("month_num")
        .agg(
            revenue=("total_amount_inr", "sum"),
            bookings=("booking_id", "count")
        )
        .reset_index()
        .sort_values("month_num")
    )

    return jsonify(
        monthly_data.to_dict(
            orient="records"
        )
    )

# --------------------------------------------------
# DATA QUALITY INFO
# --------------------------------------------------

@app.route("/audit")
def audit():

    audit_data = {
        "issues_found": 9,
        "duplicates_removed": True,
        "negative_amounts_fixed": True,
        "mixed_dates_normalized": True,
        "room_types_standardized": True,
        "channels_standardized": True
    }

    return jsonify(audit_data)

# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )