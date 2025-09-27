# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import run_query
from queries import *

st.set_page_config(page_title="Netflix Data Visualization", layout="wide")

logo_url = "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" 
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="{logo_url}" width="180" style="margin-right: 10px;">
        <h1 style="color:#FFFFFF; margin: 0;">DATA VISUALIZATION</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Filtros")
df_all = run_query("SELECT DISTINCT release_year, rating_age, type FROM titles_clean;")
anos = sorted(df_all['release_year'].dropna().unique())
ano_selecionado = st.sidebar.selectbox("Ano de lançamento", options=["Todos"] + list(anos), index=0)
faixas = sorted(df_all['rating_age'].dropna().unique())
faixa_selecionada = st.sidebar.selectbox("Faixa etária", options=["Todos"] + list(faixas), index=0)
tipos = sorted(df_all['type'].dropna().unique())
tipo_selecionado = st.sidebar.selectbox("Tipo de conteúdo", options=["Todos"] + list(tipos), index=0)

#filtros a uma query
def aplicar_filtros(query: str):
    if ano_selecionado != "Todos":
        query += f" AND release_year = {ano_selecionado}"
    if faixa_selecionada != "Todos":
        query += f" AND rating_age = '{faixa_selecionada}'"
    if tipo_selecionado != "Todos":
        query += f" AND LOWER(TRIM(type)) = '{tipo_selecionado.lower()}'"
    return query


# Metricas gerais
df_metrics = run_query(aplicar_filtros(metrics_query_base()))

st.subheader("Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Filmes distintos", df_metrics['qtd_filmes_distintos'][0])
col2.metric("Séries distintas", df_metrics['qtd_series_distintos'][0])
col3.metric("Países distintos", df_metrics['qtd_paises_distintos'][0])
col4.metric("Gêneros distintos", df_metrics['qtd_generos_distintos'][0])


# Paises com mais titulos

df_countries = run_query(aplicar_filtros(top_countries_query_base()))
#st.markdown("<h2 style='color:white'>Top 10 Países com mais títulos</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])

with col1:
    fig = px.bar(
        df_countries, x="total_titulos", y="country", orientation='h',
        color="total_titulos", color_continuous_scale=["#B81D24", "#E50914"], text="total_titulos",
        height=400
    )
    fig.update_layout(
        title="Top 10 Países com mais títulos",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        xaxis=dict(title="Quantidade de títulos", tickfont=dict(color="white")),
        coloraxis_showscale=False, title_font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)


# Top Paises com generos distintos

df_top_genres = run_query(aplicar_filtros(query_top_genres()))
with col2:
    fig2 = px.bar(
        df_top_genres, x="qtd_generos_distintos", y="country", orientation='h',
        color="qtd_generos_distintos", color_continuous_scale=["#B81D24", "#E50914"], text="qtd_generos_distintos",
        height=400
    )
    fig2.update_layout(
        title="Top 10 Países com mais gêneros distintos",
        title_font_color="white",
        xaxis_title="Quantidade de gêneros distintos",
        yaxis_title="País",
        xaxis=dict(tickfont=dict(color="white")),
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig2, use_container_width=True)


# Moveis VS tv show por paises 

df_movies_tv = run_query(aplicar_filtros(query_movies_tv()))
df_movies_tv_long = df_movies_tv.melt(id_vars='country', value_vars=['qtd_movies', 'qtd_tvshows'],
                                      var_name='tipo', value_name='quantidade')
with col3:
    fig3 = px.bar(
        df_movies_tv_long, x='quantidade', y='country', color='tipo', orientation='h',
        text='quantidade', color_discrete_map={'qtd_movies':'#FFFFFF','qtd_tvshows':'#B81D24'}, height=400
    )
    fig3.update_layout(
        title="Top 10 paises com mais filmes vs series",
        xaxis_title="Quantidade", yaxis_title="País",
        xaxis=dict(tickfont=dict(color="white")),
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text='Tipo', legend=dict(title_font_color='white', font=dict(color='white')),
        title_font_color="white"
    )
    st.plotly_chart(fig3, use_container_width=True)


# Evolução Mensal

df_evolucao = run_query(aplicar_filtros(query_evolucao()))
df_evolucao_long = df_evolucao.melt(id_vars='mes', value_vars=['qtd_movies', 'qtd_tvshows'],
                                    var_name='tipo', value_name='quantidade')
fig = px.line(df_evolucao_long, x='mes', y='quantidade', color='tipo', markers=True,
              color_discrete_map={'qtd_movies':'#E50914', 'qtd_tvshows':'#B81D24'})
fig.update_layout(
    title="Evolução Mensal de Títulos Adicionados à Netflix",
    xaxis_title="Mês/Ano", yaxis_title="Quantidade de Títulos",
    xaxis=dict(tickfont=dict(color="white")), yaxis=dict(tickfont=dict(color="white")),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    legend_title_text='Tipo', legend=dict(title_font_color='white', font=dict(color='white')),
    title_font_color="white"
)
st.plotly_chart(fig, use_container_width=True)


# Media de filmes adicionados por mes 

