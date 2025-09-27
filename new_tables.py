import pandas as pd
from config import get_engine

def normalize_multivalues():
    engine = get_engine()
   
    df = pd.read_sql("titles_clean", engine)
    #print(f"Total de linhas: {len(df)}\n")

    # titles_by_country 
    df_country = df[['show_id', 'country']].copy()
    df_country['country'] = df_country['country'].str.split(',')
    df_country = df_country.explode('country')
    df_country['country'] = df_country['country'].str.strip()
    df_country.to_sql('titles_by_country', engine, if_exists='replace', index=False)
    
    #print(df_country.head(10))
    #print(f"Total de linhas: {len(df_country)}")
    #print(f"showid distintos: {df_country['show_id'].nunique()}")
    #print(f"países distintos: {df_country['country'].nunique()}\n")

    # titles_by_genre
    df_genre = df[['show_id', 'listed_in']].copy()
    df_genre['listed_in'] = df_genre['listed_in'].str.split(',')
    df_genre = df_genre.explode('listed_in')
    df_genre['listed_in'] = df_genre['listed_in'].str.strip()
    df_genre.to_sql('titles_by_genre', engine, if_exists='replace', index=False)
    #print(df_genre.head(10))
    #print(f"Total de linhas: {len(df_genre)}")
    #print(f"show id distintos: {df_genre['show_id'].nunique()}")
    #print(f"Total de gêneros distintos: {df_genre['listed_in'].nunique()}\n")

    # Relacionamento 
    print("Relacionamento via show_id:")
   

if __name__ == "__main__":
    normalize_multivalues()
