import streamlit as st
import mysql.connector

# Must be the first Streamlit command
st.set_page_config(page_title="Filmoria")

#css styling for the app
st.markdown("""
    <style>
    /* Main app styling */
    .main {
        background-color: #141414;  /* Netflix black */
        color: white;
        max-width: 2500px;  /* Compact width */
        margin: 15px;    /* Center the content */
        padding: 20px;
    }
    /* Custom Filmoria header */
    .filmoria-header {
        font-family: 'Bebas Neue', sans-serif;  /* Stylish, cinematic font */
        color: #B20710;  /* Deep red */
        font-size: 48px;  /* Large size */
        text-align: center;
        margin-bottom: 20px;
        text-transform: uppercase;  /* All caps for impact */
        letter-spacing: 2px;  /* Slight spacing for elegance */
    }
    /* Headers */
    h2 {
        color: #E50914;  /* Netflix red for subheaders */
    }
    /* Buttons */
    .stButton>button {
        background-color: #E50914;
        color: white;
        border: none;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #f40612;  /* Slightly lighter red */
    }
    /* Text inputs */
    .stTextInput>div>input {
        background-color: #333;
        color: white;
        border: 1px solid #E50914;
    }
    /* Multiselect and selectbox */
    .stMultiSelect>div, .stSelectbox>div {
        background-color: #333;
        color: white;
    }
    /* Movie card styling  */
    .movie-card {
        transition: all 0.3s ease;
        margin-bottom: 100px;
        padding: 30px;
        margin: 10px;
        display: inline-block;
    }
    
   
    .movie-card img {
        border-radius: 30px;
    }
    /* General text */
    .stMarkdown, .stText {
        color: white;
    }
    /* Add spacing between columns */
    .stColumn > div {
        margin: 10px;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Connect to MySQL Database
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="movie_recommendation"
        )
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Create users table if not exists
def create_users_table():
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                genre_preference VARCHAR(255),
                actor_preference VARCHAR(255)
            )
        ''')
        conn.commit()
        conn.close()

# Function to register a new user
def register_user(username, password):
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            return True
        except mysql.connector.IntegrityError:
            conn.close()
            return False
    return False

# Function to authenticate user
def authenticate_user(username, password):
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = c.fetchone()
        conn.close()
        return user
    return None

# Function to store user preferences
def save_preferences(username, genres, actors):
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        c.execute("UPDATE users SET genre_preference=%s, actor_preference=%s WHERE username=%s",
                  (", ".join(genres), ", ".join(actors), username))
        conn.commit()
        conn.close()
        return True
    return False

# Function to fetch user preferences
def get_user_preferences(username):
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        c.execute("SELECT genre_preference, actor_preference FROM users WHERE username=%s", (username,))
        result = c.fetchone()
        conn.close()
        return result[0].split(", ") if result[0] else [], result[1].split(", ") if result[1] else []
    return [], []

# Function to fetch recommended movies
def get_recommendations(preferred_genres, preferred_actors):
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        query = "SELECT movie_name, genre, imdb_rating, description, actors, poster FROM movies WHERE 1=1"
        conditions = []
        values = []

        if preferred_genres and "All" not in preferred_genres:
            conditions.append("genre IN (" + ", ".join(["%s"] * len(preferred_genres)) + ")")
            values.extend(preferred_genres)
        if preferred_actors and "All" not in preferred_actors:
            conditions.append("(" + " OR ".join(["actors LIKE %s"] * len(preferred_actors)) + ")")
            values.extend([f"%{actor}%" for actor in preferred_actors])

        if conditions:
            query += " AND " + " AND ".join(conditions)
        query += " ORDER BY imdb_rating DESC LIMIT 5"

        c.execute(query, values)
        movies = c.fetchall()
        conn.close()
        return movies if movies else []
    return []

# Function to search movies
def search_movies(query):
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        c.execute("SELECT movie_name, genre, imdb_rating, description, actors, poster FROM movies WHERE movie_name LIKE %s",
                  (f"%{query}%",))
        movies = c.fetchall()
        conn.close()
        return movies if movies else []
    return []

# ------------------ UI ------------------

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

# Create tables
create_users_table()

# ------------------ LOGIN / REGISTER ------------------

if not st.session_state.authenticated:
    st.markdown('<div class="filmoria-header">Filmoria</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials! Try again.")

    with tab2:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Account created! Please log in.")
            else:
                st.error("Username already exists or registration failed.")

    st.stop()

# ------------------ MAIN INTERFACE ------------------

st.markdown('<div class="filmoria-header">Filmoria</div>', unsafe_allow_html=True)
st.write(f"Welcome, {st.session_state.username}!", style={"color": "white"})
st.subheader("Tell us your movie preferences 📽️")

genre_options = ["All", "Action", "Drama", "Romance", "Thriller", "Crime"]
actor_options = ["All", "Adrien Brody", "Amy Adams", "Ana de Armas", "Angela Bassett", "Anya Taylor-Joy", "Aunjanue Ellis", 
"Awkwafina", "Brad Pitt", "Brendan Fraser", "Carrie-Anne Moss", "Cate Blanchett", "Chris Evans", 
"Chris Hemsworth", "Christian Bale", "Cillian Murphy", "Daniel Craig", "Denzel Washington", 
"Donnie Yen", "Edward Norton", "Elisabeth Moss", "Emily Blunt", "Emma Stone", "Emilia Clarke", 
"Emilia Jones", "Florence Pugh", "Frances McDormand", "Gabriel Basso", "Gabriel LaBelle", 
"Gal Gadot", "Gael García Bernal", "Gary Oldman", "Glen Powell", "Golshifteh Farahani", 
"Greta Lee", "Harry Melling", "Harry Styles", "Hayley Atwell", "Issa Rae", "Jason Momoa", 
"Jennifer Lopez", "Jim Caviezel", "Joey King", "John David Washington", "Johnny Flynn", 
"Joaquin Phoenix", "Keanu Reeves", "Keke Palmer", "LaKeith Stanfield", "Lana Condor", 
"Letitia Wright", "Luciane Buchanan", "Madeleine Yuna Voyles", "Marion Cotillard", 
"Marlon Brando", "Matthew McConaughey", "Michelle Williams", "Miles Teller", 
"Mira Sorvino", "Morgan Freeman", "Natalie Portman", "Nicholas Galitzine", "Nina Hoss", 
"Noah Centineo", "Olivia Colman", "Owen Wilson", "Priyanka Chopra", "Rami Malek", 
"Robert Downey Jr.", "Robert Pattinson", "Ryan Gosling", "Ryan Reynolds", "Sadie Sink", 
"Sam Claflin", "Sam Heughan", "Scarlett Johansson", "Simu Liu", "Sofia Carson", 
"Sydney Sweeney", "Teo Yoo", "Timothée Chalamet", "Tom Cruise", "Tom Hanks", 
"Tom Hardy", "Tom Holland", "Tommy Lee Jones", "Troy Kotsur", "Vicky Krieps", 
"Vin Diesel", "Walker Scobell", "Will Smith", "Zendaya", "Zoë Kravitz"]


current_genres, current_actors = get_user_preferences(st.session_state.username)
selected_genres = st.multiselect("Pick your favorite genres:", genre_options, default=current_genres)
selected_actors = st.multiselect("Pick your favorite actors:", actor_options, default=current_actors)

if st.button("Save Preferences"):
    if save_preferences(st.session_state.username, selected_genres, selected_actors):
        st.success("Preferences saved!")
    else:
        st.error("Failed to save preferences")

# ------------------ RECOMMENDATIONS ------------------

st.subheader("✨ Recommended for You")
recommended_movies = get_recommendations(selected_genres, selected_actors)
if recommended_movies:
    cols = st.columns(min(3, len(recommended_movies)))
    for i, movie in enumerate(recommended_movies):
        with cols[i % 3]:
            st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
            st.image(movie[5], width=150, caption=movie[0])
            st.write(f"⭐ {movie[2]}")
            st.write(f"🎭 {movie[1]}")
            st.write(f"🎬 {movie[4]}")
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Select preferences to see recommendations!")

# ------------------ SEARCH & CUSTOM RECOMMENDATION ------------------

st.subheader("🔍 Search for a Movie")
search_query = st.text_input("Enter movie name:")
if st.button("Search"):
    results = search_movies(search_query)
    if results:
        for movie in results:
            st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
            st.image(movie[5], width=150, caption=movie[0])
            st.write(f"⭐ {movie[2]}")
            st.write(f"🎭 {movie[1]}")
            st.write(f"🎬 {movie[4]}")
            st.write(f"📖 {movie[3]}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No results found!")

st.subheader("🎲 Personalized Movie Recommendation")
selected_genre = st.selectbox("Choose a Genre", ["Any"] + genre_options[1:])
selected_actor = st.selectbox("Choose an Actor", ["Any"] + actor_options[1:])
if st.button("Recommend Something!"):
    genres = [selected_genre] if selected_genre != "Any" else []
    actors = [selected_actor] if selected_actor != "Any" else []
    filtered_movies = get_recommendations(genres, actors)
    if filtered_movies:
        movie = filtered_movies[0]
        st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
        st.image(movie[5], width=150, caption=movie[0])
        st.write(f"⭐ {movie[2]}")
        st.write(f"🎭 {movie[1]}")
        st.write(f"🎬 {movie[4]}")
        st.write(f"📖 {movie[3]}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No recommendations found!")