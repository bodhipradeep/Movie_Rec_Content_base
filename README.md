# 🎬 Content-Based Movie Recommendation System with KNN

---

![Main Dashboard](https://your-link.com/dashboard.png)
*Main dashboard where users can explore movies and trigger recommendations*

---

## Overview

This project is a **Content-Based Movie Recommender System** built with **K-Nearest Neighbors (KNN)** and **TF-IDF** text embeddings to suggest similar movies based on user selection. It features a fully interactive **Streamlit** interface and integrates with **TMDB** to fetch live movie posters.

Once a user selects a movie from the sidebar, the app finds the most similar movies based on text similarity of their metadata (like genres, tags, etc.). Posters and links to the TMDB website are also shown.

---

![Recommendations View](https://your-link.com/recommendations.png)
*Example of the interface after generating recommendations*

---

## Key Features

- 🔍 **Interactive Movie Selection**: Choose a movie from a searchable dropdown
- 🧠 **TF-IDF + KNN Based Similarity**: Finds similar movies using vectorized content
- 🖼️ **Poster Integration**: Fetches movie posters live from the TMDB API
- ⚡ **Fast & Cached**: Uses Streamlit caching for fast response times
- 🔁 **Retry-Logic**: Handles TMDB API errors and rate limits gracefully
- 📊 **Responsive Layout**: Grid layout for poster display with adaptive styling

---

## How it Works

1. A **TF-IDF matrix** is computed over movie metadata (not shown in this repo).
2. A **KNN model** is trained on the TF-IDF vectors to find nearest neighbors.
3. The user selects a movie via the sidebar.
4. The system finds top-N similar movies based on cosine similarity.
5. Posters and links are fetched using TMDB movie IDs.

---

## File Structure

```bash
.
├── app.py                            # Streamlit web app
├── content_based_rec_with_knn.ipynb  # Notebook to generate TF-IDF & train KNN
├── knn_model.pkl                     # Pickled trained KNN model
├── tfidf_matrix.pkl                  # Pickled TF-IDF matrix
├── movies_processed.csv              # Processed movie metadata (must be present)
```

---

## Technology Stack
- Python
- Streamlit
- Pandas
- Scikit-learn
- TF-IDF Vectorizer
- KNN (cosine similarity)
- TMDB API

---

## 📄 License

This repository is licensed under the MIT License. See the LICENSE file for details.

--- 

## 🔗 **Links & Contact**

- **GitHub Profile:** [Github](https://github.com/pradeep-kumar8/)
- **LinkedIn:** [Likedin](https://linkedin.com/in/pradeep-kumar8)
- **Email:** [gmail](mailto:pradeep.kmr.pro@gmail.com)
