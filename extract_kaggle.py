import os
import zipfile
import pandas as pd

def baixar_dataset(slug: str, destino: str = "."):
    cmd = f'kaggle datasets download -d {slug} -p {destino} --force'
    os.system(cmd)

    
    for arquivo in os.listdir(destino):
        if arquivo.endswith(".zip"):
            caminho_zip = os.path.join(destino, arquivo)
            #print("funciona ate aqui")
            #print(caminho_zip)
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                for nome in zip_ref.namelist():
                    if nome.endswith(".csv"):
                        zip_ref.extract(nome, destino)
                        caminho_csv = os.path.join(destino, nome)
            os.remove(caminho_zip)  
            return caminho_csv  

def carregar_como_dataframe(caminho_csv: str) -> pd.DataFrame:
    print("Carregando CSV:", caminho_csv)
    return pd.read_csv(caminho_csv)

if __name__ == "__main__":
    slug_do_dataset = "shivamb/netflix-shows"
    caminho_csv = baixar_dataset(slug_do_dataset, destino=".")
    df = carregar_como_dataframe(caminho_csv)
    #print(df.head())
    #print("Shape:", df.shape)
