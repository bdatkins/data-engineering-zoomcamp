#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name = params.table_name
    csv_url = params.csv_url
    
    if csv_url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f"wget {csv_url} -O {csv_name}")
    
    connect_str = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
    
    
    engine= create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    
    
    
    print('connect_str: ' + connect_str)
    engine= create_engine(connect_str)

    df_iter = pd.read_csv(csv_name,  iterator=True, chunksize=100000)
    df = next(df_iter)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name='green_taxi_data', con=engine, if_exists='append')

    while True:
        df = next(df_iter)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        print('inserted another chunk')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data into Postgres')
    
    # user, password, host, port, database name, table name,  csv url
    parser.add_argument('--user', help='Postgres user name')
    parser.add_argument('--password', help='Postgres password')
    parser.add_argument('--host', help='Postgres host')
    parser.add_argument('--port', help='Postgres port')
    parser.add_argument('--db_name', help='Postgres database name')
    parser.add_argument('--table_name', help='Postgres table name')
    parser.add_argument('--csv_url', help='CSV Data file URL')

    args = parser.parse_args()
    main(args)






