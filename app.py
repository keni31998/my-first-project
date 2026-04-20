# ==============================================
# Multi-Company Financial Analysis System (Final Polished Version)
# Created by Connie | Independent Controls | Smart Analysis | No Stacked Bars
# ==============================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="Connie's Financial Dashboard", page_icon="📊", layout="wide")

# --------------------------
# Color pool (No repetition, soft)
# --------------------------
COLORS = [
    "#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#FF99CC",
    "#99CCFF", "#FFB366", "#85E0C8", "#C29FFF", "#73DFFF",
    "#FFA75B", "#B8E085", "#FF88A8", "#66B2E0", "#B2F080"
]

plt.rcParams["font.sans-serif"] = ["Arial", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# --------------------------
# Welcome Text + Platform Description
# --------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #FF6B6B;'>
    👋 Hello, Welcome to Connie's Interactive Financial Dashboard! 📊
    </h1>
    <p style='text-align: center; font-size: 18px; color: #888888;'>
    This is an interactive platform for multi-company financial performance comparison, featuring 8 professional charts and smart analysis.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# ==============================================
# Load data (local file, stable)
# ==============================================
@st.cache_data
def load_data():
    return pd.read_excel("company_finance_data.xlsx")

df = load_data()
all_companies = sorted(df["company_name"].unique())
all_years = sorted(df["fyear"].unique())
st.success("✅ Data loaded successfully")

# ==============================================
# Sidebar: Project Info + Company List
# ==============================================
with st.sidebar:
    st.header("📂 About This Dashboard")
    st.markdown("""
    **8 Analysis Charts:**
    1. Annual Revenue Comparison
    2. Annual Net Profit Trend
    3. Revenue Share Pie Chart
    4. Profit Contribution Bar Chart
    5. Annual Revenue Growth Rate
    6. Net Profit Margin Ranking
    7. Annual Asset Scale Comparison
    8. Comprehensive Capability Radar Chart
    """)
    st.markdown("---")
    st.subheader("Available Companies")
    for c in all_companies:
        st.markdown(f"- {c}")

# ==============================================
# Helper: get color for each company
# ==============================================
def get_color_map(companies):
    return {c: COLORS[i] for i, c in enumerate(companies)}

# ==============================================
# Helper: simple smart analysis text
# ==============================================
def smart_analysis(df, metric_name):
    if len(df) < 2:
        return "ℹ️ Please select at least 2 companies for comparison."
    max_row = df.loc[df[metric_name].idxmax()]
    min_row = df.loc[df[metric_name].idxmin()]
    diff = round((max_row[metric_name] - min_row[metric_name]) / min_row[metric_name] * 100, 1) if min_row[metric_name] !=0 else "N/A"
    return f"📊 Smart Analysis: **{max_row['company_name']}** has the highest {metric_name.replace('_', ' ')} ({round(max_row[metric_name],2)}), which is **{diff}% higher** than {min_row['company_name']} ({round(min_row[metric_name],2)})."

# ==============================================================================
# 1 Annual Revenue Comparison (FIXED: Grouped bars, no stacking)
# ==============================================================================
st.header("1. Annual Revenue Comparison")
col1, col2 = st.columns([3, 1])
with col1:
    comp1 = st.multiselect("Select companies", all_companies, key="c1", default=all_companies[:2])
with col2:
    y1_start, y1_end = st.select_slider("Year range", all_years, (all_years[0], all_years[-1]), key="y1")

df1 = df[(df["company_name"].isin(comp1)) & (df["fyear"] >= y1_start) & (df["fyear"] <= y1_end)]
cmap1 = get_color_map(comp1)

# Grouped bar chart fix
fig, ax = plt.subplots(figsize=(12, 5))
years = sorted(df1["fyear"].unique())
bar_width = 0.8 / len(comp1)
for i, c in enumerate(comp1):
    values = df1[df1["company_name"] == c].set_index("fyear")["revenue"].reindex(years, fill_value=0)
    x = np.arange(len(years)) + i * bar_width
    ax.bar(x, values, width=bar_width, label=c, color=cmap1[c], alpha=0.85)
ax.set_xticks(np.arange(len(years)) + bar_width * (len(comp1)-1)/2)
ax.set_xticklabels(years)
ax.set_title("Annual Revenue Comparison", weight="bold")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)

# Smart analysis
df1_agg = df1.groupby("company_name")["revenue"].sum().reset_index()
st.info(smart_analysis(df1_agg, "revenue"))
st.divider()

