"""
model.py
--------
All data loading, preprocessing, and recommendation logic.
Imported by app.py (Streamlit UI).
"""

import os
import gdown
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# ── Audio features used for mood-based search ────────────────────────────────
AUDIO_FEATURES = [
    "danceability", "loudness", "acousticness",
    "instrumentalness", "valence", "energy"
]

# ── Load & preprocess ─────────────────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the CSV, clean it, and create the 'combined_features' column.
    If filepath is a Google Drive URL, downloads it first using gdown.
    """
    # If it's a Google Drive URL, download it first
    if "drive.google.com" in filepath:
        local_path = "/tmp/music_data.csv"
        if not os.path.exists(local_path):
            gdown.download(filepath, local_path, quiet=False, fuzzy=True)
        filepath = local_path

    df = pd.read_csv(filepath)
    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)
    df.dropna(subset=["artist_name", "track_name", "genre"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Combined text feature (genre + artist + track)
    df["combined_features"] = (
        df["genre"].fillna("") + " " +
        df["artist_name"].fillna("") + " " +
        df["track_name"].fillna("")
    )

    # Normalise audio features to [0, 1]
    existing_audio = [f for f in AUDIO_FEATURES if f in df.columns]
    scaler = MinMaxScaler()
    df[existing_audio] = scaler.fit_transform(df[existing_audio].fillna(0))

    return df


# ── TF-IDF similarity matrix ──────────────────────────────────────────────────
def build_tfidf_matrix(df: pd.DataFrame):
    """
    Build TF-IDF vectors and cosine similarity matrix.
    Capped at 10,000 rows so it runs fast in Streamlit.
    """
    sample = df.head(10_000).reset_index(drop=True)

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(sample["combined_features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return sample, cosine_sim


# ── Song-based recommendation ─────────────────────────────────────────────────
def get_recommendations(song_title: str, df: pd.DataFrame,
                        cosine_sim: np.ndarray, top_n: int = 10,
                        genre_filter: str = "All") -> pd.DataFrame:
    """
    Content-based recommendation by song title (TF-IDF cosine similarity).
    """
    idx_matches = df[df["track_name"].str.lower() == song_title.lower()].index

    if len(idx_matches) == 0:
        return pd.DataFrame()

    idx = idx_matches[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]  # exclude the song itself

    results = []
    for i, score in sim_scores:
        row = df.iloc[i].copy()
        if genre_filter != "All" and row["genre"] != genre_filter:
            continue
        row["similarity_score"] = round(score * 100, 1)
        results.append(row)
        if len(results) == top_n:
            break

    return pd.DataFrame(results) if results else pd.DataFrame()


# ── Mood-based recommendation (ALL 6 features) ───────────────────────────────
def get_recommendations_by_mood(
    energy: float = 0.5,
    valence: float = 0.5,
    danceability: float = 0.5,
    acousticness: float = 0.5,
    instrumentalness: float = 0.5,
    loudness: float = 0.5,
    df: pd.DataFrame = None,
    top_n: int = 10,
    genre_filter: str = "All"
) -> pd.DataFrame:
    """
    Recommend songs by all 6 audio feature values.
    Each parameter is a float in [0, 1].
    """
    existing_audio = [f for f in AUDIO_FEATURES if f in df.columns]

    feature_map = {
        "energy":            energy,
        "valence":           valence,
        "danceability":      danceability,
        "acousticness":      acousticness,
        "instrumentalness":  instrumentalness,
        "loudness":          loudness,
    }
    target = np.array([feature_map.get(f, 0.5) for f in existing_audio])

    scores = cosine_similarity([target], df[existing_audio])[0]
    ranked = np.argsort(scores)[::-1]

    results = []
    for idx in ranked:
        row = df.iloc[idx].copy()
        if genre_filter != "All" and row["genre"] != genre_filter:
            continue
        row["similarity_score"] = round(float(scores[idx]) * 100, 1)
        results.append(row)
        if len(results) == top_n:
            break

    return pd.DataFrame(results) if results else pd.DataFrame()


# ── EDA helpers ───────────────────────────────────────────────────────────────
def genre_distribution(df: pd.DataFrame) -> pd.Series:
    """Top genres by song count."""
    return df["genre"].value_counts()


def top_artists(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Top N artists by number of songs."""
    return df.groupby("artist_name").size().sort_values(ascending=False).head(n)


def audio_features_by_genre(df: pd.DataFrame, feature: str) -> pd.Series:
    """Mean value of an audio feature grouped by genre."""
    return df.groupby("genre")[feature].mean().sort_values(ascending=False)
