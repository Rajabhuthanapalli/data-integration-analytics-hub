import streamlit as st
import pandas as pd
import json
from sqlalchemy import create_engine
from src.config import get_settings

st.set_page_config(page_title="DIAH Dashboard", layout="wide")
st.title("Data Integration & Analytics Hub – Quality & Performance")

cfg = get_settings()
engine = create_engine(cfg.database.url, future=True)

# --- Section 1: KPIs ---
st.subheader("📊 Business KPIs")

@st.cache_data(ttl=300)
def run_sql(q):
    return pd.read_sql(q, con=engine)

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
rev = run_sql("SELECT ROUND(COALESCE(SUM(amount_usd),0),2) AS revenue_usd FROM fact_orders;")
ordr = run_sql("SELECT COUNT(*) AS n_orders FROM fact_orders;")
cust = run_sql("SELECT COUNT(DISTINCT customer_id) AS n_customers FROM fact_orders;")
kpi_col1.metric("Revenue (USD)", f"${float(rev['revenue_usd'][0]):,.2f}")
kpi_col2.metric("Orders", int(ordr['n_orders'][0]))
kpi_col3.metric("Customers", int(cust['n_customers'][0]))

# --- Section 2: Validation Results ---
st.subheader("✅ Data Quality Report")

try:
    with open("data/reports/data_quality.json", "r") as f:
        dq = json.load(f)
    dq_df = pd.DataFrame(dq)
    st.dataframe(dq_df, use_container_width=True)
except FileNotFoundError:
    st.warning("No data-quality report found. Please run the pipeline first.")

# --- Section 3: Revenue Trend ---
st.subheader("📈 Revenue Trend")
trend = run_sql("""
SELECT d.order_date, SUM(f.amount_usd) AS revenue_usd
FROM fact_orders f
JOIN dim_date d USING(date_key)
GROUP BY d.order_date
ORDER BY d.order_date;
""")
st.line_chart(trend.set_index("order_date")["revenue_usd"])
