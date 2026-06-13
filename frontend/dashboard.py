import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

API_BASE = "http://localhost:5000"

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Fernhill Stay Ops",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# GLOBAL THEME & CSS
# ---------------------------------------------------

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ── ROOT & BACKGROUND ─────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background-color: #0B1628 !important;
    color: #E2EAF4 !important;
}

[data-testid="stSidebar"] {
    background-color: #0D1E36 !important;
    border-right: 1px solid #1E3352 !important;
}

[data-testid="stHeader"] {
    background-color: #0B1628 !important;
}

/* ── TYPOGRAPHY ───────────────────────────────── */
h1, h2, h3 {
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 0.04em;
}

body, p, div, span, label,
[data-testid="stMarkdownContainer"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── MAIN TITLE ───────────────────────────────── */
.fh-hero {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #E8C97D;
    line-height: 1;
    margin: 0;
}

.fh-hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 400;
    color: #8FA3B8;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 4px;
}

.fh-badge {
    display: inline-block;
    background: rgba(232,201,125,0.12);
    border: 1px solid rgba(232,201,125,0.3);
    color: #E8C97D;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
    margin-bottom: 12px;
}

/* ── KPI CARDS ────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin: 20px 0 28px;
}

.kpi-card {
    background: linear-gradient(145deg, #0F2040, #0D1A30);
    border: 1px solid #1E3352;
    border-radius: 6px;
    padding: 20px 18px 16px;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #E8C97D, transparent);
}

.kpi-card.accent-teal::before { background: linear-gradient(90deg, #4ECDC4, transparent); }
.kpi-card.accent-coral::before { background: linear-gradient(90deg, #E07B6A, transparent); }
.kpi-card.accent-violet::before { background: linear-gradient(90deg, #A78BFA, transparent); }
.kpi-card.accent-blue::before { background: linear-gradient(90deg, #60A5FA, transparent); }

.kpi-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    color: #8FA3B8;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.kpi-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #E2EAF4;
    line-height: 1;
}

.kpi-icon {
    position: absolute;
    top: 16px; right: 16px;
    font-size: 1.4rem;
    opacity: 0.25;
}

/* ── SECTION HEADERS ──────────────────────────── */
.section-header {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #E2EAF4;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border-left: 3px solid #E8C97D;
    padding-left: 12px;
    margin: 24px 0 16px;
}

/* ── EXECUTIVE SUMMARY BOX ────────────────────── */
.exec-box {
    background: linear-gradient(135deg, rgba(78,205,196,0.07), rgba(232,201,125,0.05));
    border: 1px solid rgba(78,205,196,0.2);
    border-radius: 6px;
    padding: 18px 22px;
    margin: 0 0 24px;
    font-size: 0.88rem;
    color: #C5D5E8;
    line-height: 1.7;
}

.exec-box strong {
    color: #E8C97D;
    font-weight: 600;
}

/* ── TABS ─────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    background: #0D1E36;
    border-bottom: 1px solid #1E3352;
    gap: 0;
    padding: 0 8px;
}

[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #8FA3B8 !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 20px !important;
    border-radius: 0 !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #E8C97D !important;
    border-bottom-color: #E8C97D !important;
    background: transparent !important;
}

/* ── DATA TABLE ───────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #1E3352 !important;
    border-radius: 6px !important;
    overflow: hidden;
}

[data-testid="stDataFrame"] table {
    background: #0D1E36 !important;
}

[data-testid="stDataFrame"] th {
    background: #0B1628 !important;
    color: #8FA3B8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #1E3352 !important;
}

[data-testid="stDataFrame"] td {
    color: #C5D5E8 !important;
    font-size: 0.85rem !important;
    border-color: #1E3352 !important;
}

/* ── SIDEBAR ──────────────────────────────────── */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #8FA3B8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] select,
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #0B1628 !important;
    border-color: #1E3352 !important;
    color: #E2EAF4 !important;
}

.sidebar-logo {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #E8C97D;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 8px 0 4px;
}

.sidebar-tagline {
    font-size: 0.68rem;
    color: #8FA3B8;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.sidebar-divider {
    border: none;
    border-top: 1px solid #1E3352;
    margin: 16px 0;
}

/* ── METRICS (native streamlit) ───────────────── */
[data-testid="stMetric"] {
    background: #0D1E36 !important;
    border: 1px solid #1E3352 !important;
    border-radius: 6px !important;
    padding: 14px !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    color: #8FA3B8 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.8rem !important;
    color: #E2EAF4 !important;
}

