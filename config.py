import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode="require" 
        )
        print("ok")
        return conn
    except Exception as e:
        print("Erro", e)
        return None




def get_engine():
    try:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")

        # adiciona sslmode se necessário
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}?sslmode=require"

        engine = create_engine(url)
        return engine

    except Exception as e:
        print("Erro:", e)
        return None
    

def run_query(query):
    conn = get_connection()
    if conn:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame()