"""
app.py
------
Streamlit UI for the Music Recommendation System.
All ML logic lives in model.py.

Run:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from model import (
    load_data,
    build_tfidf_matrix,
    get_recommendations,
    get_recommendations_by_mood,
    genre_distribution,
    top_artists,
    audio_features_by_genre,
    AUDIO_FEATURES,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎵 Music Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background-color: #0d0d1a; }
  [data-testid="stSidebar"]          { background-color: #111122; }
  h1  { color: #1DB954; font-size: 2.2rem; }
  h2, h3 { color: #e0e0e0; }
  .song-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-left: 4px solid #1DB954;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.55rem;
  }
  .song-title  { font-size: 1rem; font-weight: 700; color: #ffffff; }
  .song-meta   { font-size: 0.82rem; color: #888; margin-top: 3px; }
  .badge       { display:inline-block; border-radius:20px; padding:2px 9px;
                 font-size:0.72rem; font-weight:700; margin-right:4px; }
  .badge-green { background:#1DB954; color:#000; }
  .badge-purple{ background:#7c3aed; color:#fff; }
  .score-box   { text-align:right; }
  .score-num   { font-size:1.2rem; font-weight:700; color:#1DB954; }
  .score-lbl   { font-size:0.72rem; color:#666; }

  /* Live search dropdown styling */
  .search-suggestion {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: background 0.15s;
  }
  .search-suggestion:hover {
    background: #22223e;
    border-color: #1DB954;
  }
  .sug-icon { color: #1DB954; font-size: 1rem; }
  .sug-title { color: #fff; font-size: 0.9rem; font-weight: 600; }
  .sug-artist { color: #888; font-size: 0.78rem; }
  .sug-genre { color: #1DB954; font-size: 0.72rem; background: #0d2e1a; border-radius: 10px; padding: 1px 7px; }
</style>
""", unsafe_allow_html=True)


# ── Load data (cached so it only runs once) ───────────────────────────────────
@st.cache_data(show_spinner="Loading dataset…")
def cached_load(path):
    return load_data(path)


@st.cache_data(show_spinner="Building similarity matrix…")
def cached_matrix(_df):
    return build_tfidf_matrix(_df)

DATA_PATH = "https://drive.google.com/uc?id=1kMX-fyIhw5shzDW-c7hWsENA_3PiSTaQ"
df        = cached_load(DATA_PATH)
sample, cosine_sim = cached_matrix(df)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎵 Music Recommender")
    st.caption(f"**{len(df):,} songs** · {df['genre'].nunique()} genres")
    st.divider()

    page = st.radio(
        "Navigate",
        ["🔍 Song-Based", "🎛️ Mood-Based", "📊 EDA"],
        label_visibility="collapsed",
    )
    st.divider()

    genre_filter = st.selectbox(
        "Filter by Genre",
        ["All"] + sorted(df["genre"].dropna().unique().tolist()),
    )
    top_n = st.slider("Number of Recommendations", 4, 20, 10)


