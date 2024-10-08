import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import math

#---------STREAMLIT PAGE CONFIGURATION (Has to be at the beginning)----------------------------------

# Set page configuration to use wide layout
st.set_page_config(layout="wide")

#---------------CONNECT AND LOAD DATA FROM THE DATABASE-----------------------------------

# Load environment variables from Streamlit secrets
db_username = st.secrets["DB_USERNAME"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOST"]
db_port = st.secrets["DB_PORT"]
db_name = st.secrets["DB_NAME"]

# Connect to the PostgreSQL database
def get_connection():
    try:
        return psycopg2.connect(
            database=db_name,
            user=db_username,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Load data from the PostgreSQL database
@st.cache_data
def load_data():
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    query = "SELECT * FROM movies"
    df = pd.read_sql(query, conn)
    conn.close()
    # Ensure the release_date is in datetime format
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    return df

movies_df = load_data()

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply custom CSS
local_css("style.css")

#------------FUNCTIONS FOR EACH PAGE--------------------------------------------

#------------Trendy Pick Page Functions-----------------------------------------
# Get the HotPick for Today
def get_trendy_films_today():
    today = pd.to_datetime('today').normalize()
    # Normalize the release_date column to ensure the comparison is done only on the date part
    movies_df['release_date'] = pd.to_datetime(movies_df['release_date']).dt.normalize()
    trendy_films = movies_df[movies_df['release_date'] == today]

    if trendy_films.empty:
        latest_film = movies_df[movies_df['release_date'] < today].sort_values(by='release_date', ascending=False).head(1)
        return latest_film    
    return trendy_films

# Function to format the date in Trendy Section
def format_date(date_str):
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return date_str  # Return the original string if it doesn't match expected formats
        return date_obj.strftime('%d-%m-%Y')
    return ''

# Function to get trendy films for the week
def get_trendy_films_week():
    today = pd.to_datetime('today').normalize()
    start_of_last_week = today - pd.Timedelta(days=today.weekday() + 7)
    end_of_last_week = start_of_last_week + pd.Timedelta(days=6)
    
    # Filter films released in the past week
    trendy_films = movies_df[(movies_df['release_date'] >= start_of_last_week) & (movies_df['release_date'] <= end_of_last_week)]
    
    # Sort by vote_count and select top 10 Popular Films (vote_count)
    top_trendy_films = trendy_films.sort_values(by='vote_count', ascending=False).head(10)
    
    return top_trendy_films

# Function to get trendy films for the month (make sure are the ones before today)
def get_trendy_films_month():
    today = pd.to_datetime('today').normalize()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + pd.DateOffset(months=1)) - pd.Timedelta(days=1)
    trendy_films = movies_df[(movies_df['release_date'] >= start_of_month) & (movies_df['release_date'] <= end_of_month)]
    return trendy_films

# Get today's date for the trendy Section
today_date = datetime.now().strftime('%A %d-%m-%Y')

# Function to display films in rows for Trendy Section(movie_card_small css))
def display_films_in_rows(films, card_class="movie-card-small"):
    films = films.head(10)  # Select top 10 films
    cols = st.columns(5)
    for i, film in enumerate(films.itertuples()):
        with cols[i % 5]:
            st.markdown(f"""
            <div class="{card_class}">
                <img src="{film.poster_image}" alt="{film.title}">
                <div class="movie-info">
                    <h4>{film.title}</h4>
                    <p>{format_providers(film.providers)}</p>
                    <p class="rating">{format_rating(film.vote_average)}</p>
                    <details>
                        <summary>More info</summary>
                        <p><strong>Overview:</strong> {film.overview}</p>
                        <p><strong>Genres:</strong> {format_genres(film.genres)}</p>
                    </details>
                </div>
            </div>
            """, unsafe_allow_html=True)

#------------Streaming Filter Page Functions---------------------------------

# Function to display films in styled HTML For Filter Section
def display_films(films, card_class="movie-card"):
    for i in range(len(films)):
        film = films.iloc[i]
        st.markdown(f"""
        <div class="{card_class}">
            <img src="{film['poster_image']}" alt="{film['title']}">
            <div class="movie-info">
                <h4>{film['title']}</h4>
                <p>{format_providers(film['providers'])}</p>
                <p class="rating">{format_rating(film['vote_average'])}</p>
                <details>
                    <summary>More info</summary>
                    <p><strong>Overview:</strong> {film['overview']}</p>
                    <p><strong>Genres:</strong> {format_genres(film['genres'])}</p>
                </details>
            </div>
        </div>
        """, unsafe_allow_html=True)
# Current Year for the Section Best films per Year
current_year = datetime.now().year

#------------Functions used in common-----------------------------------

# Function to format the release date in Fun Fact Section
def format_release_date(date_string):
    return date_string[:10] if date_string else "N/A"

# Function to format rating
def format_rating(rating):
    return f"{rating:.1f} stars" if rating else "N/A"

# Function to format genres
def format_genres(genres):
    if isinstance(genres, list):
        return ", ".join(genres)
    return genres

# Function to format providers
def format_providers(providers):
    if not providers:
        return "Now Showing"
    if isinstance(providers, list):
        return ", ".join(providers)
    return providers

#---------SIDEBAR SETTINGS-----------------------------------------------------------------

# Sidebar Colour
st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #cacef4;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Logo
logo_path = "logo_moviedash.png"
# Load the logo image
logo_image = st.sidebar.image(logo_path, width=300)  # Adjust width and height as needed

# Sidebar Menu Initialisation
st.sidebar.markdown('<h2>Grab your popcorn and explore our latest hot picks, streaming options, and movie trivia!</h2>', unsafe_allow_html=True)
if 'menu' not in st.session_state:
    st.session_state.menu = 'Trendy Films'

# Sidebar menu options with icons
menu_options = {
    "Trendy Films": "🍿 Trendy Picks",
    "Streaming Options": " 📺 Stream & Chill",
    "Interesting facts": "🌟 Movies Fun Facts"
}

# Update menu based on selection
menu = st.sidebar.radio("", list(menu_options.values()))
st.session_state.menu = [key for key, value in menu_options.items() if value == menu][0]

# Sidebar footer
st.sidebar.markdown('''
---
Created with ❤️ by [Marta Matias](https://digitalfutures.com).

Data provided by Justwatch and TMDB
''')

#----------------------1) TRENDY SECTION PAGE ------------------------------------------

# Welcome message
if st.session_state.menu == "Trendy Films": # Display the selected menu content
    st.markdown("""
    <style>
        .hero-section h2 {
            color: white;
        }
        .hero-section .highlight {
            color: #FF3131;
        }
    </style>
    <div class="hero-section">
        <h1>Welcome to <span class="highlight">Movie</span>Dash</h1>
        <h2>Your ultimate source for the latest and greatest films!</h2> 
        <p>Get your popcorn and dive into today's top picks, discover fascinating movie facts,<br> and easily find your favourite films with our advanced filters.</p>
    </div>
    """, unsafe_allow_html=True)

# Today's Hot Pick Section- Films streamed today

    st.header("Today's Popping Hot Picks 🍿")
    st.markdown(f"Discover the top movies released Today (<strong>{today_date}</strong>), freshly popped just for you!", unsafe_allow_html=True)
    st.markdown('<div class="movies-container">', unsafe_allow_html=True)

    trendy_films_today = get_trendy_films_today()
    if trendy_films_today.empty:
        st.write("No trendy films for today.")
    else:
        trendy_films_today = trendy_films_today.sort_values(by=['vote_count'], ascending=[False])
        display_films_in_rows(trendy_films_today)

    st.markdown('</div>', unsafe_allow_html=True)
    
    
# Weekly or Monthly Hotpicks Section - Selection

    st.markdown("""
    <div style="background-color: #cacef4; padding: 20px; border-radius: 10px;">
        <h2>Pick Your Popcorn Flicks 🎥</h2>
        <p>Select between this week's and this month's must-watch movies!</p>
        <div class="movies-container">
    """, unsafe_allow_html=True)
    
    # Selection box for week or month
    selection = st.selectbox("", ["This Week", "This Month"])
    
    # Close the div
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch and display the weekly/monthly trendy films data based on user selection (week or month)
    if selection == "This Week":
        st.markdown("<h2>This Week's Must-Watch Popcorn Flicks 🍿</h2>", unsafe_allow_html=True)
        trendy_films = get_trendy_films_week()
    else:
        st.markdown("<h2>This Month's Must-Watch Popcorn Flicks 🍿</h2>", unsafe_allow_html=True)
        trendy_films = get_trendy_films_month()
    
    if trendy_films.empty:
        st.write(f"No trendy films for {selection.lower()}.")
    else:
        # Sort films by vote count in descending order and select top 10
        trendy_films = trendy_films.sort_values(by=['vote_count'], ascending=[False])
        display_films_in_rows(trendy_films)
    
# Fun Fact Section (Bottom)-----------------------------------------------------

    st.markdown("""
    <div style="background-color: #cacef4; padding: 20px; border-radius: 10px;">
        <h2>Popcorn Fun Fact 💡</h2>
        <p>Explore genres distribution in this week's and this month's must-watch movies.</p>
        <div class="movies-container">
    """, unsafe_allow_html=True)
    
    # Close the div
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch the data for the genre distribution
    trendy_films_week = get_trendy_films_week()
    trendy_films_month = get_trendy_films_month()

    #Display results
    if trendy_films_week is not None and not trendy_films_week.empty and trendy_films_month is not None and not trendy_films_month.empty:
        col1, col2 = st.columns(2)
    
        with col1:
            st.markdown("""
            <div style="background-color: #FFF478; padding: 20px; border-radius: 10px;">
            <h2>Popping This Week</h2>
            """, unsafe_allow_html=True)
            
            # Create a list of all genres from the films
            genres_list_week = []
            for genres in trendy_films_week['genres']:
                if isinstance(genres, list):
                    genres_list_week.extend(genres)
                elif isinstance(genres, str):
                    genres_list_week.extend(genres.split(', '))
            
            # Create a DataFrame for genres
            genres_df_week = pd.DataFrame(genres_list_week, columns=['genre'])
            genre_counts_week = genres_df_week['genre'].value_counts().reset_index()
            genre_counts_week.columns = ['genre', 'count']
            
            # Create a pie chart with percentage and genre type
            fig_week = px.pie(genre_counts_week, names='genre', values='count', title='Genre Distribution This Week',
                         labels={'count': 'Count', 'genre': 'Genre'},
                         hole=0.3)
            fig_week.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_week)
            st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
        
        #Fetch and display the data for the month
        with col2:
            st.markdown("""            
            <div style="background-color: #FFF478; padding: 20px; border-radius: 10px;">
            <h2>Sizzling This Month</h2>
            """, unsafe_allow_html=True)
            
            # Create a list of all genres from the films
            genres_list_month = []
            for genres in trendy_films_month['genres']:
                if isinstance(genres, list):
                    genres_list_month.extend(genres)
                elif isinstance(genres, str):
                    genres_list_month.extend(genres.split(', '))

            # Create a DataFrame for genres
            genres_df_month = pd.DataFrame(genres_list_month, columns=['genre'])
            genre_counts_month = genres_df_month['genre'].value_counts().reset_index()
            genre_counts_month.columns = ['genre', 'count']
            
            # Create a pie chart with percentage and genre type
            fig_month = px.pie(genre_counts_month, names='genre', values='count', title='Genre Distribution This Month',
                         labels={'count': 'Count', 'genre': 'Genre'},
                         hole=0.3)
            fig_month.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_month)
            st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.write("No trendy films data available for this week or this month.")

