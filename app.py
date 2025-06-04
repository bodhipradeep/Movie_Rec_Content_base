import streamlit as st
import pickle
import pandas as pd
import requests
from urllib.parse import urlparse
import time

# Set page layout
st.set_page_config(layout="wide")

# Load saved objects with better caching
@st.cache_data(show_spinner="Loading recommendation data...")
def load_data():
    with open("knn_model.pkl", "rb") as f:
        knn_model = pickle.load(f)

    with open("tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)

    movies = pd.read_csv("movies_processed.csv")
    return knn_model, tfidf_matrix, movies

knn_model, tfidf_matrix, movies = load_data()

# Fetch poster with retry logic and better caching
@st.cache_data(ttl=24*60*60, show_spinner=False)  # Cache for 24 hours
def fetch_poster(movie_id):
    if not movie_id or not str(movie_id).isdigit():
        return None
    
    for attempt in range(3):
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=tmdb_api_key&language=en-US"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
                return None
            elif response.status_code == 429:  # Too many requests
                time.sleep(2)  # Wait before retrying
                continue
            else:
                return None
        except Exception as e:
            print(f"Error fetching poster (attempt {attempt+1}): {e}")
            time.sleep(1)
    
    return None

def extract_tmdb_id(url):
    if pd.isna(url) or not isinstance(url, str):
        return None
    try:
        # Handle different URL formats
        parts = [p for p in url.strip().split("/") if p]
        if "themoviedb.org" in url:
            return parts[-1]
        return parts[-1] if parts else None
    except:
        return None

# Movie recommendation function with progress
def recommend_movies(movie_title, top=15):
    try:
        idx = movies[movies['title'] == movie_title].index[0]
        distances, indices = knn_model.kneighbors(tfidf_matrix[idx], n_neighbors=top+1)
        
        recommended = []
        progress_bar = st.progress(0)
        
        for i, index in enumerate(indices.flatten()[1:]):
            title = movies.iloc[index]['title']
            url = movies.iloc[index]['tmdb_url']
            tmdb_id = extract_tmdb_id(url)
            poster = fetch_poster(tmdb_id)
            recommended.append((title, url, poster))
            progress_bar.progress((i + 1) / top)
            
        progress_bar.empty()
        return recommended
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return []

# Sidebar interface
st.sidebar.header("🎬 Search Movie")
selected_title = st.sidebar.selectbox(
    "Enter or select a movie:", 
    movies['title'].dropna().unique(),
    index=0
)

recommend_clicked = st.sidebar.button("Get Recommendations")

if recommend_clicked:
    # Selected movie info with error handling
    try:
        selected_movie = movies[movies['title'] == selected_title].iloc[0]
        selected_url = selected_movie['tmdb_url']
        selected_tmdb_id = extract_tmdb_id(selected_url)
        selected_poster = fetch_poster(selected_tmdb_id)

        if selected_poster:
            st.sidebar.image(selected_poster, use_container_width=True)
        else:
            st.sidebar.image("https://via.placeholder.com/300x450.png?text=Poster+Not+Available", 
                           use_container_width=True)

        st.sidebar.markdown(f"**{selected_title}**")
        if selected_url and isinstance(selected_url, str):
            st.sidebar.markdown(f"[View on TMDB]({selected_url})")
    except Exception as e:
        st.sidebar.error(f"Error loading selected movie info: {e}")

    # Main area
    st.subheader(f"Recommendations for :  {selected_title}")
    st.markdown("---")

    with st.spinner('Finding similar movies...'):
        recommendations = recommend_movies(selected_title)

    # Grid of recommended movies with better loading
    cols_per_row = 5
    placeholder_img = "https://via.placeholder.com/300x450.png?text=Poster+Not+Available"

    for i in range(0, len(recommendations), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(recommendations):
                title, url, poster = recommendations[i + j]
                with col:
                    # Show loading spinner while image loads
                    with st.spinner(f'Loading {title}...'):
                        st.image(poster if poster else placeholder_img, 
                               use_container_width=True,
                               caption=title[:50] + ("..." if len(title) > 50 else ""))
                    
                    if url and isinstance(url, str):
                        st.markdown(f"[View on TMDB]({url})")
else:
    # Compact styling with reduced margins
    st.markdown("""
    <style>
    .title {
        font-size: 36px;
        text-align: center;
        margin-bottom: 5px !important;
        padding-top: 0px !important;
    }
    .divider {
        border-top: 2px solid #ddd;
        margin: 10px 0 !important;
    }
    .movie-title {
        font-size: 14px;
        text-align: center;
        margin: 5px 0 10px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title with minimal top spacing
    st.markdown("""
    <div style='margin-top: 0px; padding-top: 0px;'>
        <h1 class="title">🎥 Movie Recommendation System</h1>
        <hr class="divider">
    </div>
    """, unsafe_allow_html=True)

    # Updated dummy movies with Money Heist and 3 Idiots
    dummy_movies = [
        {"title": "The Shawshank Redemption", "poster": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"},
        {"title": "The Godfather", "poster": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"},
        {"title": "The Dark Knight", "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"},
        {"title": "Money Heist", "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg"},
        {"title": "3 Idiots", "poster": "https://image.tmdb.org/t/p/w500/66A9MqXOyVFCssoloscw79z8Tew.jpg"}
    ]

    # Titles row
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f'<p class="movie-title">{dummy_movies[i]["title"]}</p>', 
                       unsafe_allow_html=True)

    # Posters row
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(dummy_movies[i]["poster"], 
                   use_container_width=True)

    # Compact instructions
    st.markdown("""
    <div style="text-align: center; margin: 10px 0;">
        <h4>How to use:</h4>
        <ol style="display: inline-block; text-align: left; padding-left: 20px; margin: 5px 0;">
            <li>Select a movie from sidebar</li>
            <li>Click "Get Recommendations"</li>
            <li>Explore similar movies</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
