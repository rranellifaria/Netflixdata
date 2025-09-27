# Netflix Data Pipeline & Dashboard  

Projeto de análise de dados da Netflix em Streamlit.  

---

## 📂 Estrutura do Projeto  

```bash
.
├── env/                 # Ambiente virtual Python
├── netflix_titles.csv   # Dataset extraído do Kaggle
├── config.py            # Configuração e conexão com banco (PostgreSQL)
├── extract_kaggle.py    # Script para baixar e extrair dados do Kaggle
├── load_raw.py          # Cria tabela 'raw_data' e insere dados brutos no banco
├── tratamento.py        # Limpeza, padronização e criação da tabela 'titles_clean'
├── new_tables.py        # Criação de tabelas derivadas (titles_by_country, titles_by_genre)
├── queries.py           # Conjunto de queries SQL para o dashboard
├── dash.py              # Dashboard em Streamlit
└── README.md            # Este arquivo
```


## 1. Criação do Banco de Dados

O banco de dados foi criado utilizando o **Aiven**, um serviço de banco de dados gerenciado na nuvem.  
A escolha foi por
- Facilidade de criação do bancos   

<img width="1563" height="172" alt="image" src="https://github.com/user-attachments/assets/6f8a0e60-bc89-4796-a41a-f7c8ba58b032" />

## 2. Criação do Ambiente Virtual

Um ambiente virtual Python (`venv`) foi criado 


## 3. Configuração de Conexão com o Banco

O Script `config.py` é onde está as configurações de conexão

- **`get_connection()`**: conexão direta via `psycopg2`
- **`get_engine()`**: cria uma **engine SQLAlchemy**, para as operaões `pandas` facilitar na criação dos graficos


## 4. Extração e Inserção da Base de Dados

Foram criados dois scripts 

- **`Extração`**:

Busca os dados da Netflix utilizando a API do Kaggle. Gera um arquivo CSV local.

- **`Inserção`**: 

O Script `load_raw.py` inseri os dados brutos no banco.  

- Criação da tabela `raw_data`:  

## 5. Tratamento de Dados

O script `tratamento.py` realiza o processamento utiliza `pandas` e `SQLAlchemy` para manipular os dados e por no banco de dados.

- **`Leitura dos dados brutos`**:  
   - Os dados são carregados da tabela `raw_data` .

- **`Padronização das colunas`**:  
   - colunas são convertidas para `snake_case`.

- **`Conversão de datas`**: 
   - A coluna `date_added` é convertida para `datetime`.
   
- **`Tratamento da coluna `duration``**:  
   - Valores nulos são substituídos por `"unknown"`.
   - A coluna dividida 
     - `duration_value`: valor numérico
     - `duration_unit`: unidade (ex.: min ou season)

- **`Padronização de valores categóricos**:  
    - nulos substituídos por `"unknown"` 

- **`Criação da coluna `rating_age`**:  
   - Classificações (`tv-ma`, `pg-13`, etc.) para para faixas etárias (`kids`, `teens`, `adults`, `older kids`).
  de acordo com https://www.amazon.com/gp/help/customer/display.html?nodeId=G2C2CPZWGZWHZ42J

## 6. Criação de Novas Tabelas

O script `new_tables.py` criar tabelas  a partir da `titles_clean`,

 `country` e `listed_in`, têm vários valores separados por vírgula. O `explode` transforma cada valor em uma linha separada, mantendo o `show_id`  
- `str.split()` e `str.strip()` ajudam a separar e limpar os valores.  

<img width="546" height="239" alt="image" src="https://github.com/user-attachments/assets/cf496028-2dab-4a89-8abc-a958a1113117" />


 ## 7. Análises e Queries

O arquivo `queries.py`, que tem todas as queries SQL utilizadas nas análises e no dashboards 
 
## 8. Dashboard 

O arquivo `dash.py`, que cria um dashboard