#------------------- 2) STREAMING FILTER PAGE --------------------------------------

# Ensure genres column has no NaN values
movies_df['genres'] = movies_df['genres'].apply(lambda x: x if isinstance(x, list) else [])

# "Streaming Options" Sidebar Section
if st.session_state.menu == "Streaming Options":
    st.title("Find Your Perfect Film 🎬")
    st.write("Filter by Provider, Genre, Year, and Popularity to discover the best movies for you!")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Search filter
        search_query = st.text_input("🔍 Search for a film", value="")
    
        # Filter options
        selected_providers = st.multiselect(
            "📺 Select Provider",
            options=['Amazon Prime Video', 'Netflix', 'Disney Plus', 'Apple TV', 'Now TV Cinema', 'Paramount Plus', 'Sky Go'],
            default=['Netflix', 'Amazon Prime Video', 'Disney Plus', 'Apple TV', 'Now TV Cinema', 'Paramount Plus', 'Sky Go']
        )
    
        # Filter options without NaN or empty lists
        genre_options = movies_df['genres'].explode().dropna().unique().tolist()
        selected_genres = st.multiselect(
            "🎭 Select Genres",
            options=genre_options,
            default=genre_options
        )
    
        # Year filter slider
        year_filter = st.slider(
            "📅 Filter by Release Year",
            min_value=2010,
            max_value=current_year,
            step=1,
            value=(2010, current_year)
        )
    
        popularity_range = st.slider(
            "📈 Select Popularity Range",
            min_value=int(movies_df['vote_average'].min()),
            max_value=int(movies_df['vote_average'].max()),
            value=(int(movies_df['vote_average'].min()), int(movies_df['vote_average'].max())),
            format="%d",
            help="Slide to choose between less popular to extremely popular movies based on vote count."
        )
    # Filter results
    with col2:
        # Filter the dataframe based on the search query
        if search_query:
            filtered_movies_df = movies_df[movies_df['title'].str.contains(search_query, case=False, na=False)]
        else:
            filtered_movies_df = movies_df.copy()
    
        # Further filter the dataframe based on other user selections
        filtered_movies_df = filtered_movies_df[
            filtered_movies_df['providers'].apply(lambda x: any(provider in x for provider in selected_providers)) &
            filtered_movies_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres)) &
            filtered_movies_df['year'].between(year_filter[0], year_filter[1]) &
            filtered_movies_df['vote_average'].between(popularity_range[0], popularity_range[1])
        ]
    
        # Display the filtered films in a grid layout
        if filtered_movies_df.empty:
            st.write("No films match the selected criteria.")
        else:
            cols = st.columns(4)
            for i, film in filtered_movies_df.iterrows():
                # Find the matching provider for the selected provider
                matching_provider = next((provider for provider in film['providers'] if provider in selected_providers), None)
                
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{film['poster_image']}" alt="{film['title']}">
                        <div class="movie-info">
                            <h4>{film['title']}</h4>
                            <p><b>Provider:</b> {matching_provider}</p>
                            <p><b>Release Date:</b> {film['release_date'].strftime('%d/%m/%Y')}</p>
                                <p class="rating">{format_rating(film.vote_average)}</p>
                            <details>
                                <summary>More info</summary>
                                <p>{film['overview']}</p>
                            </details>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Fun Fact in the Streaming Filter Page (Bottom Section)------------------------------------ 

    # Headline for Fun Fact Filter Section
    st.markdown("""
    <div style="background-color: #cacef4; padding: 20px; border-radius: 10px;">
        <h2>Popcorn Fun Fact </h2>
        <p>Explore interesting bites from our Providers.</p>
        <div class="movies-container">
    """, unsafe_allow_html=True)    
    # Close the div
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create some graphs about providers - Fun Fact Filter Section
    col1, col2 = st.columns(2)

    with col1:
        # Provider Market Share
        st.markdown("""
            <div style="background-color: #FFF478; padding: 20px; border-radius: 10px;">
            <h2>Provider Market Share</h2>
            <p>Explore the percentage of films available on each provider.</p>
            """, unsafe_allow_html=True)  
        
        # Filter only the specified providers
        selected_providers = [
            'Amazon Prime Video', 'Netflix', 'Disney Plus', 'Now TV Cinema', 'Paramount Plus', 'Sky Go'
        ]
        filtered_movies_df = movies_df[movies_df['providers'].apply(lambda x: any(provider in selected_providers for provider in x))]

        # Group by provider and count number of films
        provider_counts = filtered_movies_df.explode('providers')['providers'].value_counts().reset_index()
        provider_counts.columns = ['provider', 'count']
        provider_counts = provider_counts[provider_counts['provider'].isin(selected_providers)]

        # Create the 3D donut chart
        fig_donut = go.Figure(data=[go.Pie(
            labels=provider_counts['provider'],
            values=provider_counts['count'],
            hole=.3,
            hoverinfo="label+percent",
            textinfo='label+percent',
            textposition='inside'
        )])

        # Update layout to hide the legend
        fig_donut.update_layout(
            title_text="",
            showlegend=False
        )

        # Display the chart
        st.plotly_chart(fig_donut)

    with col2:
        # Most Popular Films by Provider
        st.markdown("""
        <div style="background-color: #FFF478; padding: 20px; border-radius: 10px;">
        <h2>Most Popular Films by Provider</h2>
        <p>Explore which provider has the most popular films based on vote count.</p>
        """, unsafe_allow_html=True)  

        # Explode 'providers' column to create separate rows for each provider
        exploded_movies_df = filtered_movies_df.explode('providers')

        # Find the most popular films by provider based on vote count
        popular_movies_df = exploded_movies_df.loc[exploded_movies_df.groupby('providers')['vote_count'].idxmax()]
        provider_popularity_counts = popular_movies_df['providers'].value_counts().reset_index()
        provider_popularity_counts.columns = ['provider', 'count']

        # Create the bar chart
        fig_bar_popularity = px.bar(
            provider_popularity_counts,
            x='provider',
            y='count',
            title='',
            labels={'provider': 'Provider', 'count': 'Number of Most Popular Films'}
        )

        # Display the chart
        st.plotly_chart(fig_bar_popularity)


