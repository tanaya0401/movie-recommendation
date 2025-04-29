Filmoria - Movie Recommendation App

Overview

Filmoria is a web-based movie recommendation application built using Streamlit and MySQL. It allows users to register, log in, set their movie preferences (genres and actors), and receive personalized movie recommendations. The app also features a search functionality to find movies and a custom recommendation tool based on user-selected genres and actors.
The application is styled with a Netflix-inspired dark theme, featuring a sleek, cinematic design with custom fonts and vibrant red accents.

Features:
User Authentication: Register and log in with a username and password.
Preference Management: Select favorite genres and actors to personalize recommendations.
Movie Recommendations: Get tailored movie suggestions based on user preferences.
Search Functionality: Search for movies by name and view details like genre, IMDb rating, actors, and description.
Custom Recommendations: Generate a single movie recommendation based on a chosen genre and actor.
Responsive UI: Styled with a Netflix-like aesthetic, including custom fonts, colors, and movie card layouts.

Tech Stack:
Frontend: Streamlit (Python-based web framework)
Backend: MySQL (for storing user data and movie information)
Styling: Custom CSS with Google Fonts (Bebas Neue)
Database: MySQL Connector for Python
Deployment: Designed for local deployment (can be extended to cloud platforms)

Prerequisites:
To run Filmoria locally, ensure you have the following installed:
Python 3.8+
MySQL Server
pip (Python package manager)

Installation:
Clone the Repository:
git clone https://github.com/your-username/filmoria.git
cd filmoria
Install Dependencies: Create a virtual environment and install the required Python packages:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install streamlit mysql-connector-python

Set Up MySQL Database:
Install and start MySQL Server.
Create a database named movie_recommendation:
CREATE DATABASE movie_recommendation;
Update the database connection details in the get_db_connection() function if needed (default: host=localhost, user=root, password=root).
The app automatically creates a users table. You need to create and populate a movies table with the following schema:

CREATE TABLE movies (
    movie_name VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    imdb_rating FLOAT,
    description TEXT,
    actors TEXT,
    poster VARCHAR(255)
);

Insert movie data manually or via a script. The poster column should contain URLs to movie poster images.
Run the Application: Start the Streamlit app:
streamlit run app.py
Open your browser and navigate to http://localhost:8501.

Usage:
Register/Login:
Create an account or log in using the tabs on the landing page.
Set Preferences:
Choose your favorite genres and actors from the provided lists.
Save preferences to tailor recommendations.
View Recommendations:
See a list of recommended movies based on your preferences, displayed in a grid of movie cards.
Search Movies:
Enter a movie name to search and view matching results with details.
Custom Recommendation:
Select a genre and actor to get a single, personalized movie recommendation.

File Structure

filmoria/
├── app.py           # Main Streamlit application code
├── README.md        # This file
└── venv/            # Virtual environment (not tracked in git)

Notes:
The app is designed for local use. For production, consider deploying on a cloud platform like Heroku, AWS, or Render, and secure the database connection.
Ensure movie poster URLs in the movies table are valid to avoid broken images.
The app does not hash passwords for simplicity. In a production environment, use a library like bcrypt to securely hash passwords.
The movies table must be populated with data for recommendations and search to work effectively.
