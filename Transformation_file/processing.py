import pandas as pd
def process_fpl_standings():
# Load the CSV file into a DataFrame
    df = pd.read_csv('/opt/airflow/Extraction_file/Fpl_standings.csv')
    print(df.head()) 

# Rename columns to match the database schema
    df = df.rename(columns={
       'id': 'player_id',
       'event_total': 'matchweek_points',
       'last_rank': 'last_matchweek_rank',
       'total': 'total_points',
       'entry': 'unique_id',
       'entry_name': 'team_name'
    })
#making sure the data types are correct for the database
    print(df.dtypes)

    print(df.isna().sum())  

    print(df.duplicated())

    df.to_csv('/opt/airflow/Transformation_file/processed_fpl_standings.csv', index=False)
    print("everything is okay")