# -------------3) INTERESTING FACTS PAGE------------------------------------------------------

# Headlines of the page
elif st.session_state.menu == "Interesting facts":
    st.title("Film Release Trends Over Time")
    st.header("Track the popping number of films released each year from 2010 to the present.")

    # Load the data
    movies_df = load_data()
    
# GRAPHIC 1: Number of films released each year from 2010 to the present------------------------
    
    # Filter data from 2010 onwards
    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])
    movies_df = movies_df[movies_df['release_date'].dt.year >= 2010]

    # Extract year from release_date
    movies_df['year'] = movies_df['release_date'].dt.year

    # Ensure 'providers' is in list format
    movies_df['providers'] = movies_df['providers'].apply(lambda x: x.split(',') if isinstance(x, str) else x)

    # Explode providers to separate rows
    movies_df = movies_df.explode('providers')

    # Displaying the UI components
    st.subheader("Number of Films Released Each Year by Provider")

    # Multiselect widget for selecting providers
    selected_providers = st.multiselect(
        "Select Providers",
        ['Amazon Prime Video', 'Netflix', 'Disney Plus', 'Now TV Cinema', 'Paramount Plus', 'Sky Go'],
        default=['Amazon Prime Video', 'Netflix', 'Disney Plus']
    )

    # Filter the data based on selected providers
    films_per_year_provider = movies_df.groupby(['year', 'providers']).size().reset_index(name='count')
    films_per_year_provider = films_per_year_provider[films_per_year_provider['providers'].isin(selected_providers)]

    # Create the line chart
    fig = px.line(films_per_year_provider, x='year', y='count', color='providers', 
                title='See how many films each streaming service pops out annually.',
                labels={'year': 'Year', 'count': 'Number of Films', 'providers': 'Provider'})

    # Display the chart
    st.plotly_chart(fig)
    