/* ── INFO / SUCCESS / WARNING BOXES ──────────── */
[data-testid="stAlert"] {
    border-radius: 6px !important;
    border-left-width: 3px !important;
    font-size: 0.86rem !important;
}

/* ── AUDIT MARKDOWN ───────────────────────────── */
.audit-section h3 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.1rem !important;
    color: #E8C97D !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    margin-top: 22px !important;
}

/* ── SCROLLBAR ────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0B1628; }
::-webkit-scrollbar-thumb { background: #1E3352; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2A4A6B; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PLOTLY THEME
# ---------------------------------------------------

CHART_BG       = "#0B1628"
CHART_PAPER    = "#0B1628"
GRID_COLOR     = "#1E3352"
AXIS_COLOR     = "#8FA3B8"
FONT_COLOR     = "#C5D5E8"
PALETTE        = ["#E8C97D", "#4ECDC4", "#E07B6A", "#A78BFA", "#60A5FA"]

def apply_dark_theme(fig, title=""):
    fig.update_layout(
        plot_bgcolor=CHART_BG,
        paper_bgcolor=CHART_PAPER,
        font=dict(family="Inter, sans-serif", color=FONT_COLOR, size=12),
        title=dict(
            text=title,
            font=dict(family="Barlow Condensed, sans-serif", size=18,
                      color="#E2EAF4", weight="bold"),
            x=0.02, xanchor="left"
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            tickcolor=AXIS_COLOR,
            tickfont=dict(color=AXIS_COLOR, size=11),
            title_font=dict(color=AXIS_COLOR, size=11)
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            tickcolor=AXIS_COLOR,
            tickfont=dict(color=AXIS_COLOR, size=11),
            title_font=dict(color=AXIS_COLOR, size=11),
            zeroline=False
        ),
        legend=dict(
            bgcolor="rgba(11,22,40,0.8)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
            font=dict(color=FONT_COLOR, size=11)
        ),
        margin=dict(l=16, r=16, t=48, b=16),
        hoverlabel=dict(
            bgcolor="#0F2040",
            bordercolor="#1E3352",
            font=dict(family="Inter, sans-serif", color="#E2EAF4", size=12)
        )
    )
    return fig

# ---------------------------------------------------
# API LOADER
# ---------------------------------------------------

@st.cache_data(ttl=60)
def load_data():
    summary    = requests.get(f"{API_BASE}/summary",    timeout=10).json()
    properties = pd.DataFrame(requests.get(f"{API_BASE}/properties", timeout=10).json())
    channels   = pd.DataFrame(requests.get(f"{API_BASE}/channels",   timeout=10).json())
    health     = pd.DataFrame(requests.get(f"{API_BASE}/health",     timeout=10).json())
    monthly    = pd.DataFrame(requests.get(f"{API_BASE}/monthly").json())
    audit      = requests.get(f"{API_BASE}/audit").json()
    return summary, properties, channels, health, monthly, audit

try:
    summary, properties, channels, health, monthly, audit = load_data()
except Exception as e:
    st.error("Unable to connect to backend API.")
    st.exception(e)
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🏨 Fernhill Stay</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Operations Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown("**Filter by Property**")
    property_options = ["All"] + sorted(properties["property"].unique().tolist())
    selected_property = st.selectbox("Property", property_options, label_visibility="collapsed")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    

if selected_property != "All":
    properties_view = properties[properties["property"] == selected_property]
    health_view     = health[health["property"] == selected_property]
else:
    properties_view = properties.copy()
    health_view     = health.copy()

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown('<div class="fh-badge">Operational Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="fh-hero">Fernhill Stay Ops</div>', unsafe_allow_html=True)
st.markdown('<div class="fh-hero-sub">Performance Intelligence · Jan – May 2026</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# KPI ROW
# ---------------------------------------------------

best_property = health.sort_values("health_score", ascending=False).iloc[0]

kpi_html = f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-icon">₹</div>
    <div class="kpi-label">Total Revenue</div>
    <div class="kpi-value">₹{summary['total_revenue']:,.0f}</div>
  </div>
  <div class="kpi-card accent-teal">
    <div class="kpi-icon">📋</div>
    <div class="kpi-label">Total Bookings</div>
    <div class="kpi-value">{summary['total_bookings']}</div>
  </div>
  <div class="kpi-card accent-coral">
    <div class="kpi-icon">✓</div>
    <div class="kpi-label">Checked Out</div>
    <div class="kpi-value">{summary['checked_out']}</div>
  </div>
  <div class="kpi-card accent-violet">
    <div class="kpi-icon">🏢</div>
    <div class="kpi-label">Properties</div>
    <div class="kpi-value">{summary['properties']}</div>
  </div>
  <div class="kpi-card accent-blue">
    <div class="kpi-icon">🏆</div>
    <div class="kpi-label">Top Property</div>
    <div class="kpi-value" style="font-size:1.1rem;padding-top:4px;">{best_property['property']}</div>
  </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# ---------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------

st.markdown(
    f"""<div class="exec-box">
    Top-performing property: <strong>{best_property['property']}</strong> &nbsp;·&nbsp;
    Health Score: <strong>{best_property['health_score']}</strong>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    All metrics calculated from the <strong>cleaned dataset</strong>.
    Cancelled bookings are excluded from revenue. Only <strong>Checked-out</strong> bookings
    contribute toward revenue figures.
    </div>""",
    unsafe_allow_html=True
)

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "📈  Property Performance",
    "🔗  Channel Analysis",
    "💠  Health Score",
    
])

# ===================================================
# TAB 1 — Property Performance
# ===================================================

with tab1:

    st.markdown('<div class="section-header">Revenue Trend</div>', unsafe_allow_html=True)

    # Revenue trend – area + line
    trend_fig = go.Figure()

    trend_fig.add_trace(go.Scatter(
        x=monthly["month_num"],
        y=monthly["revenue"],
        mode="lines+markers",
        name="Revenue",
        line=dict(color="#E8C97D", width=2.5, shape="spline"),
        marker=dict(size=8, color="#E8C97D",
                    line=dict(color="#0B1628", width=2)),
        fill="tozeroy",
        fillcolor="rgba(232,201,125,0.08)",
        hovertemplate="Month %{x}<br>₹%{y:,.0f}<extra></extra>"
    ))

    trend_fig = apply_dark_theme(trend_fig, "Monthly Revenue · Jan–May 2026")
    trend_fig.update_xaxes(
        tickvals=monthly["month_num"].tolist(),
        ticktext=["Jan","Feb","Mar","Apr","May"][:len(monthly)]
    )
    trend_fig.update_yaxes(tickprefix="₹", tickformat=",.0f")
    trend_fig.update_layout(showlegend=False, height=320)
    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown('<div class="section-header">Bookings by Property</div>', unsafe_allow_html=True)

    # Horizontal bar — more legible for property names
    booking_fig = go.Figure(go.Bar(
        y=properties_view["property"],
        x=properties_view["bookings"],
        orientation="h",
        marker=dict(
            color=properties_view["bookings"],
            colorscale=[[0, "#1E3352"], [0.5, "#4ECDC4"], [1, "#E8C97D"]],
            showscale=False,
            line=dict(width=0)
        ),
        text=properties_view["bookings"],
        textposition="outside",
        textfont=dict(color="#E2EAF4", size=11),
        hovertemplate="%{y}<br>Bookings: %{x}<extra></extra>"
    ))

    booking_fig = apply_dark_theme(booking_fig, "Bookings by Property")
    booking_fig.update_layout(height=max(280, len(properties_view) * 42), yaxis=dict(autorange="reversed"))
    booking_fig.update_xaxes(title_text="Bookings")
    st.plotly_chart(booking_fig, use_container_width=True)

    # Data table
    st.markdown('<div class="section-header">Property Data</div>', unsafe_allow_html=True)
    display = properties_view.copy()
    if "revenue" in display.columns:
        display["revenue"] = display["revenue"].round(0).astype(int)
    st.dataframe(display, use_container_width=True, hide_index=True)

# ===================================================
# TAB 2 — Channel Analysis
# ===================================================

with tab2:

    col_a, col_b = st.columns([1, 1], gap="medium")

    with col_a:
        st.markdown('<div class="section-header">Revenue by Channel</div>', unsafe_allow_html=True)

        pie_fig = go.Figure(go.Pie(
            labels=channels["booking_channel"],
            values=channels["revenue"],
            hole=0.52,
            marker=dict(
                colors=PALETTE,
                line=dict(color=CHART_BG, width=3)
            ),
            textinfo="label+percent",
            textfont=dict(color="#E2EAF4", size=11),
            hovertemplate="%{label}<br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
            rotation=90
        ))

        # Centre label
        top_ch = channels.sort_values("revenue", ascending=False).iloc[0]
        pie_fig.update_layout(
            annotations=[dict(
                text=f"<b>{top_ch['booking_channel']}</b><br><span style='font-size:10px'>Top Channel</span>",
                x=0.5, y=0.5, font=dict(size=12, color="#E8C97D"),
                showarrow=False
            )],
            showlegend=True,
            legend=dict(orientation="v", x=1.02, y=0.5),
            height=360
        )
        pie_fig = apply_dark_theme(pie_fig, "Revenue Contribution")
        st.plotly_chart(pie_fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Bookings by Channel</div>', unsafe_allow_html=True)

        bar_ch = go.Figure(go.Bar(
            x=channels["booking_channel"],
            y=channels["bookings"],
            marker=dict(
                color=PALETTE[:len(channels)],
                line=dict(width=0)
            ),
            text=channels["bookings"],
            textposition="outside",
            textfont=dict(color="#E2EAF4", size=11),
            hovertemplate="%{x}<br>Bookings: %{y}<extra></extra>"
        ))
        bar_ch = apply_dark_theme(bar_ch, "Bookings Volume")
        bar_ch.update_layout(height=360, showlegend=False)
        bar_ch.update_yaxes(title_text="Bookings")
        st.plotly_chart(bar_ch, use_container_width=True)

    st.markdown('<div class="section-header">Channel Data</div>', unsafe_allow_html=True)
    st.dataframe(channels, use_container_width=True, hide_index=True)

    st.success(
        f"**Highest revenue channel:** {top_ch['booking_channel']} "
        f"— ₹{top_ch['revenue']:,.0f}"
    )

# ===================================================
# TAB 3 — Health Score
# ===================================================

with tab3:

    # Formula card
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    formula_items = [
        ("40%", "Revenue Performance",     "#E8C97D"),
        ("30%", "Checked-out Rate",         "#4ECDC4"),
        ("20%", "Cancellation Quality",     "#E07B6A"),
        ("10%", "Channel Diversity",        "#A78BFA"),
    ]
    for col, (pct, label, color) in zip([col_f1, col_f2, col_f3, col_f4], formula_items):
        with col:
            st.markdown(
                f"""<div style="
                    background:linear-gradient(145deg,#0F2040,#0D1A30);
                    border:1px solid #1E3352;
                    border-top:2px solid {color};
                    border-radius:6px;
                    padding:14px 16px;
                    text-align:center;margin-bottom:12px;">
                    <div style="font-family:Barlow Condensed,sans-serif;font-size:2rem;
                        font-weight:800;color:{color};">{pct}</div>
                    <div style="font-size:0.72rem;color:#8FA3B8;letter-spacing:0.08em;
                        text-transform:uppercase;">{label}</div>
                </div>""",
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-header">Health Score Leaderboard</div>', unsafe_allow_html=True)

    health_sorted = (
        health_view
        .sort_values("health_score", ascending=True)
        .reset_index(drop=True)
    )

    # Gradient bar chart — the signature element
    n = len(health_sorted)
    colors = []
    for i in range(n):
        ratio = i / max(n - 1, 1)
        # interpolate from #E07B6A → #4ECDC4 → #E8C97D
        if ratio < 0.5:
            r_ratio = ratio * 2
            r = int(0xE0 + (0x4E - 0xE0) * r_ratio)
            g = int(0x7B + (0xCD - 0x7B) * r_ratio)
            b = int(0x6A + (0xC4 - 0x6A) * r_ratio)
        else:
            r_ratio = (ratio - 0.5) * 2
            r = int(0x4E + (0xE8 - 0x4E) * r_ratio)
            g = int(0xCD + (0xC9 - 0xCD) * r_ratio)
            b = int(0xC4 + (0x7D - 0xC4) * r_ratio)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")

    hs_fig = go.Figure(go.Bar(
        y=health_sorted["property"],
        x=health_sorted["health_score"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"  {v}" for v in health_sorted["health_score"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="#0B1628", size=12, family="Barlow Condensed"),
        hovertemplate="%{y}<br>Health Score: %{x}<extra></extra>"
    ))

    hs_fig = apply_dark_theme(hs_fig, "Property Health Score Ranking")
    hs_fig.update_layout(height=max(300, n * 46), yaxis=dict(autorange="reversed"))
    hs_fig.update_xaxes(title_text="Score", range=[0, 110])
    st.plotly_chart(hs_fig, use_container_width=True)

    # Leaderboard table with rank
    health_display = (
        health_view
        .sort_values("health_score", ascending=False)
        .reset_index(drop=True)
    )
    health_display.insert(0, "Rank", [f"#{i+1}" for i in range(len(health_display))])

    st.dataframe(
        health_display[["Rank", "property", "health_score"]],
        use_container_width=True,
        hide_index=True
    )

    winner = health_view.sort_values("health_score", ascending=False).iloc[0]
    st.success(
        f"🏆 **Best Performing Property:** {winner['property']} &nbsp;·&nbsp; "
        f"Health Score: **{winner['health_score']}**"
    )