# ==============================================================================
# 2 Annual Net Profit Trend
# ==============================================================================
st.header("2. Annual Net Profit Trend")
col1, col2 = st.columns([3, 1])
with col1:
    comp2 = st.multiselect("Select companies", all_companies, key="c2", default=comp1)
with col2:
    y2_start, y2_end = st.select_slider("Year range", all_years, (all_years[0], all_years[-1]), key="y2")

df2 = df[(df["company_name"].isin(comp2)) & (df["fyear"] >= y2_start) & (df["fyear"] <= y2_end)]
cmap2 = get_color_map(comp2)

fig, ax = plt.subplots(figsize=(12, 5))
for c in comp2:
    d = df2[df2["company_name"] == c]
    ax.plot(d["fyear"].astype(str), d["profit"], marker="o", label=c, color=cmap2[c], linewidth=2.5)
ax.set_title("Net Profit Trend", weight="bold")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)

df2_agg = df2.groupby("company_name")["profit"].sum().reset_index()
st.info(smart_analysis(df2_agg, "profit"))
st.divider()

# ==============================================================================
# 3 Revenue Share Pie Chart
# ==============================================================================
st.header("3. Revenue Share Pie Chart")
col1, col2 = st.columns([3, 1])
with col1:
    comp3 = st.multiselect("Select companies", all_companies, key="c3", default=all_companies[:3])
with col2:
    y3 = st.selectbox("Select year", all_years, len(all_years)-1, key="y3")

df3 = df[(df["company_name"].isin(comp3)) & (df["fyear"] == y3)]
cmap3 = get_color_map(comp3)

fig, ax = plt.subplots(figsize=(7,7))
wedges, texts, autotexts = ax.pie(df3["rev_share"], labels=df3["company_name"], autopct="%.1f%%",
       colors=[cmap3[c] for c in df3["company_name"]], startangle=90)
# Improve readability
plt.setp(texts, size=10)
plt.setp(autotexts, size=10, weight="bold", color="white")
ax.set_title(f"Revenue Share {y3}", weight="bold")
st.pyplot(fig)

st.info(smart_analysis(df3, "rev_share"))
st.divider()

# ==============================================================================
# 4 Profit Contribution Bar Chart
# ==============================================================================
st.header("4. Profit Contribution Bar Chart")
col1, col2 = st.columns([3, 1])
with col1:
    comp4 = st.multiselect("Select companies", all_companies, key="c4", default=comp3)
with col2:
    y4 = st.selectbox("Select year", all_years, len(all_years)-1, key="y4")

df4 = df[(df["company_name"].isin(comp4)) & (df["fyear"] == y4)]
cmap4 = get_color_map(comp4)

fig, ax = plt.subplots(figsize=(10,5))
ax.barh(df4["company_name"], df4["prof_share"], color=[cmap4[c] for c in df4["company_name"]], alpha=0.85)
ax.set_title(f"Profit Contribution {y4}", weight="bold")
ax.grid(alpha=0.3)
st.pyplot(fig)

st.info(smart_analysis(df4, "prof_share"))
st.divider()

# ==============================================================================
# 5 Annual Revenue Growth Rate
# ==============================================================================
st.header("5. Annual Revenue Growth Rate")
col1, col2 = st.columns([3, 1])
with col1:
    comp5 = st.multiselect("Select companies", all_companies, key="c5", default=comp2)
with col2:
    y5_start, y5_end = st.select_slider("Year range", all_years, (all_years[0], all_years[-1]), key="y5")

df5 = df[(df["company_name"].isin(comp5)) & (df["fyear"] >= y5_start) & (df["fyear"] <= y5_end)]
cmap5 = get_color_map(comp5)

fig, ax = plt.subplots(figsize=(12,5))
for c in comp5:
    d = df5[df5["company_name"] == c]
    ax.plot(d["fyear"].astype(str), d["revenue_growth"].fillna(0),
            marker="o", label=c, color=cmap5[c], linewidth=2.5)
ax.set_title("Revenue Growth Rate", weight="bold")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)

df5_agg = df5.groupby("company_name")["revenue_growth"].mean().reset_index()
st.info(smart_analysis(df5_agg, "revenue_growth"))
st.divider()

# ==============================================================================
# 6 Net Profit Margin Ranking (FIXED: sorted descending)
# ==============================================================================
st.header("6. Net Profit Margin Ranking (%)")
col1, col2 = st.columns([3, 1])
with col1:
    comp6 = st.multiselect("Select companies", all_companies, key="c6", default=comp4)
