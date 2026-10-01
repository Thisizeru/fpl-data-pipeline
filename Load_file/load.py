import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def load_fpl_standings():
    df = pd.read_csv('/opt/airflow/Transformation_file/processed_fpl_standings.csv')
    
    db_url = URL.create(
        drivername='postgresql+psycopg2',
        username='airflow',
        password='PAUL081eru@@',
        host='postgres',
        port=5432,
        database='fpl_db'
    )
    
    engine = create_engine(db_url)
    
    df.to_sql(
        name='fpl_standings',
        con=engine,
        if_exists='replace',
        index=False
    )
    
    print("Data loaded successfully into the database.")