# 🎬 MovieCommendor - Movie Recommendation System

An interactive, end-to-end Machine Learning web application that recommends top movies based on content similarity using **Cosine Similarity** and **NLP Vectorization**.

🚀 **Live Demo:** [Click Here to View the App](https://movie-recommendation-system-u5e8ffthzjg85kejv6qyka.streamlit.app)

---

## 📌 Features
- **Smart Search & Filter:** Filter movies by category/genre or search directly.
- **Top 5 Recommendations:** Get instant, highly relevant movie recommendations.
- **Poster Integration:** Fetches high-quality official movie posters dynamically via TMDB API.
- **Optimized Model:** Float32 compressed similarity matrix (~88MB) for lightweight, high-speed execution.

---

## 🛠️ Tech Stack & Tools
- **Language:** Python
- **Data Processing & ML:** Pandas, NumPy, Scikit-learn (CountVectorizer, Cosine Similarity)
- **Deployment & UI:** Streamlit Cloud, Streamlit
- **Version Control:** Git, Git LFS

---

## ⚙️ How It Works
1. **Text Preprocessing:** Stemming and vectorization applied to tags (genres, keywords, cast, crew).
2. **Similarity Matrix:** Calculated using **Cosine Similarity** between text vectors.
3. **Data Compression:** Matrix downcasted to `float32` to meet production limits without sacrificing recommendation accuracy.