# ── Helpers ───────────────────────────────────────────────────────────────────
def render_song_card(row: pd.Series, rank: int):
    score = row.get("similarity_score", "–")
    genre = row.get("genre", "")
    topic = row.get("topic", "")
    year  = int(row.get("release_date", 0))
    nrg   = row.get("energy", 0)
    bars  = "█" * int(nrg * 10) + "░" * (10 - int(nrg * 10))

    st.markdown(f"""
    <div class="song-card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <div class="song-title">#{rank} &nbsp; {row['track_name']}</div>
          <div class="song-meta">🎤 {row['artist_name']} &nbsp;·&nbsp; 📅 {year}</div>
          <div style="margin-top:5px;">
            <span class="badge badge-green">{genre}</span>
            <span class="badge badge-purple">{topic}</span>
          </div>
        </div>
        <div class="score-box">
          <div class="score-num">{score}%</div>
          <div class="score-lbl">match</div>
          <div style="font-size:0.75rem;color:#444;margin-top:4px;">{bars}</div>
          <div class="score-lbl">energy</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)


def seaborn_fig(plot_fn, title=""):
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#0d0d1a")
    ax.set_facecolor("#111122")
    ax.tick_params(colors="#aaa")
    ax.xaxis.label.set_color("#aaa")
    ax.yaxis.label.set_color("#aaa")
    ax.title.set_color("#e0e0e0")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    plot_fn(ax)
    if title:
        ax.set_title(title, color="#e0e0e0")
    st.pyplot(fig)
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Song-Based Recommendations  (LIVE SEARCH)
# ════════════════════════════════════════════════════════════════════════════
if page == "🔍 Song-Based":
    st.markdown("# 🔍 Song-Based Recommendations")
    st.markdown("Uses **TF-IDF + Cosine Similarity** on genre, artist, and track name.")
    st.divider()

    # ── Search type toggle ────────────────────────────────────────────────
    search_by = st.radio("Search by", ["Song title", "Artist"], horizontal=True)

    # ── Live search input ─────────────────────────────────────────────────
    query = st.text_input(
        "🔎 Start typing to see suggestions…",
        placeholder="e.g.  cry,  love,  beatles,  eminem",
        key="live_search"
    )

    # ── Session state to track selected song ─────────────────────────────
    if "selected_song_idx" not in st.session_state:
        st.session_state.selected_song_idx = None
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    # Reset selection if query changed
    if query != st.session_state.last_query:
        st.session_state.selected_song_idx = None
        st.session_state.last_query = query

    # ── Live suggestions dropdown ─────────────────────────────────────────
    if query and st.session_state.selected_song_idx is None:
        field = "track_name" if search_by == "Song title" else "artist_name"
        # Search the FULL dataset (all 28k songs), not just sample
        hits = df[df[field].str.contains(query, case=False, na=False)].head(8)

        if hits.empty:
            st.warning("🔍 No matches found — try a different keyword.")
        else:
            st.markdown(f"<div style='color:#888;font-size:0.82rem;margin-bottom:6px;'>Showing {len(hits)} suggestions — click one to select</div>", unsafe_allow_html=True)

            for i, (df_idx, row) in enumerate(hits.iterrows()):
                col_btn, col_info = st.columns([1, 9])
                with col_info:
                    st.markdown(f"""
                    <div class="search-suggestion">
                      <span class="sug-icon">🎵</span>
                      <div>
                        <div class="sug-title">{row['track_name']}</div>
                        <div class="sug-artist">🎤 {row['artist_name']} &nbsp;·&nbsp; 📅 {int(row.get('release_date',0))}</div>
                      </div>
                      <span class="sug-genre">{row.get('genre','')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    if st.button("▶ Pick", key=f"pick_{i}_{df_idx}"):
                        st.session_state.selected_song_idx = df_idx
                        st.rerun()

    # ── Show selected song + recommendations ──────────────────────────────
    if st.session_state.selected_song_idx is not None:
        # Use full df for display, fall back to sample if idx out of range
        if st.session_state.selected_song_idx in sample.index:
            chosen_row = sample.loc[st.session_state.selected_song_idx]
        else:
            chosen_row = df.loc[st.session_state.selected_song_idx]

        # Selected song card
        st.markdown(f"""
        <div class="song-card" style="border-color:#7c3aed; margin-top:10px;">
          <div class="song-title">▶ &nbsp; {chosen_row['track_name']}</div>
          <div class="song-meta">
            🎤 {chosen_row['artist_name']} &nbsp;·&nbsp;
            📅 {int(chosen_row.get('release_date', 0))} &nbsp;·&nbsp;
            {chosen_row.get('genre','')} &nbsp;·&nbsp; {chosen_row.get('topic','')}
          </div>
        </div>""", unsafe_allow_html=True)

        col_btn, col_clear = st.columns([3, 1])
        with col_btn:
            get_recs = st.button("🎯 Get Recommendations", use_container_width=True)
        with col_clear:
            if st.button("✖ Clear", use_container_width=True):
                st.session_state.selected_song_idx = None
                st.session_state.last_query = ""
                st.rerun()

        if get_recs:
            song_name = chosen_row["track_name"]
            artist_name = chosen_row["artist_name"]
            # If song is outside the 10k sample, find it by name/artist in sample
            if st.session_state.selected_song_idx not in sample.index:
                match = sample[sample["track_name"].str.lower() == song_name.lower()]
                if match.empty:
                    match = sample[sample["artist_name"].str.lower() == artist_name.lower()]
                if not match.empty:
                    song_name = match.iloc[0]["track_name"]
                else:
                    st.warning("This song is outside the similarity matrix range. Showing similar artist results.")
                    song_name = None
            if song_name:
                recs = get_recommendations(
                    song_name, sample, cosine_sim,
                    top_n=top_n, genre_filter=genre_filter
                )
                if recs.empty:
                    st.info("No recommendations found with current filters.")
                else:
                    st.markdown(f"### 🎶 Top {len(recs)} Similar Songs")
                    for rank, (_, row) in enumerate(recs.iterrows(), 1):
                        render_song_card(row, rank)

    elif not query:
        st.info("👆 Start typing a song or artist name to see live suggestions.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Mood-Based Recommendations
# ════════════════════════════════════════════════════════════════════════════
elif page == "🎛️ Mood-Based":
    st.markdown("# 🎛️ Mood-Based Recommendations")
    st.markdown("Click a mood feature below to expand its slider, then hit **Find Songs**.")
    st.divider()

    # ── All 6 mood features with metadata ────────────────────────────────
    MOOD_FEATURES = [
        {
            "key":   "energy",
            "label": "⚡ Energy",
            "desc":  "Intensity & activity level of the song. High energy = fast, loud, noisy. Low = slow, quiet, calm.",
            "color": "#FF6B35",
            "low":   "😌 Low Energy",
            "high":  "🔥 High Energy",
        },
        {
            "key":   "valence",
            "label": "😊 Positivity (Valence)",
            "desc":  "Musical positiveness. High valence = happy, cheerful, euphoric. Low = sad, depressed, angry.",
            "color": "#FFD700",
            "low":   "😔 Melancholic",
            "high":  "😄 Happy",
        },
        {
            "key":   "danceability",
            "label": "💃 Danceability",
            "desc":  "How suitable the track is for dancing based on tempo, rhythm stability, and beat strength.",
            "color": "#1DB954",
            "low":   "🎼 Laid-back",
            "high":  "🕺 Danceable",
        },
        {
            "key":   "acousticness",
            "label": "🎸 Acousticness",
            "desc":  "Confidence that the track is acoustic (non-electronic). High = acoustic guitar, piano. Low = synthesised.",
            "color": "#A78BFA",
            "low":   "🎛️ Electronic",
            "high":  "🎸 Acoustic",
        },
        {
            "key":   "instrumentalness",
            "label": "🎺 Instrumentalness",
            "desc":  "Predicts whether a track has no vocals. High = purely instrumental. Low = has singing.",
            "color": "#38BDF8",
            "low":   "🎤 Has Vocals",
            "high":  "🎺 Instrumental",
        },
        {
            "key":   "loudness",
            "label": "🔊 Loudness",
            "desc":  "Overall loudness of the track (normalised). High = loud/punchy. Low = quiet/soft.",
            "color": "#FB7185",
            "low":   "🤫 Quiet",
            "high":  "📢 Loud",
        },
    ]

    # ── Session state for expanded feature ───────────────────────────────
    if "expanded_mood" not in st.session_state:
        st.session_state.expanded_mood = None

    # ── CSS for mood boxes ────────────────────────────────────────────────
    st.markdown("""
    <style>
    .mood-box {
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        border: 2px solid transparent;
        transition: all 0.2s;
    }
    .mood-box-title { font-size: 1rem; font-weight: 700; color: #fff; }
    .mood-box-desc  { font-size: 0.78rem; color: #bbb; margin-top: 4px; }
    .mood-box-tags  { margin-top: 8px; display: flex; gap: 8px; }
    .mood-tag { font-size: 0.72rem; background: rgba(255,255,255,0.12);
                border-radius: 20px; padding: 2px 10px; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

    # ── Slider values dict ────────────────────────────────────────────────
    slider_values = {}

    # ── Render each mood feature box ─────────────────────────────────────
    for feat in MOOD_FEATURES:
        k     = feat["key"]
        color = feat["color"]
        is_open = (st.session_state.expanded_mood == k)
        bg    = f"background: linear-gradient(135deg, {color}22, {color}11); border-color: {color};" if is_open else "background: #1a1a2e; border-color: #2a2a4e;"

        st.markdown(f"""
        <div class="mood-box" style="{bg}">
          <div class="mood-box-title" style="color:{color};">{feat['label']}</div>
          <div class="mood-box-desc">{feat['desc']}</div>
          <div class="mood-box-tags">
            <span class="mood-tag">{feat['low']}</span>
            <span class="mood-tag">→</span>
            <span class="mood-tag">{feat['high']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_toggle, col_slider = st.columns([1, 4])
        with col_toggle:
            btn_label = "▲ Close" if is_open else "▼ Open"
            if st.button(btn_label, key=f"toggle_{k}"):
                st.session_state.expanded_mood = None if is_open else k
                st.rerun()

        if is_open:
            with col_slider:
                slider_values[k] = st.slider(
                    feat["label"], 0.0, 1.0, 0.5, 0.05,
                    key=f"slider_{k}"
                )
        else:
            slider_values[k] = 0.5   # default when not opened

    st.divider()

    # ── Active mood summary ───────────────────────────────────────────────
    if st.session_state.expanded_mood:
        active = next(f for f in MOOD_FEATURES if f["key"] == st.session_state.expanded_mood)
        val    = slider_values[st.session_state.expanded_mood]
        mood_word = active["high"] if val >= 0.5 else active["low"]
        st.markdown(f"**Selected mood:** &nbsp; `{active['label']}` &nbsp; → &nbsp; `{mood_word}` &nbsp; ({val})")
    else:
        st.info("👆 Click ▼ Open on any feature above to set its value.")

    st.divider()

    if st.button("🎵 Find Songs", use_container_width=True):
        recs = get_recommendations_by_mood(
            energy          = slider_values.get("energy", 0.5),
            valence         = slider_values.get("valence", 0.5),
            danceability    = slider_values.get("danceability", 0.5),
            acousticness    = slider_values.get("acousticness", 0.5),
            instrumentalness= slider_values.get("instrumentalness", 0.5),
            loudness        = slider_values.get("loudness", 0.5),
            df=df, top_n=top_n, genre_filter=genre_filter
        )
        if recs.empty:
            st.info("No results — try adjusting the genre filter.")
        else:
            st.markdown(f"### 🎶 Top {len(recs)} Songs for Your Mood")
            for rank, (_, row) in enumerate(recs.iterrows(), 1):
                render_song_card(row, rank)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — EDA
# ════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("# 📊 Exploratory Data Analysis")
    st.markdown("Visual breakdown of the dataset — same charts as the notebook.")
    st.divider()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Songs",  f"{len(df):,}")
    m2.metric("Genres",       df["genre"].nunique())
    m3.metric("Artists",      df["artist_name"].nunique())
    m4.metric("Year Range",   f"{int(df['release_date'].min())} – {int(df['release_date'].max())}")
    st.divider()

    st.markdown("### 🎸 Top 10 Genres by Song Count")
    gen_counts = genre_distribution(df).head(10)
    def plot_genres(ax):
        sns.barplot(x=gen_counts.values, y=gen_counts.index, palette="viridis", ax=ax)
        ax.set_xlabel("Count"); ax.set_ylabel("Genre")
    seaborn_fig(plot_genres, "Top 10 Genres")

    st.markdown("### 🎤 Top 10 Artists by Number of Songs")
    artists = top_artists(df, 10)
    def plot_artists(ax):
        sns.barplot(x=artists.values, y=artists.index, palette="viridis", ax=ax)
        ax.set_xlabel("Number of Songs"); ax.set_ylabel("Artist Name")
    seaborn_fig(plot_artists, "Top 10 Artists")

    st.markdown("### 🎼 Audio Feature by Genre")
    feat_choice = st.selectbox("Select audio feature", AUDIO_FEATURES)
    feat_data   = audio_features_by_genre(df, feat_choice)
    def plot_feat(ax):
        sns.barplot(x=feat_data.values, y=feat_data.index, palette="coolwarm", ax=ax)
        ax.set_xlabel(f"Mean {feat_choice}"); ax.set_ylabel("Genre")
    seaborn_fig(plot_feat, f"Mean {feat_choice.title()} by Genre")

    st.markdown("### 🗂️ Topic Distribution")
    topic_counts = df["topic"].value_counts()
    def plot_topics(ax):
        sns.barplot(x=topic_counts.values, y=topic_counts.index, palette="magma", ax=ax)
        ax.set_xlabel("Count"); ax.set_ylabel("Topic")
    seaborn_fig(plot_topics, "Song Topics")

    st.markdown("### 📋 Raw Data Sample")
    st.dataframe(
        df[["artist_name", "track_name", "genre", "topic",
            "release_date", "energy", "valence", "danceability"]].head(100),
        use_container_width=True,
    )
