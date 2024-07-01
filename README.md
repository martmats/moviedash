# 🎬 MovieDash

MovieDash is a Streamlit web application designed to help you discover the latest and greatest movies. With daily updates on new releases, weekly trending films, and monthly highlights, MovieDash ensures you never miss out on must-watch movies. The app also offers detailed information on each film, including genres, ratings, and available streaming providers.

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

## 🚀 Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/MovieDash.git
   cd MovieDash
    Install the required dependencies:

sh
Copy code
pip install -r requirements.txt
Set up your PostgreSQL database and add the connection details to Streamlit secrets:

sh
Copy code
streamlit secrets set DB_USERNAME your_db_username
streamlit secrets set DB_PASSWORD your_db_password
streamlit secrets set DB_HOST your_db_host
streamlit secrets set DB_PORT your_db_port
streamlit secrets set DB_NAME your_db_name
Run the Streamlit app:

sh
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
