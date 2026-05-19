# 🎬 CineMatch — Movie Recommendation System

An AI-powered, content-based movie recommender built with **Python**, **Scikit-learn**, and **Streamlit**. Pick any movie from 5,000+ titles and CineMatch instantly finds 8 movies you'll love — complete with posters, ratings, genres, and match scores pulled live from the TMDB API.

---

## 📌 Overview

CineMatch uses **content-based filtering** to recommend movies based on the features of a selected title — genres, cast, crew, keywords, and plot overview. All these are combined into a unified text corpus per movie, vectorised using a Bag-of-Words model, and ranked using **cosine similarity**.

The frontend is a fully custom **Streamlit** web app with a dark cinema aesthetic, animated hover cards, a personal watchlist, and a sidebar match-score chart.

---

## ✨ Features

- 🔍 **Search & Recommend** — Select any of 5,000+ movies and get 8 content-similar picks instantly
- 🎲 **Random Pick** — Let the engine surprise you with a random seed movie
- 🏠 **Trending Section** — Curated popular titles shown on the home screen
- 📌 **Watchlist** — Add/remove movies to a personal watch-later list (session-based)
- 📊 **Match Score Sidebar** — Visual progress bars showing the cosine similarity % for each recommendation
- 🎬 **Live Poster + Metadata** — Fetches poster, rating, year, genres, runtime, and overview from the TMDB API in real time
- 🌑 **Custom Dark UI** — Cinema-inspired dark theme with hover card overlays, `Bebas Neue` typography, and red/gold accent palette

---

## 🗂️ Repository Structure

```
Movie-Recommendation/
│
├── main.py                        # Streamlit web application (CineMatch UI)
├── movie_1.ipynb                  # Jupyter Notebook — EDA, feature engineering & model building
├── movie_list.pkl                 # Serialised DataFrame of movie titles & IDs
├── tmdb_5000_movies.csv           # TMDB movies dataset (metadata)
│
│   ── NOT IN REPO (size > 25 MB) ──
├── tmdb_5000_credits.csv          # TMDB credits dataset → download from Kaggle (link below)
└── similarity.pkl                 # Pre-computed cosine similarity matrix → generate via notebook
│
└── README.md
```

---

## 🛠️ Tech Stack

| Tool / Library | Purpose |
|----------------|---------|
| **Python 3.x** | Core language |
| **Pandas / NumPy** | Data manipulation |
| **Scikit-learn** | CountVectorizer, cosine similarity |
| **NLTK** | Stemming / text preprocessing |
| **Streamlit** | Interactive web app frontend |
| **Requests** | TMDB API calls for live poster & metadata |
| **Pickle** | Model and data serialisation |
| **Jupyter Notebook** | EDA and model development |

---

## 🤖 How It Works

```
Movie Selected
      │
      ▼
Feature Extraction
  ├── Genres
  ├── Keywords
  ├── Top 3 Cast
  ├── Director (Crew)
  └── Plot Overview
      │
      ▼
Text Corpus ("tags") per movie
      │
      ▼
CountVectorizer  →  5,000 × N Bag-of-Words matrix
      │
      ▼
Cosine Similarity  →  5,000 × 5,000 matrix
      │
      ▼
Top-8 Nearest Neighbours  →  Recommendations
      │
      ▼
TMDB API  →  Poster + Rating + Genres + Overview
```

---

## 📁 Dataset

**Source:** [TMDB 5000 Movie Dataset — Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

The dataset consists of two CSV files:

| File | Description | Size |
|------|-------------|------|
| `tmdb_5000_movies.csv` | Movie metadata — title, genres, keywords, overview, budget, revenue | ~5 MB ✅ in repo |
| `tmdb_5000_credits.csv` | Cast and crew information per movie | ~40 MB ⚠️ download separately |

> **⚠️ Note:** `tmdb_5000_credits.csv` exceeds GitHub's 25 MB file limit and is not included in this repository. Download it from the Kaggle link above and place it in the root directory before running the notebook.

Key columns used:

| Column | Source File | Used For |
|--------|-------------|---------|
| `movie_id` | movies | Linking with TMDB API |
| `title` | movies | Display and selection |
| `overview` | movies | Plot-based similarity |
| `genres` | movies | Feature tag |
| `keywords` | movies | Feature tag |
| `cast` | credits | Top 3 actors as feature |
| `crew` | credits | Director as feature |

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/mohanish0703/Movie-Recommendation.git
cd Movie-Recommendation
```

### 2. Install dependencies
```bash
pip install streamlit pandas numpy scikit-learn nltk requests
```

### 3. Download the missing dataset file
Download `tmdb_5000_credits.csv` from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) and place it in the root directory.

### 4. Generate the similarity matrix
Run the Jupyter notebook to preprocess the data and build the model:
```bash
jupyter notebook movie_1.ipynb
```
This will generate `similarity.pkl` and update `movie_list.pkl` in the root directory.

### 5. Launch the app
```bash
streamlit run main.py
```
Open your browser at `http://localhost:8501` 🎬

---

## 🔑 TMDB API

This project uses the [TMDB API](https://www.themoviedb.org/documentation/api) to fetch live movie posters, ratings, genres, and overviews. The API key is already configured in `main.py`.

If you encounter rate limits or want to use your own key, register at [themoviedb.org](https://www.themoviedb.org/) and replace the `TMDB_API_KEY` value in `main.py`.

---

## 🔍 Key Insights

- **Content-based filtering** is highly effective for cold-start scenarios (no user history needed)
- Combining multiple feature types (cast + genres + keywords + overview) significantly improves recommendation quality over single-feature approaches
- The **cosine similarity matrix** is the most memory-intensive artefact (~100–200 MB for 5,000 movies), which is why it's generated locally
- Stemming the tags corpus reduces vocabulary size and improves feature matching across similar words

---

## 👤 Author

**Mohanish**  
B.Tech Computer Science & Engineering  
Vellore Institute of Technology (VIT)  
[GitHub Profile](https://github.com/mohanish0703)

---

## 📄 Acknowledgements

- Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) on Kaggle
- Movie metadata API: [The Movie Database (TMDB)](https://www.themoviedb.org/)
