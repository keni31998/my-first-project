# ==============================================
# Multi-Company Financial Comparison Analysis System
# Local Excel File | Macaron Color Scheme | Full Button Interaction
# ==============================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# --------------------------
# Page Settings
# --------------------------
st.set_page_config(
    page_title="Financial Analysis System",
    page_icon="📊",
    layout="wide"
)

# --------------------------
# Macaron Color Palette (soft & beautiful)
# --------------------------
colors = [
    "#FFB7B7", "#FFD9B7", "#FFFFB7",
    "#B7FFB7", "#B7FFFF", "#B7B7FF",
    "#FFB7FF", "#D9B7FF", "#B7D9FF"
]

plt.rcParams["font.sans-serif"] = ["Arial", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# --------------------------
# Title
# --------------------------
st.title("📊 Multi-Company Financial Comparison Analysis System")
st.markdown("---")

# ==============================================
# ✅ Core: Read Local Excel File (100% stable)
# ==============================================
@st.cache_data
def load_data():
    # Read local Excel file (synced with GitHub repo)
    df = pd.read_excel("company_finance_data.xlsx")
    return df

try:
    df = load_data()
    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"❌ Data load failed: {str(e)}")
    st.info("Please check if 'company_finance_data.xlsx' is in the same folder as app.py")
    st.stop()

# ==============================================
# Sidebar: Company + Year Selection (all buttons, no input)
# ==============================================
with st.sidebar:
    st.header("⚙️ Filter Settings")
    
    # Select Companies
    companies = sorted(df["company_name"].unique())
    selected_companies = st.multiselect(
        "Select Companies",
        companies,
        default=companies[:2]
    )
    
    # Select Year Range
    years = sorted(df["fyear"].unique())
    start_year, end_year = st.select_slider(
        "Select Year Range",
        options=years,
        value=(years[0], years[-1])
    )

# Filter Data
df_filter = df[
    (df["company_name"].isin(selected_companies)) &
    (df["fyear"] >= start_year) &
    (df["fyear"] <= end_year)
].copy()

# Show Data Preview
with st.expander("📄 View Data Preview"):
    st.dataframe(df_filter.round(2), use_container_width=True)

st.markdown("---")

# ==============================================
# Function Selection (Button Menu)
# ==============================================
st.subheader("📈 Select Analysis Chart")
chart_type = st.radio(
    "",
    [
        "1 Annual Revenue Comparison",
        "2 Annual Net Profit Trend",
        "3 Revenue Share Pie Chart (Select Year)",
        "4 Profit Contribution Bar Chart (Select Year)",
        "5 Annual Revenue Growth Rate",
        "6 Net Profit Margin Ranking (Select Year)",
        "7 Annual Asset Scale Comparison",
        "8 Comprehensive Capability Radar Chart (Select Year)"
    ],
    horizontal=True
)

# Select Year (only for pie/bar/ranking/radar charts)
need_year = ["3", "4", "6", "8"]
select_year = None
if any(key in chart_type for key in need_year):
    select_year = st.selectbox("Select Year", sorted(df_filter["fyear"].unique()))

# ==============================================
# 8 Charts (Macaron Color Scheme + 1:1 Restoration)
# ==============================================

# 1 Annual Revenue Comparison
if chart_type.startswith("1"):
    fig, ax = plt.subplots(figsize=(12,5))
    for i, c in enumerate(df_filter.company_name.unique()):
        d = df_filter[df_filter.company_name == c]
        ax.bar(d.fyear.astype(str), d.revenue, label=c, color=colors[i % len(colors)], alpha=0.8)
    ax.set_title("Annual Revenue Comparison", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)

# 2 Annual Net Profit Trend
elif chart_type.startswith("2"):
    fig, ax = plt.subplots(figsize=(12,5))
    for i, c in enumerate(df_filter.company_name.unique()):
        d = df_filter[df_filter.company_name == c]
        ax.plot(d.fyear.astype(str), d.profit, marker="o", label=c, color=colors[i % len(colors)], linewidth=2)
    ax.set_title("Annual Net Profit Trend", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)

# 3 Revenue Share Pie Chart
elif chart_type.startswith("3"):
    d = df_filter[df_filter.fyear == select_year]
    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(d.rev_share, labels=d.company_name, autopct="%.1f%%", colors=colors, startangle=90)
    ax.set_title(f"Revenue Share - {select_year}", fontsize=14, fontweight='bold')
    st.pyplot(fig)

# 4 Profit Contribution Horizontal Bar Chart
elif chart_type.startswith("4"):
    d = df_filter[df_filter.fyear == select_year]
    fig, ax = plt.subplots(figsize=(10,5))
    ax.barh(d.company_name, d.prof_share, color=colors[:len(d)], alpha=0.8)
    ax.set_title(f"Profit Contribution - {select_year}", fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    st.pyplot(fig)

# 5 Annual Revenue Growth Rate
elif chart_type.startswith("5"):
    fig, ax = plt.subplots(figsize=(12,5))
    for i, c in enumerate(df_filter.company_name.unique()):
        d = df_filter[df_filter.company_name == c]
        ax.plot(d.fyear.astype(str), d.revenue_growth.fillna(0), marker='o', color=colors[i % len(colors)], linewidth=2)
    ax.set_title("Annual Revenue Growth Rate", fontsize=14, fontweight='bold')
    ax.legend(df_filter.company_name.unique())
    ax.grid(alpha=0.3)
    st.pyplot(fig)

# 6 Net Profit Margin Ranking
elif chart_type.startswith("6"):
    d = df_filter[df_filter.fyear == select_year]
    fig, ax = plt.subplots(figsize=(10,5))
    ax.barh(d.company_name, d.profit_margin * 100, color=colors[:len(d)], alpha=0.8)
    ax.set_title(f"Net Profit Margin Ranking (%) - {select_year}", fontsize=14, fontweight='bold')
    st.pyplot(fig)

# 7 Annual Asset Scale Comparison
elif chart_type.startswith("7"):
    fig, ax = plt.subplots(figsize=(12,5))
    for i, c in enumerate(df_filter.company_name.unique()):
        d = df_filter[df_filter.company_name == c]
        ax.fill_between(d.fyear.astype(str), d.assets, alpha=0.4, color=colors[i % len(colors)], label=c)
    ax.set_title("Annual Asset Scale Comparison", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)

# 8 Comprehensive Capability Radar Chart
elif chart_type.startswith("8"):
    d = df_filter[df_filter.fyear == select_year].copy()
    indicators = ["Revenue", "Profit", "Net Margin", "Growth", "Assets"]
    N = len(indicators)

    for _, row in d.iterrows():
        values = [
            row["revenue"] / d["revenue"].max() * 10,
            row["profit"] / d["profit"].max() * 10,
            row["profit_margin"] * 10,
            max(row["revenue_growth"], 0) / 50 * 10 if pd.notna(row["revenue_growth"]) else 0,
            row["assets"] / d["assets"].max() * 10
        ]
        values += values[:1]
        angles = [n / N * 2 * pi for n in range(N)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color='#FFA8A8', linewidth=2)
        ax.fill(angles, values, color='#FFD1DC', alpha=0.4)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(indicators)
        ax.set_title(f"Comprehensive Capability - {row.company_name} ({select_year})", fontsize=14, fontweight='bold')
        st.pyplot(fig)

st.markdown("---")
st.caption("✅ Multi-Company Financial Comparison Analysis System | Streamlit Version")