df_media_mes = run_query(aplicar_filtros(query_media_mes()))
import calendar
df_media_mes['mes_nome'] = df_media_mes['mes'].apply(lambda x: calendar.month_name[int(x)])
col1, col2 = st.columns([1,1])
with col1:
    fig = px.bar(df_media_mes, x='media_filmes', y='mes_nome', orientation='h', text='media_filmes',
                 color='media_filmes', color_continuous_scale=["#B81D24","#E50914"], height=400)
    fig.update_layout(
        title="Top 5 Meses com Maior Média de Filmes Adicionados",
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        xaxis=dict(tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, title_font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)


# Quantidade de titulos por ano de lançamento

df_titulos_ano = run_query(aplicar_filtros(query_titulos_ano()))
with col2:
    fig_ano = px.bar(df_titulos_ano, x='release_year', y='total_titulos', text='total_titulos',
                     color='total_titulos', color_continuous_scale=["#B81D24", "#E50914"], height=400)
    fig_ano.update_layout(
        title="Quantidade de Títulos por Ano",
        xaxis_title="Ano", yaxis_title="Quantidade de Títulos",
        xaxis=dict(tickfont=dict(color="white")), yaxis=dict(tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
        title_font_color="white"
    )
    st.plotly_chart(fig_ano, use_container_width=True)


# Top generos

df_generos = run_query(aplicar_filtros(query_generos()))
with col1:
    fig_generos = px.bar(df_generos, x='total_titulos', y='genero', orientation='h', text='total_titulos',
                         color='total_titulos', color_continuous_scale=["#B81D24","#E50914"], height=400)
    fig_generos.update_layout(
        title="Top 10 Gêneros com Maior Participação",
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        xaxis=dict(tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, title_font_color="white"
    )
    st.plotly_chart(fig_generos, use_container_width=True)


#Evolução generos distintos por ano

df_generos_ano = run_query(aplicar_filtros(query_generos_ano()))
with col2:
    fig_generos_ano = px.line(df_generos_ano, x='release_year', y='qtd_generos_distintos', markers=True)
    fig_generos_ano.update_traces(line=dict(color="#E50914", width=3), marker=dict(size=8, color="#E50914"))
    fig_generos_ano.update_layout(
        title="Evolução da Quantidade de Gêneros Distintos por Ano",
        xaxis=dict(tickfont=dict(color="white")), yaxis=dict(tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", title_font_color="white"
    )
    st.plotly_chart(fig_generos_ano, use_container_width=True)


#Duração média filmes e series

df_medias = run_query(aplicar_filtros(query_duracao_medias()))
duracao_media_filmes = df_medias['duracao_media_filmes'][0]
duracao_media_series = df_medias['duracao_media_series'][0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    fig_filme = go.Figure(go.Indicator(mode="number", value=duracao_media_filmes,
                                       number={"font":{"size":40,"color":"white"}},
                                       title={"text":"Média de filmes (min)","font":{"size":20,"color":"white"}}))
    fig_filme.update_layout(paper_bgcolor="#E50914", height=200, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig_filme, use_container_width=True)

with col2:
    fig_series = go.Figure(go.Indicator(mode="number", value=duracao_media_series,
                                        number={"font":{"size":40,"color":"white"}},
                                        title={"text":"Média de séries (temporadas)","font":{"size":20,"color":"white"}}))
    fig_series.update_layout(paper_bgcolor="#E50914", height=200, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig_series, use_container_width=True)


# Top 5 filmes e series mais longos

df_top5_filmes = run_query(aplicar_filtros(query_top5_filmes()))
df_top5_series = run_query(aplicar_filtros(query_top5_series()))

with col3:
    fig_filmes = px.bar(df_top5_filmes, x='duracao', y='title', orientation='h', text='duracao',
                        color='duracao', color_continuous_scale=["#B81D24","#E50914"], height=400)
    fig_filmes.update_layout(title="Top 5 Filmes mais longos",
                             xaxis_title="Duração (min)", yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
                             plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
                             title_font_color="white")
    st.plotly_chart(fig_filmes, use_container_width=True)

with col4:
    fig_series = px.bar(df_top5_series, x='temporadas', y='title', orientation='h', text='temporadas',
                        color='temporadas', color_continuous_scale=["#B81D24","#E50914"], height=400)
    fig_series.update_layout(title="Top 5 Séries com mais temporadas",
                             xaxis_title="Temporadas", yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
                             plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
                             title_font_color="white")
    st.plotly_chart(fig_series, use_container_width=True)



# Métricas gerais
col1, col2 = st.columns(2)

# Total de atores distintos
query = query_total_atores()

df_total_atores = run_query(query)
total_atores = int(df_total_atores['total_atores'][0])

# Total de diretores distintos
query = query_total_diretores()
df_total_diretores = run_query(query)
total_diretores = int(df_total_diretores['total_diretores'][0])

col1.metric("Total de Atores Distintos", total_atores)
col2.metric("Total de Diretores Distintos", total_diretores)


# Top diretores e atores

df = run_query("SELECT * FROM titles_clean;")

col1, col2 = st.columns(2)

# Top Diretores
with col1:
    df_director = df['director'].dropna().str.strip()
    df_director = df_director[df_director.str.lower() != 'unknown']
    df_director_counts = df_director.value_counts().head(10).reset_index()
    df_director_counts.columns = ['director','qtd_titulos']
    fig_director = px.bar(df_director_counts, x='qtd_titulos', y='director', orientation='h', text='qtd_titulos',
                          color='qtd_titulos', color_continuous_scale=["#B81D24","#E50914"], height=400)
    fig_director.update_layout(
        title="Top 10 Diretores com Mais Títulos",
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        xaxis=dict(tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, title_font_color="white"
    )
    st.plotly_chart(fig_director, use_container_width=True)

# Top Atores
with col2:
    df_cast = df['cast'].dropna().str.split(',')
    df_cast = df_cast.explode().str.strip()
    df_cast = df_cast[df_cast.str.lower() != 'unknown']
    df_cast_counts = df_cast.value_counts().head(10).reset_index()
    df_cast_counts.columns = ['actor','qtd_titulos']
    fig_cast = px.bar(df_cast_counts, x='qtd_titulos', y='actor', orientation='h', text='qtd_titulos',
                      color='qtd_titulos', color_continuous_scale=["#B81D24","#E50914"], height=400)
    fig_cast.update_layout(
        title="Top 10 Atores com Mais Títulos",
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        xaxis=dict(tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, title_font_color="white"
    )
    st.plotly_chart(fig_cast, use_container_width=True)


# Diversidade de elenco

col1, col2 = st.columns(2)

with col1:
    #st.subheader("Diretores com maior diversidade de elenco")

    df_diversidade = df.dropna(subset=['director', "cast"]).copy()
    df_diversidade = df_diversidade[df_diversidade['director'].str.lower() != 'unknown']
    df_diversidade = df_diversidade[df_diversidade["cast"].str.lower() != 'unknown']

    df_diversidade = df_diversidade.assign(actor=df_diversidade["cast"].str.split(',')).explode('actor')
    df_diversidade['actor'] = df_diversidade['actor'].str.strip()

    # atores distintos por diretor
    df_diversidade_count = (
        df_diversidade.groupby('director')['actor']
        .nunique()
        .reset_index(name='atores_distintos')
        .sort_values(by='atores_distintos', ascending=False)
        .head(10)
    )

    fig_diversidade = px.bar(
        df_diversidade_count,
        x='atores_distintos',
        y='director',
        orientation='h',
        text='atores_distintos',
        color='atores_distintos',
        color_continuous_scale=["#B81D24", "#E50914"],
        height=400
    )
    fig_diversidade.update_layout(
        title="Diretores com maior diversidade de elenco",
        yaxis=dict(autorange="reversed", tickfont=dict(color="white")),
        xaxis=dict(title="Quantidade de Atores Distintos", tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font_color="white",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_diversidade, use_container_width=True)

# Top gêneros por quantidade de atores distintos 
with col2:
    query = query_genero_atores()
    df_genero_atores = run_query(query)

    fig_genero_atores = px.bar(
        df_genero_atores,
        x="genero",
        y="qtd_atores_distintos",
        text="qtd_atores_distintos",
        color="qtd_atores_distintos",
        color_continuous_scale=["#B81D24", "#E50914"],
        height=500
    )

    fig_genero_atores.update_layout(
        title="Top 10 Gêneros com Maior Quantidade de Atores Distintos",
        title_font_color="white",
        xaxis=dict(title="Gênero", tickfont=dict(color="white")),
        yaxis=dict(title="Atores Distintos", tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_genero_atores, use_container_width=True)

# Rating

st.subheader("Análises por Faixa Etária")

col1, col2 = st.columns(2)

#Qtd de Filmes e Séries por rating age
with col1:
    query = query_idade_titles()
    df_idade_titles = run_query(query)

    fig_idade_titles = px.bar(
        df_idade_titles,
        x="rating_age",
        y="qtd_titulos",
        color="type",
        barmode="group",
        text="qtd_titulos",
        color_discrete_sequence=["#E50914", "#B81D24"],
        height=450
    )

    fig_idade_titles.update_layout(
        title="Quantidade de Filmes e Séries por Faixa Etária",
        title_font_color="white",
        xaxis=dict(title="Faixa Etária", tickfont=dict(color="white")),
        yaxis=dict(title="Quantidade de Títulos", tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Tipo"
    )

    st.plotly_chart(fig_idade_titles, use_container_width=True)

#Maior Gênero por rating age
with col2:
    query = query_maior_genero_idade()
    df_genero_idade = run_query(query)

    fig_genero_idade = px.bar(
        df_genero_idade,
        x="rating_age",
        y="qtd_titulos",
        color="genero",
        text="qtd_titulos",
        color_discrete_sequence=["#E50914", "#B81D24"],
        height=450
    )

    fig_genero_idade.update_layout(
        title="Títulos por Gênero e Faixa Etária",
        title_font_color="white",
        xaxis=dict(title="Faixa Etária", tickfont=dict(color="white")),
        yaxis=dict(title="Quantidade de Títulos", tickfont=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_genero_idade, use_container_width=True)