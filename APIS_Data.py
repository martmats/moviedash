import os
import requests
import pandas as pd
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# My API Key
api_key = os.getenv('API_KEY')

# Base URL
base_url = 'https://api.themoviedb.org/3'
# Base URL for poster images
poster_base_url = 'https://image.tmdb.org/t/p/w500'

# Function to fetch data from TMDB
def fetch_data(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Function to fetch movies
def fetch_movies(url, params, pages):
    movies = []
    for page in range(1, pages + 1):
        params['page'] = page
        page_movies = fetch_data(url, params)['results']
        movies.extend(page_movies)
    return movies

# Function to fetch genres
def fetch_genres():
    genres_url = f'{base_url}/genre/movie/list'
    params = {'api_key': api_key, 'language': 'en-US'}
    genre_data = fetch_data(genres_url, params)['genres']
    genre_dict = {genre['id']: genre['name'] for genre in genre_data}
    return genre_dict

# Function to fetch watch providers using the new endpoint
# JustWatch Attribution and TMDb Required: In order to use this data, you must attribute the source of the data as JustWatch and TMDb.
def fetch_watch_providers(movie_id):
    providers_url = f'{base_url}/movie/{movie_id}/watch/providers'
    params = {
        'api_key': api_key,
        'watch_region': 'GB'
    }
    providers_data = fetch_data(providers_url, params).get('results', {}).get('GB', {}).get('flatrate', [])
    provider_names = [provider['provider_name'] for provider in providers_data]
    provider_release_dates = [provider.get('release_date', None) for provider in providers_data]
    return provider_names, provider_release_dates

# Fetch trending movies
def fetch_trending_movies(media_type, time_window, pages):
    trending_url = f'{base_url}/trending/{media_type}/{time_window}'
    params = {'api_key': api_key, 'region': 'GB'}
    trending_movies = fetch_movies(trending_url, params, pages)
    for movie in trending_movies:
        movie['trending'] = True
    return trending_movies

# Discover movies by year
def discover_movies_by_year(year_from, year_to, pages, genres):
    discover_url = f'{base_url}/discover/movie'
    params = {
        'api_key': api_key,
        'region': 'GB',
        'primary_release_date.gte': f'{year_from}-01-01',
        'primary_release_date.lte': f'{year_to}-12-31',
        'with_genres': genres
    }
    discovered_movies = fetch_movies(discover_url, params, pages)
    for movie in discovered_movies:
        movie['trending'] = False
    return discovered_movies

# Fetch data for the Database
trending_movies = fetch_trending_movies('movie', 'day', 10)  # Fetch 10 pages of trending movies
genres_dict = fetch_genres()
discovered_movies = discover_movies_by_year(2010, datetime.now().year, 200, '28')  # Fetch 200 pages of action movies from 2010 to present

# Combine data
all_movies = trending_movies + discovered_movies
movies_df = pd.DataFrame(all_movies)

# Add genres
movies_df['genres'] = movies_df['genre_ids'].apply(lambda ids: [genres_dict.get(id) for id in ids])

# Fetch providers and provider release dates
provider_data = movies_df['id'].apply(fetch_watch_providers)
movies_df['providers'], movies_df['provider_release_dates'] = zip(*provider_data)

# Convert provider release dates to datetime.date and handle NaT
def convert_to_date(dates):
    converted_dates = []
    for date in dates:
        try:
            converted_dates.append(pd.to_datetime(date).date() if date else None)
        except Exception as e:
            print(f"Error converting date: {date}, Error: {e}")
            converted_dates.append(None)
    return converted_dates

movies_df['provider_release_dates'] = movies_df['provider_release_dates'].apply(convert_to_date)

# Add poster image URL
movies_df['poster_image'] = movies_df['poster_path'].apply(lambda path: f"{poster_base_url}{path}" if path else None)

# Add timestamp
movies_df['timestamp'] = datetime.now()

# Clean and ensure data types are correct
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce').dt.date


# Database credentials
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database=db_name,
    user=db_username,
    password=db_password,
    host=db_host,
    port=db_port
)

# Create a cursor object
cur = conn.cursor()

# Function to create table and upsert data
def create_and_upsert_table(df, schema_name, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER UNIQUE,
        title VARCHAR(255),
        vote_average NUMERIC,
        vote_count INTEGER,
        overview TEXT,
        release_date DATE,
        genres TEXT[],
        providers TEXT[],
        provider_release_dates DATE[],
        poster_image VARCHAR(255),
        trending BOOLEAN,
        timestamp TIMESTAMP
    )
    """
    cur.execute(create_table_query)

    upsert_query = f"""
    INSERT INTO {schema_name}.{table_name} (movie_id, title, vote_average, vote_count, overview, release_date, genres, providers, provider_release_dates, poster_image, trending, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (movie_id) DO UPDATE SET
    title = EXCLUDED.title,
    vote_average = EXCLUDED.vote_average,
    vote_count = EXCLUDED.vote_count,
    overview = EXCLUDED.overview,
    release_date = EXCLUDED.release_date,
    genres = EXCLUDED.genres,
    providers = EXCLUDED.providers,
    provider_release_dates = EXCLUDED.provider_release_dates,
    poster_image = EXCLUDED.poster_image,
    trending = EXCLUDED.trending,
    timestamp = EXCLUDED.timestamp
    """
    for _, row in df.iterrows():
        # Handle NaT values for release_date
        release_date = row['release_date'] if pd.notnull(row['release_date']) else None

        
        cur.execute(upsert_query, (
            row['id'], row['title'], row['vote_average'], row['vote_count'], row['overview'],
            release_date, row['genres'], row['providers'], row['provider_release_dates'],
            row['poster_image'], row['trending'], row['timestamp']
        ))


# Create table and upsert data
create_and_upsert_table(movies_df, 'student', 'movies')

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()



# Ensure proper attribution: Data provided by JustWatch. Attribution is required when using this data