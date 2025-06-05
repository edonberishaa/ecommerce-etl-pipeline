import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine("postgresql+psycopg2://airflow:airflow@localhost:5432/airflow")

df = pd.read_sql("SELECT * FROM orders ORDER BY timestamp ASC",engine)

st.title("E-Commerce Orders Dashboard")

if df.empty:
    st.warning("No data found. Make sure the ETL process has run successfully.")
else:
    total_revenue = df['total_price'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")    

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    revenue_time = df.groupby(df['timestamp'].dt.date)['total_price'].sum().reset_index()
    revenue_time.columns = ['Date', 'Revenue']

    st.subheader("Revenue Over Time")
    st.line_chart(revenue_time.set_index('Date'))

    best_sellers = df.groupby('product')['quantity'].sum().sort_values(ascending=False)

    st.subheader("Best Selling Products")
    st.bar_chart(best_sellers)

    with st.expander("View All Orders"):
        st.dataframe(df)