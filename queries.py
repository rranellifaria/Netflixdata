# queries.py

def metrics_query_base():
    return """
    SELECT
    COUNT(DISTINCT CASE WHEN tc.type = 'movie' THEN tc.show_id END) AS qtd_filmes_distintos,
    COUNT(DISTINCT CASE WHEN tc.type = 'tv show' THEN tc.show_id END) AS qtd_series_distintos,
    COUNT(DISTINCT tc.country) AS qtd_paises_distintos,
    COUNT(DISTINCT tg.listed_in) AS qtd_generos_distintos
    FROM titles_clean tc
    LEFT JOIN titles_by_genre tg
    ON tc.show_id = tg.show_id
    WHERE 1=1;
    """

def top_countries_query_base():
    return """
    SELECT tc.country, COUNT(*) AS total_titulos
    FROM titles_clean tc
    WHERE 1=1
    GROUP BY tc.country
    ORDER BY total_titulos DESC
    LIMIT 10;
    """

def query_top_genres():
    return """
    SELECT tc.country, COUNT(DISTINCT tg.listed_in) AS qtd_generos_distintos
    FROM titles_clean tc
    LEFT JOIN titles_by_genre tg ON tc.show_id = tg.show_id
    WHERE 1=1
    AND tc.country != 'unknown'   
    GROUP BY tc.country
    ORDER BY qtd_generos_distintos DESC
    LIMIT 10;
    """

def query_movies_tv():
    return """
    SELECT 
    tc.country,
    SUM(CASE WHEN tc.type = 'movie' THEN 1 ELSE 0 END) AS qtd_movies,
    SUM(CASE WHEN tc.type = 'tv show' THEN 1 ELSE 0 END) AS qtd_tvshows
    FROM titles_clean tc
    WHERE tc.country != 'unknown'
    GROUP BY tc.country
    ORDER BY qtd_movies DESC
    LIMIT 10;"""

def query_evolucao():
    return """
    SELECT 
    DATE_TRUNC('month', date_added) AS mes,
    SUM(CASE WHEN type = 'movie' THEN 1 ELSE 0 END) AS qtd_movies,
    SUM(CASE WHEN type = 'tv show' THEN 1 ELSE 0 END) AS qtd_tvshows
    FROM titles_clean
    WHERE date_added IS NOT NULL
    GROUP BY mes
    ORDER BY mes;"""


def query_media_mes():
    return """
    SELECT 
    EXTRACT(MONTH FROM mes_ano) AS mes,
    AVG(qtd_filmes) AS media_filmes
    FROM (
    SELECT 
    DATE_TRUNC('month', date_added) AS mes_ano,
    COUNT(title) AS qtd_filmes
    FROM titles_clean
    WHERE title IS NOT NULL
    AND date_added IS NOT NULL
    GROUP BY mes_ano
    ) AS filmes_por_mes
    GROUP BY mes
    ORDER BY media_filmes DESC
    LIMIT 5;
    """

def query_titulos_ano():
    return """
    SELECT 
    release_year,
    COUNT(title) AS total_titulos
    FROM titles_clean
    WHERE title IS NOT NULL
    GROUP BY release_year
    ORDER BY release_year DESC
    """
    
def query_generos():
    return """
    SELECT tg.listed_in AS genero, COUNT(*) AS total_titulos
    FROM titles_clean tc
    LEFT JOIN titles_by_genre tg ON tc.show_id = tg.show_id
    WHERE tg.listed_in IS NOT NULL
    GROUP BY tg.listed_in
    ORDER BY total_titulos DESC
    LIMIT 10;
    """

def query_generos_ano():
    return """
    SELECT release_year, COUNT(DISTINCT tg.listed_in) AS qtd_generos_distintos
    FROM titles_clean tc
    LEFT JOIN titles_by_genre tg ON tc.show_id = tg.show_id
    WHERE tg.listed_in IS NOT NULL
    GROUP BY release_year
    ORDER BY release_year;
    """

def query_duracao_medias():
    return """
    SELECT 
    AVG(CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER)) AS duracao_media_filmes,
    (SELECT AVG(CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER))
    FROM titles_clean
    WHERE type ILIKE 'tv show' AND duration ~ '[0-9]') AS duracao_media_series
    FROM titles_clean
    WHERE type ILIKE 'movie' AND duration ~ '[0-9]';
    """

def query_top5_filmes():
    return """
    SELECT title, CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER) AS duracao
    FROM titles_clean
    WHERE type ILIKE 'movie' AND duration ~ '[0-9]'
    ORDER BY duracao DESC
    LIMIT 5;
    """

def query_top5_series():
    return """
    SELECT title, CAST(REGEXP_REPLACE(duration, '[^0-9]', '', 'g') AS INTEGER) AS temporadas
    FROM titles_clean
    WHERE type ILIKE 'tv show' AND duration ~ '[0-9]'
    ORDER BY temporadas DESC
    LIMIT 5;
    """

def query_genero_atores():
    return """
    SELECT genero, COUNT(DISTINCT actor) AS qtd_atores_distintos
    FROM (
    SELECT 
    tg.listed_in AS genero,
    TRIM(actor) AS actor
    FROM titles_clean tc
    LEFT JOIN titles_by_genre tg 
    ON tc.show_id = tg.show_id,
    LATERAL unnest(string_to_array(tc."cast", ',')) AS actor
    WHERE tc."cast" IS NOT NULL
    AND tg.listed_in IS NOT NULL
    AND tc."cast" <> 'unknown'
    AND tg.listed_in <> 'unknown'
    ) sub
    GROUP BY genero
    ORDER BY qtd_atores_distintos DESC
    LIMIT 10;"""


def query_total_atores():
    return """
    SELECT COUNT(DISTINCT actor) AS total_atores
    FROM titles_clean,
    LATERAL unnest(string_to_array("cast", ',')) AS actor
    WHERE "cast" IS NOT NULL
    AND "cast" <> 'unknown';"""

def query_total_diretores():
    return """
    SELECT COUNT(DISTINCT director) AS total_diretores
    FROM titles_clean
    WHERE director IS NOT NULL
    AND director <> 'unknown';"""


def query_idade_titles():
    return """
    SELECT rating_age, 
    type, 
    COUNT(*) AS qtd_titulos
    FROM titles_clean
    WHERE rating_age IS NOT NULL
    AND rating_age <> 'unknown'
    GROUP BY rating_age, type
    ORDER BY rating_age, type;"""

def query_maior_genero_idade():
    return """
    SELECT rating_age, genero, qtd_titulos
    FROM (
    SELECT 
    tc.rating_age,
    tg.listed_in AS genero,
    COUNT(*) AS qtd_titulos,
    ROW_NUMBER() OVER (PARTITION BY tc.rating_age ORDER BY COUNT(*) DESC) AS rn
    FROM titles_clean tc
    LEFT JOIN titles_by_genre tg ON tc.show_id = tg.show_id
    WHERE tc.rating_age IS NOT NULL
    AND tc.rating_age <> 'unknown'
    AND tg.listed_in IS NOT NULL
    AND tg.listed_in <> 'unknown'
    GROUP BY tc.rating_age, tg.listed_in
    ) sub
    WHERE rn = 1
    ORDER BY rating_age;
    """