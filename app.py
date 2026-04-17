# ==============================================
# Multi-Company Business Analysis System (Streamlit)
# Enhanced Visualization | Interactive Charts | Professional Style
# ==============================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import wrds
from math import pi
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# ----------------------
# Constants
# ----------------------
MIN_YEAR = 2015
MAX_YEAR = 2025
DEFAULT_START_YEAR = 2018
DEFAULT_END_YEAR = 2023
DEFAULT_TICKERS = "AAPL,MSFT,TSLA"
CORR_COLS = ["revenue", "profit", "assets", "profit_margin", "revenue_growth"]
RADAR_INDICATORS = ["Revenue", "Profit", "Profit Margin", "Growth", "Assets"]
PLOTLY_CONFIG = {
    'displayModeBar': False,
    'responsive': True,
    'staticPlot': False
}
PLOTLY_STYLE = {
    'template': 'plotly_white',
    'color_discrete_sequence': px.colors.qualitative.Bold,
    'title_x': 0.5
}

# ----------------------
# Functions
# ----------------------
def fetch_wrds_data(db, tickers, start_year, end_year):
    try:
        ticker_params = ', '.join([f"'{t}'" for t in tickers])
        sql = f"""
            SELECT
                tic AS company,
                fyear,
                sale AS revenue,
                ni AS profit,
                at AS assets,
                ni/sale AS profit_margin
            FROM comp.funda
            WHERE tic IN ({ticker_params})
              AND fyear BETWEEN {start_year} AND {end_year}
        """
        df = db.raw_sql(sql)
        df = df.groupby(["company", "fyear"]).last().reset_index()
        df["fyear"] = df["fyear"].astype(int)

        df = df.sort_values(["company", "fyear"])
        df["revenue_growth"] = df.groupby("company")["revenue"].pct_change() * 100
        df["profit_growth"] = df.groupby("company")["profit"].pct_change() * 100
        df[["revenue_growth", "profit_growth"]] = df[["revenue_growth", "profit_growth"]].fillna(0)

        df["profit_margin"] = df["profit"].div(df["revenue"], fill_value=0)

        year_total = df.groupby("fyear")[["revenue", "profit", "assets"]].sum().reset_index()
        year_total.columns = ["fyear", "total_rev", "total_prof", "total_ast"]
        df = df.merge(year_total, on="fyear")
        df["rev_share"] = df["revenue"] / df["total_rev"] * 100
        df["prof_share"] = df["profit"] / df["total_prof"] * 100

        return df
    except Exception as e:
        st.error(f"❌ Data fetch failed: {str(e)}")
        return pd.DataFrame()

def create_radar_chart(row, radar_df):
    max_revenue = radar_df["revenue"].max() or 1
    max_profit = radar_df["profit"].max() or 1
    max_assets = radar_df["assets"].max() or 1
    max_growth = radar_df["revenue_growth"].max() if radar_df["revenue_growth"].max() > 0 else 1

    values = [
        row["revenue"] / max_revenue * 10,
        row["profit"] / max_profit * 10,
        row["profit_margin"] * 10,
        max(row["revenue_growth"], 0) / max_growth * 10,
        row["assets"] / max_assets * 10
    ]
    values += values[:1]
    angles = [n / 5 * 2 * pi for n in range(5)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'polar': True})
    ax.plot(angles, values, linewidth=2, color="#1f77b4")
    ax.fill(angles, values, alpha=0.3, color="#1f77b4")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(RADAR_INDICATORS)
    ax.set_ylim(0, 10)
    plt.title(f"{row.company} {row.fyear}", fontsize=10, pad=20)
    return fig

# ----------------------
# Page Setup
# ----------------------
st.set_page_config(page_title="Multi-Company Analysis", layout="wide")
st.title("📊 Multi-Company Business Analysis System")
st.sidebar.header("⚙️ Settings")

