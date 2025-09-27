import pandas as pd
from config import get_engine
from sqlalchemy import text


def normalize_and_load():
    engine = get_engine()

    # df = pd.read_sql("SELECT * FROM raw_data LIMIT 1000;", engine)
    df = pd.read_sql("SELECT * FROM raw_data;", engine)
    print(df.dtypes)

    # snake case
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    # print("\nColunas")
    # print(df.head())

    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    # print("\nData convertida")
    print(df[['date_added']].head())
    print(df.dtypes['date_added'])

    df['duration'] = df['duration'].fillna('unknown')
    df['duration_value'] = df['duration'].str.extract(r'(\d+)').astype('Int64')
    df['duration_unit'] = df['duration'].str.extract(r'([a-zA-Z]+)')
    # print("\nDepois de separar duration")
    print(df[['duration', 'duration_value', 'duration_unit']].head())
    # print(df.dtypes[['duration_value', 'duration_unit']])

    # valores
    categoria = ['type', 'title', 'director',
                 'cast', 'country', 'rating', 'listed_in']
    for c in categoria:
        if c in df.columns:
            df[c] = df[c].fillna('unknown').astype(
                str).str.lower().replace('nan', 'unknown')

    # rating sem valor
    df['rating'] = df['rating'].fillna('not_rated').astype(
        str).str.lower().replace('nan', 'not_rated').replace('', 'not_rated')

# rating_age
    ratings_ages = {
        'tv-pg': 'older kids',
        'tv-ma': 'adults',
        'tv-y7-fv': 'older kids',
        'tv-y7': 'older kids',
        'tv-14': 'teens',
        'r': 'adults',
        'tv-y': 'kids',
        'nr': 'adults',
        'pg-13': 'teens',
        'tv-g': 'kids',
        'pg': 'older kids',
        'g': 'kids',
        'ur': 'adults',
        'nc-17': 'adults'
    }
    df['rating_age'] = df['rating'].map(ratings_ages).fillna('unknown')

    # print("\nDepois do tratamento de valores:")
    # print(df.head())
    print(df.dtypes)

    df.to_sql('titles_clean', engine, if_exists='replace', index=False)
    print(f"\ntitles_clean criada com sucesso! Total de linhas: {len(df)}")


if __name__ == "__main__":
    normalize_and_load()
