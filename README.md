# Multi-Company Financial Interactive Analysis System
多公司财务交互分析系统

1. Project Overview | 项目概述
This is an interactive financial analysis tool for multi-company performance comparison. Users can freely select companies and years to view 8 professional charts, and get automatic smart analysis conclusions.
这是一个用于多公司财务表现对比的交互式分析工具，用户可自由选择公司与年份，查看 8 类专业图表，并自动获得智能分析结论。

2. Problem & User | 问题与用户
Help investors, students, and analysts quickly compare corporate revenue, profit, margin, growth, assets, and market share through visual charts.
帮助投资者、学生与分析师，通过可视化图表快速对比公司营收、利润、净利率、增长率、资产与市场占比。

3. Data Source | 数据来源
Database: WRDS Compustat (comp.funda)
Period: 2018–2023
Fields: revenue, net profit, assets, profit margin, growth rate, market share
数据库：WRDS Compustat 年度财务数据
时间：2018–2023
字段：营收、净利润、总资产、净利率、增长率、市场占比

4. Methods & Tools | 方法与工具
Language: Python 3.9+
Platform: Streamlit
Charts: Matplotlib (Macaron color scheme)
Data: WRDS + Excel

5. Core Functions | 核心功能
(1)Annual Revenue Comparison
(2)Annual Net Profit Trend
(3)Revenue Share Pie Chart
(4)Profit Contribution Bar Chart
(5)Annual Revenue Growth Rate
(6)Net Profit Margin Ranking
(7)Annual Asset Scale Comparison
(8)Comprehensive Capability Radar Chart + Score Table

6. How to Run | 运行方法
Install dependencies
plaintext
pip install -r requirements.txt
Run the app
plaintext
streamlit run app.py
Select companies and years in the sidebar
View all 8 charts and smart analysis

7. Key Findings | 核心发现
Large companies have obvious advantages in total revenue and asset scale.
Some tech companies have higher profit margins but unstable growth rates.
Market share is concentrated in a few leading firms.
大型公司在营收与资产规模上优势明显
部分科技公司净利率更高，但增长波动较大
市场份额高度集中于头部企业

8. Product Link | 产品链接
（你部署后把 Streamlit 链接贴这里）Demo Video: （贴你的视频链接）

9. Limitations | 局限性
Data only includes annual reports, no quarterly data.
Does not consider industry differences and macro factors.
Some missing values may affect growth calculation.
仅使用年度数据，无季度数据
未考虑行业差异与宏观环境
部分缺失值可能影响增长率计算

10. AI Disclosure | AI 使用说明
AI was used to assist code debugging, chart optimization, and README writing. All logic, analysis, and design are completed independently by the author.
本项目使用 AI 辅助代码调试、图表优化与 README 撰写，所有逻辑、分析与设计均由本人独立完成。

11. Files | 文件结构
plaintext
app.py                  # Main Streamlit program
company_finance_data.xlsx  # Financial data
requirements.txt         # Dependencies
README.md                # Project description