# GRAPHIC 2: Genre Popularity per Year---------------------------------------------------------------------------  

    st.subheader("Genre Popularity per Year: Discover the popularity of different genres of films over the years.")
    
    # Ensure 'genres' is in list format
    movies_df['genres'] = movies_df['genres'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
    
    # Explode genres to separate rows
    movies_df = movies_df.explode('genres')
    
    # Multiselect for genres
    selected_genres = st.multiselect("Select Genres", options=movies_df['genres'].unique(), default=movies_df['genres'].unique())
    
    # Multiselect for years
    selected_years = st.multiselect("Select Years", options=movies_df['year'].unique(), default=movies_df['year'].unique())
    
    # Filter data based on selections
    filtered_movies = movies_df[(movies_df['genres'].isin(selected_genres)) & (movies_df['year'].isin(selected_years))]
    
    # Group by year and genre and count number of films
    films_per_genre_year = filtered_movies.groupby(['year', 'genres']).size().reset_index(name='count')
    
    # Create the bar chart
    fig_bar = px.bar(films_per_genre_year, x='year', y='count', color='genres', title='Number of Films in Each Genre per Year',
                     labels={'year': 'Year', 'count': 'Number of Films', 'genres': 'Genre'}, barmode='group')
    
    # Display the chart
    st.plotly_chart(fig_bar)

    
# GRAPHIC 3: Popular Film per Year (showed in cards format)-------------------------------------------------------------
  
    # Most Popular Film of Each Year
    st.subheader("Most Popular Film of Each Year")
    st.write("Find out which film popped to the top each year based on vote count.")

    # Group by year and find the film with the highest vote count
    most_popular_each_year = movies_df.loc[movies_df.groupby('year')['vote_count'].idxmax()]

    # Display the most popular film of each year in rows with 5 columns each
    cols = st.columns(8)
    for i, year in enumerate(most_popular_each_year['year'].unique()):
        film = most_popular_each_year[most_popular_each_year['year'] == year].iloc[0]
        with cols[i % 8]:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{film['poster_image']}" alt="{film['title']}">
                <div class="movie-info">
                    <h4>{year}</h4>
                    <p><b>Title:</b> {film['title']}</p>
                    <details>
                        <summary>More info</summary>
                        <p>{film['overview']}</p>
                    </details>
                </div>
            </div>
            """, unsafe_allow_html=True)
    

