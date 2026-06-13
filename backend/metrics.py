import pandas as pd


def revenue_df(df):
    """
    Revenue only comes from Checked-out bookings.
    """

    return df[df["is_revenue"] == True].copy()


# --------------------------------------------------
# PROPERTY PERFORMANCE
# --------------------------------------------------

def property_metrics(df):

    revenue = revenue_df(df)

    property_stats = (
        revenue.groupby("property")
        .agg(
            revenue=("total_amount_inr", "sum"),
            bookings=("booking_id", "count")
        )
        .reset_index()
    )

    total_bookings = (
        df.groupby("property")["booking_id"]
        .count()
        .reset_index(name="total_bookings")
    )

    cancelled = (
        df[df["status"] == "Cancelled"]
        .groupby("property")["booking_id"]
        .count()
        .reset_index(name="cancelled")
    )

    result = property_stats.merge(
        total_bookings,
        on="property",
        how="left"
    )

    result = result.merge(
        cancelled,
        on="property",
        how="left"
    )

    result["cancelled"] = result["cancelled"].fillna(0)

    result["cancellation_rate"] = (
        result["cancelled"]
        / result["total_bookings"]
        * 100
    ).round(2)

    return result.sort_values(
        "revenue",
        ascending=False
    )


# --------------------------------------------------
# CHANNEL ANALYSIS
# --------------------------------------------------

def channel_metrics(df):

    revenue = revenue_df(df)

    revenue_by_channel = (
        revenue.groupby("booking_channel")
        .agg(
            revenue=("total_amount_inr", "sum"),
            bookings=("booking_id", "count")
        )
        .reset_index()
    )

    return revenue_by_channel.sort_values(
        "revenue",
        ascending=False
    )


# --------------------------------------------------
# HEALTH SCORE
# --------------------------------------------------

def health_scores(df):

    revenue = revenue_df(df)

    property_revenue = (
        revenue.groupby("property")
        ["total_amount_inr"]
        .sum()
    )

    max_revenue = property_revenue.max()

    results = []

    for property_name in df["property"].unique():

        prop_df = df[
            df["property"] == property_name
        ]

        revenue_value = property_revenue.get(
            property_name,
            0
        )

        revenue_score = (
            revenue_value / max_revenue
            if max_revenue > 0 else 0
        )

        total = len(prop_df)

        checked_out = len(
            prop_df[
                prop_df["status"]
                == "Checked-out"
            ]
        )

        cancelled = len(
            prop_df[
                prop_df["status"]
                == "Cancelled"
            ]
        )

        occupancy_score = (
            checked_out / total
            if total > 0 else 0
        )

        cancellation_score = (
            1 - (cancelled / total)
            if total > 0 else 0
        )

        diversity_score = (
            prop_df["booking_channel"]
            .nunique()
            /
            df["booking_channel"]
            .nunique()
        )

        health = (
            revenue_score * 0.40
            + occupancy_score * 0.30
            + cancellation_score * 0.20
            + diversity_score * 0.10
        ) * 100

        results.append({
            "property": property_name,
            "health_score": round(
                health,
                2
            )
        })

    return (
        pd.DataFrame(results)
        .sort_values(
            "health_score",
            ascending=False
        )
    )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

def dashboard_summary(df):

    revenue = revenue_df(df)

    return {
        "total_revenue":
            round(
                revenue["total_amount_inr"]
                .sum(),
                2
            ),

        "total_bookings":
            int(len(df)),

        "checked_out":
            int(
                len(
                    df[
                        df["status"]
                        == "Checked-out"
                    ]
                )
            ),

        "properties":
            int(
                df["property"]
                .nunique()
            )
    }

def monthly_metrics(df):

    revenue = df[
        df["is_revenue"] == True
    ].copy()

    return (
        revenue
        .groupby("month_num")
        .agg(
            revenue=("total_amount_inr", "sum"),
            bookings=("booking_id", "count")
        )
        .reset_index()
        .sort_values("month_num")
    )