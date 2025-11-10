import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.config import get_settings

st.set_page_config(page_title="DIAH Dashboard", layout="wide")
st.title("Data Integration & Analytics Hub")

cfg = get_settings()
engine = create_engine(cfg.database.url, future=True)

@st.cache_data(ttl=300)
def run_sql(q):
    return pd.read_sql(q, con=engine)

# KPI tiles
col1, col2, col3 = st.columns(3)
rev = run_sql("SELECT ROUND(COALESCE(SUM(amount_usd),0),2) AS revenue_usd FROM fact_orders;")
ordr = run_sql("SELECT COUNT(*) AS n_orders FROM fact_orders;")
cust = run_sql("SELECT COUNT(*) AS n_customers FROM dim_customer;")
col1.metric("Revenue (USD)", f"${float(rev['revenue_usd'][0]):,.2f}")
col2.metric("Orders", int(ordr['n_orders'][0]))
col3.metric("Customers", int(cust['n_customers'][0]))

# Filters
st.sidebar.header("Filters")
min_date = run_sql("SELECT MIN(order_date) AS d FROM dim_date;")["d"][0]
max_date = run_sql("SELECT MAX(order_date) AS d FROM dim_date;")["d"][0]
date_range = st.sidebar.date_input("Order Date Range", value=(min_date, max_date))
region = st.sidebar.selectbox("Region", options=["All","US","EU","UK","IN"], index=0)

# Build where clause
where = []
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    where.append(f"d.order_date BETWEEN '{start}' AND '{end}'")
if region != "All":
    where.append(f"c.region = '{region}'")
where_sql = ("WHERE " + " AND ".join(where)) if where else ""

# Trend
st.subheader("Revenue Trend")
trend_q = f"""
SELECT d.order_date, ROUND(SUM(f.amount_usd),2) AS revenue_usd, COUNT(*) AS orders
FROM fact_orders f
JOIN dim_date d USING(date_key)
JOIN dim_customer c USING(customer_id)
{where_sql}
GROUP BY d.order_date
ORDER BY d.order_date;
"""
trend = run_sql(trend_q)
if not trend.empty:
    st.line_chart(trend.set_index("order_date")[["revenue_usd"]])
else:
    st.info("No data for selected filters.")

# Detail table
st.subheader("Orders")
detail_q = f"""
SELECT f.order_id, d.order_date, f.customer_id, c.region, f.currency, f.amount, f.amount_usd
FROM fact_orders f
JOIN dim_date d USING(date_key)
JOIN dim_customer c USING(customer_id)
{where_sql}
ORDER BY d.order_date DESC, f.order_id DESC;
"""
st.dataframe(run_sql(detail_q), use_container_width=True)
