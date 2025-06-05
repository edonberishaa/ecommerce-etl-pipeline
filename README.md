# 🛰️ Weather ETL Pipeline (Airflow + PostgreSQL + Streamlit)

## 📖 Description
This project extracts weather data from Open-Meteo API using Apache Airflow, transforms the data, and stores it in a PostgreSQL database. It includes a real-time Streamlit dashboard to visualize the latest weather.

## 🔧 Tools
- Apache Airflow
- Python
- PostgreSQL
- Streamlit
- Docker

## ⚙️ Pipeline Stages
1. **Extract**: fetches weather from API
2. **Transform**: formats and cleans the data
3. **Load**: saves into PostgreSQL
4. **Visualize**: real-time dashboard with Streamlit

## 📦 How to Run
```bash
docker compose up -d
