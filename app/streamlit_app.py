import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.config import get_settings

st.set_page_config(page_title="DIAH Dashboard", layout="wide")
st.title("Data Integration & Analytics Hub")

cfg = get_settings()
engine = create_engine(cfg.database.url, future=True)

@st.cache_data(ttl=300)
def load_df(query):
    return pd.read_sql(query, con=engine)

col1, col2, col3 = st.columns(3)
total = load_df("SELECT SUM(amount_usd) AS revenue_usd FROM fact_orders;")
orders = load_df("SELECT COUNT(*) AS n_orders FROM fact_orders;")
custs  = load_df("SELECT COUNT(*) AS n_customers FROM dim_customer;")

col1.metric("Revenue (USD)", f"${float(total['revenue_usd'][0] or 0):,.2f}")
col2.metric("Orders", int(orders['n_orders'][0]))
col3.metric("Customers", int(custs['n_customers'][0]))

st.subheader("Orders by Date")
by_date = load_df("""
SELECT d.order_date, SUM(f.amount_usd) as revenue_usd, COUNT(*) as orders
FROM fact_orders f
JOIN dim_date d USING(date_key)
GROUP BY d.order_date
ORDER BY d.order_date;
""")
st.line_chart(by_date.set_index("order_date")[["revenue_usd"]])

st.subheader("Orders Table")
st.dataframe(load_df("""
SELECT f.order_id, d.order_date, f.customer_id, f.currency, f.amount, f.amount_usd
FROM fact_orders f
JOIN dim_date d USING(date_key)
ORDER BY d.order_date DESC, f.order_id DESC;
"""))
