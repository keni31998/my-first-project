# Multi-Company Financial Interactive Analysis System

1. Project Overview 

This is an interactive financial analysis tool for multi-company performance comparison. Users can freely select companies and years to view 8 professional charts, and get automatic smart analysis conclusions.


2. Problem & User 

Help investors, students, and analysts quickly compare corporate revenue, profit, margin, growth, assets, and market share through visual charts.


3. Data Source

Database: WRDS Compustat (comp.funda)

Period: 2018–2023

Fields: revenue, net profit, assets, profit margin, growth rate, market share

NYSE/NASDAQ：AAPL，AMZN，DIS，GOOGL，HD，INTC，JPM，MA，META，MSFT，NVDA，PG，TSLA，V，WMT


5. Methods & Tools 

Language: Python 3.9+

Platform: Streamlit

Charts: Matplotlib (Macaron color scheme)

Data: WRDS + Excel


6. Core Functions 

(1)Annual Revenue Comparison

(2)Annual Net Profit Trend

(3)Revenue Share Pie Chart

(4)Profit Contribution Bar Chart

(5)Annual Revenue Growth Rate

(6)Net Profit Margin Ranking

(7)Annual Asset Scale Comparison

(8)Comprehensive Capability Radar Chart + Score Table


7. How to Run 

Install dependencies

plaintext

pip install -r requirements.txt

Run the app

plaintext

streamlit run app.py

Select companies and years in the sidebar

View all 8 charts and smart analysis


8. Key Findings 

Large companies have obvious advantages in total revenue and asset scale.
Some tech companies have higher profit margins but unstable growth rates.
Market share is concentrated in a few leading firms.


9. Product Link | 产品链接
（你部署后把 Streamlit 链接贴这里）Demo Video: （贴你的视频链接）


10. Limitations

Data only includes annual reports, no quarterly data.
Does not consider industry differences and macro factors.
Some missing values may affect growth calculation.


11. AI Disclosure 

AI was used to assist code debugging, chart optimization, and README writing. All logic, analysis, and design are completed independently by the author.


12. Files

plaintext

app.py                  # Main Streamlit program

company_finance_data.xlsx  # Financial data

requirements.txt         # Dependencies

README.md                # Project description
