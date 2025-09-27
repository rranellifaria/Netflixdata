import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from config import get_connection

def inserir_raw_data(caminho_csv: str, tabela: str = "raw_data"):
    df = pd.read_csv(caminho_csv)

    conn = get_connection()
    cur = conn.cursor()

    # cria a tabela
    cur.execute(f"""
        CREATE TABLE {tabela} (
            show_id TEXT,
            "type" TEXT,
            title TEXT,
            director TEXT,
            "cast" TEXT,
            country TEXT,
            date_added TEXT,
            release_year TEXT,
            rating TEXT,
            duration TEXT,
            listed_in TEXT,
            description TEXT
        );
    """)

    # insere os dados
    cols = ", ".join([f'"{c}"' for c in df.columns])
    insert_sql = f"INSERT INTO {tabela} ({cols}) VALUES %s"
    execute_values(cur, insert_sql, df.values.tolist())

    conn.commit()
    cur.close()
    conn.close()
    print(f"{len(df)} linhas inseridas em '{tabela}'.")

if __name__ == "__main__":
    inserir_raw_data("netflix_titles.csv")
