import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

API_KEY = '0e0d544ba3e8a3a047b177a52550d558'  

# Page Layout Config
st.set_page_config(page_title="MovieCommendor", layout="wide", page_icon="🎬")

# Custom CSS for Netflix Dark Mode Theme
# Custom CSS for Dark Theme & Bright Labels
st.markdown("""
    <style>
    .main {
        background-color: #141414;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #141414;
    }
    h1 {
        color: #E50914 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: bold;
    }
    .stSelectbox label {
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    .stButton>button {
        background-color: #E50914;
        color: white;
        border-radius: 4px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #b20710;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# TMDB API Details Fetching Function
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,videos"
    data = requests.get(url).json()
    
    # Poster
    poster_path = data.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
    
    # Overview & Release Date
    overview = data.get('overview', 'No description available.')[:100] + "..."
    release_date = data.get('release_date', 'N/A')[:4]
    rating = round(data.get('vote_average', 0), 1)
    
    # Director & Cast
    credits = data.get('credits', {})
    crew = credits.get('crew', [])
    cast = credits.get('cast', [])
    
    director = "Unknown"
    for member in crew:
        if member.get('job') == 'Director':
            director = member.get('name')
            break
            
    top_cast = [member.get('name') for member in cast[:2]]
    cast_names = ", ".join(top_cast) if top_cast else "N/A"
    
    # Trailer
    trailer_url = None
    videos = data.get('videos', {}).get('results', [])
    for video in videos:
        if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
            trailer_url = f"https://www.youtube.com/watch?v={video.get('key')}"
            break
            
    return {
        'poster': poster_url,
        'overview': overview,
        'year': release_date,
        'rating': rating,
        'director': director,
        'cast': cast_names,
        'trailer': trailer_url
    }

# Load Models
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# Recommendation Engine Function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    results = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        details = fetch_movie_details(movie_id)
        details['title'] = title
        results.append(details)
        
    return results

# UI Layout
st.markdown("<h1 style='text-align: center;'>🎬 MOVIECommendor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>Discover your next favorite movie with AI</p>", unsafe_allow_html=True)

st.write("---")

# Genre & Movie Selection Filters
col_filter1, col_filter2 = st.columns([1, 2])

with col_filter1:
    selected_genre = st.selectbox(
        'Filter by Category/Genre:',
        ['All', 'Action', 'Adventure', 'Comedy', 'Drama', 'Sci-Fi', 'Thriller']
    )

with col_filter2:
    selected_movie = st.selectbox(
        'Select or Type a Movie Name:',
        movies['title'].values
    )

if st.button('Get Recommendations 🚀'):
    results = recommend(selected_movie)
    st.write("### 🍿 Recommended Movies for You:")
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        item = results[idx]
        with col:
            st.image(item['poster'], use_container_width=True)
            st.subheader(f"{item['title']} ({item['year']})")
            st.caption(f"⭐ Rating: {item['rating']}/10")
            st.markdown(f"**🎬 Director:** {item['director']}")
            st.markdown(f"**🎭 Cast:** {item['cast']}")
            st.write(item['overview'])
            
            if item['trailer']:
                st.link_button("▶ Watch Trailer", item['trailer'])