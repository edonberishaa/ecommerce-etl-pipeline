# 🛍️ E-Commerce Orders ETL Pipeline

This project simulates a real-time data pipeline for processing e-commerce orders using **Apache Airflow**, **PostgreSQL**, and **Streamlit**.

## 📖 Description

The pipeline consists of three ETL stages:

1. **Extract**: Reads order data from a growing JSON file (simulating live transactions).
2. **Transform**: Adds computed fields like `total_price = quantity * unit_price`.
3. **Load**: Inserts the cleaned data into a PostgreSQL database.

It includes a Streamlit dashboard to visualize:

- 💰 Total revenue
- 📈 Revenue over time
- 🥇 Best-selling products

## 🧰 Tools & Technologies

- Apache Airflow
- Python 3
- PostgreSQL 13
- Streamlit
- Docker & Docker Compose

## 🚀 Getting Started

### 1. Start the Airflow environment

```bash
docker compose up -d
Access Airflow at: http://localhost:8080
Username: airflow
Password: airflow

Run the dashboard:
streamlit run dashboards/ecom_dashboard.py


🧠 Author
Edon Berisha
Self-driven Data Engineer in training
GitHub: @edonberishaa
