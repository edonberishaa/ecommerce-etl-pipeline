import json 
import csv
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresHook
from datetime import datetime,timedelta


def extract_orders():
    with open('/opt/airflow/dags/input/orders.json','r') as f:
        data = json.load(f)
    with open('/opt/airflow/dags/output/raw_orders.json','w') as f:
        json.dump(data, f)
    print("Orders extracted successfully.")

def transform_orders():
    with open('/opt/airflow/dags/output/raw_orders.json','r') as f:
        data = json.load(f)

    transformed = []
    for order in data:
        order['total_price'] = order['quantity'] * order['unit_price']
        transformed.append(order)
    
    with open('/opt/airflow/dags/output/transformed_orders.csv','w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=transformed[0].keys())
        writer.writeheader()
        writer.writerows(transformed)
    print("Orders transformed successfully.")

def load_orders():
    hook = PostgresHook(postgres_conn_id='postgres_ecom')
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
                   order_id TEXT PRIMARY KEY,
                   product TEXT,
                   quantity INT,
                   unit_price FLOAT,
                   total_price FLOAT,
                   timestamp TEXT)
    ''')

    with open('/opt/airflow/dags/output/transformed_orders.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT INTO orders (order_id, product, quantity, unit_price, total_price, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
                ''', (row['order_id'], row['product'], int(row['quantity']), row['unit_price'], float(row['total_price']), row['timestamp']))
    conn.commit()
    cursor.close()
    conn.close()
    print("Orders loaded into database successfully.")

default_args = {
    'owner': 'edon',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id = 'ecom_orders_dag',
    default_args=default_args,
    description='ETL Pipeline for e-commerce orders',
    start_date=datetime(2024,6,1),
    schedule_interval='@hourly',
    catchup=False,
    tags=['ecommerce', 'etl']
) as dag:
    extract_task = PythonOperator(
        task_id='extract_orders',
        python_callable=extract_orders,
    )

    transform_task = PythonOperator(
        task_id='transform_orders',
        python_callable=transform_orders,
    )

    load_task = PythonOperator(
        task_id='load_orders',
        python_callable=load_orders,
    )

    extract_task >> transform_task >> load_task