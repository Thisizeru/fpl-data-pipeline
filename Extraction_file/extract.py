import requests
import pandas as pd
import time

SAVE_RESULTS = True

def extract_fpl_standings():
    league_id = 1105020
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings=1&t={int(time.time())}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Referer': 'https://fantasy.premierleague.com/',
        'Origin': 'https://fantasy.premierleague.com',
    }

    cookies = {
        'global_sso_id': 'cb5956df-4150-4578-90c8-5b0bc3c37ec4',
        'datadome': 'wth~gyP6FoO~RZ82FeXpu7kudTEeiEwQ3sxoS96eZtG9SMXDvkSG7QA45f63n8s6zcZuCj2lCySoJhU46wFDd1E3HqjL8YW4kPvJbTV9OfJl~WaUsCrdL0xSQ2KPMw41',
    }

    response = requests.get(url, headers=headers, cookies=cookies, timeout=60)

    if response.status_code == 200:
        data = response.json()
        standings_data = data['standings']['results']
        df = pd.DataFrame(standings_data)
        print(df.head())

        if SAVE_RESULTS:
            df.to_csv('/opt/airflow/Extraction_file/Fpl_standings.csv', index=False)
            df.to_json('/opt/airflow/Extraction_file/Fpl_standings.json', orient='records', lines=True)
            print("Data saved to Fpl_standings.csv")
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")