# ----------------------
# WRDS Login
# ----------------------
st.sidebar.subheader("🔐 WRDS Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    try:
        db = wrds.Connection(wrds_username=username, wrds_password=password)
        db.list_libraries()
        st.sidebar.success("✅ Login Successful")
        st.session_state['db'] = db
    except Exception as e:
        st.sidebar.error(f"❌ Login Failed: {str(e)}")

if st.sidebar.button("🗑️ Clear Data"):
    for key in ['db', 'df']:
        if key in st.session_state:
            del st.session_state[key]
    st.sidebar.success("✅ Data cleared!")

# ----------------------
# Inputs
# ----------------------
st.sidebar.subheader("📋 Company & Year Settings")
tickers_str = st.sidebar.text_input("Company Tickers (comma-separated)", DEFAULT_TICKERS)
start_year = st.sidebar.number_input("Start Year", MIN_YEAR, MAX_YEAR, DEFAULT_START_YEAR)
end_year = st.sidebar.number_input("End Year", MIN_YEAR, MAX_YEAR, DEFAULT_END_YEAR)

tickers_valid = True
if tickers_str:
    tickers = [t.strip().upper() for t in tickers_str.split(",")]
    if not all(t.isalnum() for t in tickers):
        st.sidebar.error("❌ Invalid tickers. Use letters/numbers only.")
        tickers_valid = False

if start_year > end_year:
    st.sidebar.error("❌ Start year cannot be greater than end year.")
    tickers_valid = False

# ----------------------
# Load Data
# ----------------------
if st.sidebar.button("🚀 Load Data") and tickers_valid:
    if 'db' not in st.session_state:
        st.warning("⚠️ Please log in to WRDS first!")
        st.stop()

    with st.spinner("🔄 Loading data from WRDS..."):
        db = st.session_state['db']
        tickers = [t.strip().upper() for t in tickers_str.split(",")]
        df = fetch_wrds_data(db, tickers, start_year, end_year)

        if not df.empty:
            st.session_state['df'] = df
            st.success("✅ Data loaded successfully!")
            st.dataframe(df.round(2), use_container_width=True)
        else:
            st.warning("⚠️ No data found for the selected criteria!")

# ----------------------
# Visualization
# ----------------------
if 'df' in st.session_state:
    df = st.session_state['df']
    years = sorted(df['fyear'].unique())
    companies = sorted(df['company'].unique())

    st.divider()
    st.subheader("📊 Data Visualization")

    # KPI Cards
    st.subheader("🎯 Key Performance Indicators")
    latest_year = df['fyear'].max()
    latest = df[df['fyear'] == latest_year]
    cols = st.columns(len(companies))
    for i, comp in enumerate(companies):
        c_data = latest[latest['company'] == comp]
        with cols[i]:
            if not c_data.empty:
                rev = c_data['revenue'].values[0]
                profit = c_data['profit'].values[0]
                margin = c_data['profit_margin'].values[0] * 100
                st.metric(label=f"{comp} Revenue", value=f"${rev:,.0f}")
                st.metric(label="Net Profit", value=f"${profit:,.0f}")
                st.metric(label="Profit Margin %", value=f"{margin:.1f}%")
            else:
                st.info(f"No data for {comp}")

    st.divider()

    # 1 Revenue Trend
    st.subheader("1️⃣ Annual Revenue Trend")
    fig1 = px.line(df, x="fyear", y="revenue", color="company",
                   title="Revenue Trend by Company", markers=True, **PLOTLY_STYLE)
    st.plotly_chart(fig1, use_container_width=True, config=PLOTLY_CONFIG)

    # 2 Net Profit
    st.subheader("2️⃣ Net Profit Comparison")
    fig2 = px.bar(df, x="fyear", y="profit", color="company",
                  title="Net Profit by Year & Company", barmode="group", **PLOTLY_STYLE)
    st.plotly_chart(fig2, use_container_width=True, config=PLOTLY_CONFIG)

    # 3 Revenue Share
    st.subheader("3️⃣ Revenue Market Share")
    y_pie = st.selectbox("Select Year", years, key="pie")
    pie_data = df[df['fyear'] == y_pie]
    fig3 = px.pie(pie_data, values="rev_share", names="company",
                  title=f"Revenue Share {y_pie}", hole=0.3, **PLOTLY_STYLE)
    st.plotly_chart(fig3, use_container_width=True, config=PLOTLY_CONFIG)

    # 4 Profit Margin Ranking
    st.subheader("4️⃣ Profit Margin Ranking")
    y_margin = st.selectbox("Select Year", years, key="margin")
    mar_data = df[df['fyear'] == y_margin].sort_values("profit_margin")
    fig4 = px.barh(mar_data, x="profit_margin", y="company",
                   title=f"Profit Margin Ranking {y_margin}", **PLOTLY_STYLE)
    st.plotly_chart(fig4, use_container_width=True, config=PLOTLY_CONFIG)

    # 5 Revenue Growth
    st.subheader("5️⃣ Revenue Growth Rate Trend")
    fig5 = px.line(df, x="fyear", y="revenue_growth", color="company",
                   markers=True, title="Revenue Growth (%)", **PLOTLY_STYLE)
    st.plotly_chart(fig5, use_container_width=True, config=PLOTLY_CONFIG)

    # 6 Assets Trend
    st.subheader("6️⃣ Total Assets Trend")
    fig6 = px.area(df, x="fyear", y="assets", color="company",
                   title="Asset Size Comparison", **PLOTLY_STYLE)
    st.plotly_chart(fig6, use_container_width=True, config=PLOTLY_CONFIG)

    # 7 Radar Chart
    st.subheader("7️⃣ Comprehensive Capability Radar Chart")
    y_radar = st.selectbox("Select Year", years, key="radar")
    radar_df = df[df["fyear"] == y_radar].copy()

    if len(radar_df) > 6:
        st.warning("⚠️ Radar chart limited to 6 companies.")
        radar_df = radar_df.nlargest(6, "revenue")

    rad_cols = st.columns(len(radar_df))
    for i, (_, row) in enumerate(radar_df.iterrows()):
        with rad_cols[i]:
            fig = create_radar_chart(row, radar_df)
            st.pyplot(fig)

    # 8 Correlation Heatmap
    st.divider()
    st.subheader("8️⃣ Financial Indicators Correlation Heatmap")
    corr = df[CORR_COLS].corr()
    fig8 = px.imshow(corr, text_auto=True, title="Correlation Between Metrics",
                     color_continuous_scale="RdBu_r", **PLOTLY_STYLE)
    st.plotly_chart(fig8, use_container_width=True, config=PLOTLY_CONFIG)