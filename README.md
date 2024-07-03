# 🎬 MovieDash

MovieDash is a Streamlit web application designed to help you discover the latest and greatest movies. With daily updates on new releases, weekly trending films, and monthly highlights, MovieDash ensures you never miss out on must-watch movies. The app also offers detailed information on each film, including genres, ratings, and available streaming providers.

# App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://moviedash.streamlit.app)

## 🌟 Features

- **🔥 Daily Hot Picks**: Discover the top movies released today.
- **📈 Weekly Trendy Films**: Explore the most popular films of the past week.
- **📅 Monthly Highlights**: View a comprehensive list of films released in the current month.
- **🔍 Streaming Options**: Filter movies by provider, genre, year, and popularity.
- **💡 Interesting Facts**: Visualize genre distribution and trends over time with interactive charts.
- **🎨 Custom Styling**: Clean and attractive design with custom CSS.

## 🛠️ Technologies Used

- **Streamlit**: For creating the interactive web interface.
- **Pandas**: For data manipulation and analysis.
- **PostgreSQL**: As the database to store and retrieve movie data.
- **Plotly**: For creating interactive charts and visualizations.



## 📖 References to Build the App

### Articles
- **[Creating a movie finder app with Streamlit and OMDb API](https://medium.com/@davidjohnakim/creating-a-movie-finder-app-with-streamlit-and-omdb-api-a859bcf4db21)**
  - David Akim
  
- **[Make dynamic filters in Streamlit and show their effects on the original dataset](https://blog.streamlit.io/make-dynamic-filters-in-streamlit-and-show-their-effects-on-the-original-dataset/)**
  - Vladimir Timofeenko
  
- **[🎬 TMDB 🤝 Streamlit 🔥: Build Your Own Movie Recommendation System 🚀](https://python.plainenglish.io/tmdb-streamlit-build-your-own-movie-recommendation-system-f2ffbca63d11)**
  - Afaque Umer

### Videos
- **[Building a Simple Movies Directory app with Streamlit (using side by side layout & Pandas)](https://www.youtube.com/watch?v=xCDAkQdClg0)**
  - JCharisTech

- **[Movie Recommendation System: Python, Streamlit, TMDB | Machine Learning | ‪@yashhhtalks‬ | 2023 Bharat Intern](https://www.youtube.com/watch?v=or_8C2MXRU0)**
  - Bharat Intern

- **[Building a Dashboard web app in Python - Full Streamlit Tutorial - Data Professor](https://www.youtube.com/watch?v=o6wQ8zAkLxc)**
  - Data Professor

### Documentation & Forums
- **[Streamlit Documentation](https://docs.streamlit.io/)**

- **[TMDB Developer](https://developer.themoviedb.org/reference/intro/getting-started)**

- **[TMDB Forum](https://www.themoviedb.org/talk/)**

- **[Stackoverflow for questions of TMDB API and Python](https://stackoverflow.com/)**

### Special Tools
- **[Moviedash MyChatGPT](https://chatgpt.com/g/g-G9JDUQb1p-moviedash-python-and-streamlit-expert)**
  - Special Prompt to help you to build your movie app resolving all your doubts


## 🚀 Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/MovieDash.git
   cd MovieDash
    Install the required dependencies:

   ```sh
   Copy code
   pip install -r requirements.txt
   Set up your PostgreSQL database and add the connection details to Streamlit secrets:

   ```sh
   Copy code
   streamlit secrets set DB_USERNAME your_db_username
   streamlit secrets set DB_PASSWORD your_db_password
   streamlit secrets set DB_HOST your_db_host
   streamlit secrets set DB_PORT your_db_port
   streamlit secrets set DB_NAME your_db_name
   Run the Streamlit app:

   ```sh
   Copy code
   streamlit run app.py

## 📖 Usage

Open your web browser and navigate to the local URL provided by Streamlit to start exploring MovieDash.
Use the sidebar to navigate between different sections: Daily Hot Picks, Weekly Trendy Films, Monthly Highlights, Streaming Options, and Interesting Facts.
Click on any movie entry to view more details, including the overview, genres, and available streaming providers.

## 🤝 Contributing

Contributions are welcome! If you have any improvements or new features to add, please fork the repository, create a new branch, and submit a pull request. Make sure to follow the coding standards and include appropriate tests for any new functionality.

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgements
Data provided by Justwatch and TMDB.
Created with ❤️ by Marta Matias.
