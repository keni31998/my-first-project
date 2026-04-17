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

# Page Setup
st.set_page_config(page_title="Multi-Company Comparison", layout="wide")
st.title("📊 Multi-Company Business Analysis System")
st.sidebar.header("⚙️ Settings")

# ----------------------
# 1) WRDS Login
# ----------------------
st.sidebar.subheader("🔐 WRDS Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

db = None
if st.sidebar.button("Login"):
    try:
        db = wrds.Connection(wrds_username=username, wrds_password=password)
        st.sidebar.success("✅ Login Successful")
        st.session_state['db'] = db
    except:
        st.sidebar.error("❌ Login Failed")

# ----------------------
# 2) Enter Companies & Years
# ----------------------
tickers_str = st.sidebar.text_input("Company Tickers (comma-separated)", "AAPL,MSFT,TSLA")
start_year = st.sidebar.number_input("Start Year", 2015, 2025, 2018)
end_year = st.sidebar.number_input("End Year", 2015, 2025, 2023)

# ----------------------
# 3) Load Data
# ----------------------
if st.sidebar.button("🚀 Load Data"):
    if 'db' not in st.session_state:
        st.warning("Please log in to WRDS first!")
        st.stop()

    db = st.session_state['db']
    tickers = [t.strip().upper() for t in tickers_str.split(",")]

    # Fetch data from WRDS
    dfs = []
    for tic in tickers:
        sql = f"""
            SELECT
                '{tic}' AS company,
                fyear,
                sale     AS revenue,
                ni       AS profit,
                at       AS assets,
                (ni/sale) AS profit_margin
            FROM comp.funda
            WHERE tic = '{tic}'
              AND fyear BETWEEN {start_year} AND {end_year}
        """
        df = db.raw_sql(sql)
        dfs.append(df)

    df = pd.concat(dfs)
    df = df.groupby(["company", "fyear"]).last().reset_index()
    df["fyear"] = df["fyear"].astype(int)

    # Calculate growth rates
    df = df.sort_values(["company", "fyear"])
    df["revenue_growth"] = df.groupby("company")["revenue"].pct_change() * 100
    df["profit_growth"] = df.groupby("company")["profit"].pct_change() * 100

    # Annual shares
    year_total = df.groupby("fyear")[["revenue", "profit", "assets"]].sum().reset_index()
    year_total.columns = ["fyear", "total_rev", "total_prof", "total_ast"]
    df = df.merge(year_total, on="fyear")
    df["rev_share"] = df["revenue"] / df["total_rev"] * 100
    df["prof_share"] = df["profit"] / df["total_prof"] * 100

    st.session_state['df'] = df
    st.success("✅ Data loaded successfully!")
    st.dataframe(df.round(2), use_container_width=True)

# ----------------------
# Data Visualization (Enhanced)
# ----------------------
if 'df' in st.session_state:
    df = st.session_state['df']
    years = sorted(df['fyear'].unique())
    companies = sorted(df['company'].unique())

    st.divider()
    st.subheader("📊 Enhanced Data Visualization")

    # ==============================================
    # 🔥 新增：KPI 关键指标卡片（顶级可视化）
    # ==============================================
    st.subheader("🎯 Key Performance Indicators")
    latest_year = df['fyear'].max()
    latest = df[df['fyear'] == latest_year]

    cols = st.columns(len(companies))
    for i, comp in enumerate(companies):
        c_data = latest[latest['company'] == comp]
        if not c_data.empty:
            rev = c_data['revenue'].values[0]
            profit = c_data['profit'].values[0]
            margin = c_data['profit_margin'].values[0] * 100

            with cols[i]:
                st.metric(label=f"{comp} Revenue", value=f"${rev:,.0f}")
                st.metric(label="Net Profit", value=f"${profit:,.0f}")
                st.metric(label="Profit Margin %", value=f"{margin:.1f}%")

    st.divider()

    # ==============================================
    # 1. 交互式营收趋势（Plotly）
    # ==============================================
    st.subheader("1️⃣ Annual Revenue Trend (Interactive)")
    fig1 = px.line(df, x="fyear", y="revenue", color="company",
                   title="Revenue Trend by Company",
                   template="plotly_white", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # ==============================================
    # 2. 交互式净利润柱状图
    # ==============================================
    st.subheader("2️⃣ Net Profit Comparison")
    fig2 = px.bar(df, x="fyear", y="profit", color="company",
                  title="Net Profit by Year & Company",
                  template="plotly_white", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    # ==============================================
    # 3. 营收占比饼图
    # ==============================================
    st.subheader("3️⃣ Revenue Market Share")
    y_pie = st.selectbox("Select Year for Share", years, key="pie")
    pie_data = df[df['fyear'] == y_pie]
    fig3 = px.pie(pie_data, values="rev_share", names="company",
                  title=f"Revenue Share {y_pie}", hole=0.3)
    st.plotly_chart(fig3, use_container_width=True)

    # ==============================================
    # 4. 净利率排名
    # ==============================================
    st.subheader("4️⃣ Profit Margin Ranking")
    y_margin = st.selectbox("Select Year", years, key="margin")
    mar_data = df[df['fyear'] == y_margin].sort_values("profit_margin")
    fig4 = px.barh(mar_data, x="profit_margin", y="company",
                   title=f"Profit Margin Ranking {y_margin}",
                   labels={"profit_margin": "Profit Margin"})
    st.plotly_chart(fig4, use_container_width=True)

    # ==============================================
    # 5. 营收增长率对比
    # ==============================================
    st.subheader("5️⃣ Revenue Growth Rate Trend")
    fig5 = px.line(df, x="fyear", y="revenue_growth", color="company",
                   markers=True, title="Revenue Growth (%)")
    st.plotly_chart(fig5, use_container_width=True)

    # ==============================================
    # 6. 资产规模面积图
    # ==============================================
    st.subheader("6️⃣ Total Assets Trend")
    fig6 = px.area(df, x="fyear", y="assets", color="company",
                   title="Asset Size Comparison")
    st.plotly_chart(fig6, use_container_width=True)

    # ==============================================
    # 7. 综合能力雷达图
    # ==============================================
    st.subheader("7️⃣ Comprehensive Capability Radar Chart")
    y_radar = st.selectbox("Select Year", years, key="radar")
    radar_df = df[df["fyear"] == y_radar].copy()

    indicators = ["Revenue", "Profit", "Profit Margin", "Growth", "Assets"]
    rad_cols = st.columns(len(radar_df))

    for i, (_, row) in enumerate(radar_df.iterrows()):
        values = [
            row["revenue"] / radar_df["revenue"].max() * 10,
            row["profit"] / radar_df["profit"].max() * 10,
            row["profit_margin"] * 10,
            max(row["revenue_growth"], 0) / 50 * 10 if pd.notna(row["revenue_growth"]) else 0,
            row["assets"] / radar_df["assets"].max() * 10
        ]
        values += values[:1]
        angles = [n / 5 * 2 * pi for n in range(5)]
        angles += angles[:1]

        with rad_cols[i]:
            fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'polar': True})
            ax.plot(angles, values, linewidth=2)
            ax.fill(angles, values, alpha=0.3)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(indicators)
            plt.title(f"{row.company} {y_radar}")
            st.pyplot(fig)

    # ==============================================
    # 8. 新增：相关性热力图（高级可视化）
    # ==============================================
    st.divider()
    st.subheader("8️⃣ Financial Indicators Correlation Heatmap")
    corr_cols = ["revenue", "profit", "assets", "profit_margin", "revenue_growth"]
    corr = df[corr_cols].corr()
    fig8 = px.imshow(corr, text_auto=True, title="Correlation Between Metrics")
    st.plotly_chart(fig8, use_container_width=True)