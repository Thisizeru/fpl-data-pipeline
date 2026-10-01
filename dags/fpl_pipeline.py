from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def extract_fpl_standings():
    import sys
    sys.path.insert(0, '/opt/airflow')
    from Extraction_file.extract import extract_fpl_standings as _extract
    _extract()

def process_fpl_standings():
    import sys
    sys.path.insert(0, '/opt/airflow')
    from Transformation_file.processing import process_fpl_standings as _process
    _process()

def load_fpl_standings():
    import sys
    sys.path.insert(0, '/opt/airflow')
    from Load_file.load import load_fpl_standings as _load
    _load()

with DAG(
    dag_id='fpl_pipeline',
    default_args=default_args,
    description='Beautiful and brutal FPL data pipeline',
    schedule='@daily',
    start_date=datetime(2026, 4, 14),
    end_date=datetime(2027, 5, 30),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_fpl_standings',
        python_callable=extract_fpl_standings
    )

    transform_task = PythonOperator(
        task_id='process_fpl_standings',
        python_callable=process_fpl_standings
    )

    load_task = PythonOperator(
        task_id='load_fpl_standings',
        python_callable=load_fpl_standings
    )

    extract_task >> transform_task >> load_task