with col2:
    y6 = st.selectbox("Select year", all_years, len(all_years)-1, key="y6")

df6 = df[(df["company_name"].isin(comp6)) & (df["fyear"] == y6)].copy()
# Sort descending
df6 = df6.sort_values("profit_margin", ascending=True)
cmap6 = get_color_map(comp6)

fig, ax = plt.subplots(figsize=(10,5))
ax.barh(df6["company_name"], df6["profit_margin"]*100,
        color=[cmap6[c] for c in df6["company_name"]], alpha=0.85)
ax.set_title(f"Net Profit Margin {y6}", weight="bold")
st.pyplot(fig)

st.info(smart_analysis(df6, "profit_margin"))
st.divider()

# ==============================================================================
# 7 Asset Scale Comparison (Improved readability)
# ==============================================================================
st.header("7. Annual Asset Scale Comparison")
col1, col2 = st.columns([3, 1])
with col1:
    comp7 = st.multiselect("Select companies", all_companies, key="c7", default=comp1)
with col2:
    y7_start, y7_end = st.select_slider("Year range", all_years, (all_years[0], all_years[-1]), key="y7")

df7 = df[(df["company_name"].isin(comp7)) & (df["fyear"] >= y7_start) & (df["fyear"] <= y7_end)]
cmap7 = get_color_map(comp7)

fig, ax = plt.subplots(figsize=(12,5))
for c in comp7:
    d = df7[df7["company_name"] == c]
    ax.fill_between(d["fyear"].astype(str), d["assets"], alpha=0.4, label=c, color=cmap7[c])
ax.set_title("Asset Scale Comparison", weight="bold")
ax.legend(loc="upper left", bbox_to_anchor=(1,1))
ax.grid(alpha=0.3)
st.pyplot(fig)

df7_agg = df7.groupby("company_name")["assets"].sum().reset_index()
st.info(smart_analysis(df7_agg, "assets"))
st.divider()

# ==============================================================================
# 8 Comprehensive Capability Radar Chart (Added comparison table + FIXED error)
# ==============================================================================
st.header("8. Comprehensive Capability Radar Chart")
col1, col2 = st.columns([3, 1])
with col1:
    comp8 = st.multiselect("Select companies", all_companies, key="c8", default=all_companies[:2])
with col2:
    y8 = st.selectbox("Select year", all_years, len(all_years)-1, key="y8")

df8 = df[(df["company_name"].isin(comp8)) & (df["fyear"] == y8)].copy()
indicators = ["Revenue", "Profit", "Net Margin", "Growth", "Assets"]
N = len(indicators)

# Prepare comparison table
comparison_data = []

for idx, (_, row) in enumerate(df8.iterrows()):
    c = row["company_name"]
    color = COLORS[idx % len(COLORS)]

    values = [
        row["revenue"] / df8["revenue"].max() * 10,
        row["profit"] / df8["profit"].max() * 10,
        row["profit_margin"] * 10,
        max(row["revenue_growth"], 0) / 50 * 10 if pd.notna(row["revenue_growth"]) else 0,
        row["assets"] / df8["assets"].max() * 10
    ]
    values += values[:1]
    angles = [n / N * 2 * pi for n in range(N)] + [0]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw={"polar": True})
    ax.plot(angles, values, linewidth=2.5, color=color, label=c)
    ax.fill(angles, values, alpha=0.35, color=color)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(indicators)
    ax.set_title(f"{c} - {y8} Comprehensive Score", weight="bold")
    ax.legend(loc="upper right")
    st.pyplot(fig)

    # Add to comparison table
    comparison_data.append({
        "Company": c,
        "Revenue Score": round(values[0], 2),
        "Profit Score": round(values[1], 2),
        "Net Margin Score": round(values[2], 2),
        "Growth Score": round(values[3], 2),
        "Assets Score": round(values[4], 2)
    })

# Show comparison table
st.subheader("📊 Numerical Comparison Table")
st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)

# Smart analysis for radar chart (FIXED error: exclude "Company" key)
if len(comp8) >= 2:
    def total_score(x):
        return sum(v for k, v in x.items() if k != "Company")
    max_comp = max(comparison_data, key=total_score)
    st.info(f"📊 Smart Analysis: **{max_comp['Company']}** has the highest overall comprehensive score, leading in multiple dimensions.")

st.markdown("---")
st.caption("✅ Multi-Company Financial Analysis System | Created by Connie")
