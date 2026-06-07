"""
model.py
--------
All data loading, preprocessing, and recommendation logic.
Imported by app.py (Streamlit UI).
"""

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
    Load the CSV, clean it, and create the 'combined_features' column
    used by TF-IDF (same approach as the notebook).
    """
    df = pd.read_csv(filepath)
    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)
    df.dropna(subset=["artist_name", "track_name", "genre"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Combined text feature (genre + artist + track) — from notebook Step 4
    df["combined_features"] = (
        df["genre"].fillna("") + " " +
        df["artist_name"].fillna("") + " " +
        df["track_name"].fillna("")
    )

    # Normalise audio features for mood-based filtering
    existing_audio = [f for f in AUDIO_FEATURES if f in df.columns]
    scaler = MinMaxScaler()
    df[existing_audio] = scaler.fit_transform(df[existing_audio].fillna(0))

    return df


# ── TF-IDF similarity matrix ──────────────────────────────────────────────────
def build_tfidf_matrix(df: pd.DataFrame):
    """
    Build TF-IDF vectors and cosine similarity matrix.
    Capped at 10,000 rows so it runs fast in Streamlit.

    Returns
    -------
    sample      : filtered DataFrame (up to 10k rows)
    cosine_sim  : (N x N) cosine similarity matrix
    """
    sample = df.head(10_000).reset_index(drop=True)

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(sample["combined_features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return sample, cosine_sim


# ── Recommendation functions ──────────────────────────────────────────────────
def get_recommendations(song_title: str, df: pd.DataFrame,
                        cosine_sim: np.ndarray, top_n: int = 10,
                        genre_filter: str = "All") -> pd.DataFrame:
    """
    Content-based recommendation by song title (TF-IDF cosine similarity).
    Mirrors the notebook's get_recommendations() but adds genre filter.

    Parameters
    ----------
    song_title   : exact track name to look up
    df           : sample DataFrame (same one used to build cosine_sim)
    cosine_sim   : precomputed similarity matrix
    top_n        : number of results
    genre_filter : "All" or a specific genre string

    Returns
    -------
    DataFrame of recommended songs with a 'similarity_score' column (0–100)
    """
    idx_matches = df[df["track_name"].str.lower() == song_title.lower()].index

    if len(idx_matches) == 0:
        return pd.DataFrame()  # caller handles empty result

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


def get_recommendations_by_mood(energy: float, valence: float,
                                danceability: float, df: pd.DataFrame,
                                top_n: int = 10,
                                genre_filter: str = "All") -> pd.DataFrame:
    """
    Recommend songs by target audio feature values (mood sliders).
    Uses cosine similarity against a target vector built from the sliders.

    Parameters
    ----------
    energy, valence, danceability : float in [0, 1]
    df           : full DataFrame (already normalised)
    top_n        : number of results
    genre_filter : "All" or a specific genre string
    """
    existing_audio = [f for f in AUDIO_FEATURES if f in df.columns]

    # Build target vector (everything 0 except the three slider features)
    target = np.zeros(len(existing_audio))
    for feat, val in [("energy", energy), ("valence", valence),
                      ("danceability", danceability)]:
        if feat in existing_audio:
            target[existing_audio.index(feat)] = val

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