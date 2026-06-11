# Spotify Streaming Trends 2023

**Portfolio Project — Amazon Data Analytics Cohort 19**  
**Author:** Andrew Mugisa  

---

## Overview

This project analyses the [Spotify Most Streamed Songs 2023](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023) dataset from Kaggle to answer one question:

> **What actually drives a song's streaming success — musical qualities like tempo and energy, or distribution factors like playlist placement?**

The project covers the full data analysis lifecycle: scoping, data curation, exploratory data analysis, a one-page Datafolio, and an interactive dashboard.

---

## Key Finding

**Playlist exposure is the strongest predictor of streams.** Tracks appearing in more Spotify playlists consistently accumulate more streams. Audio features — BPM, energy, danceability — show negligible correlation with stream count. This was not anticipated in the original project scoping but emerged clearly from the data.

---

## Repository Structure

```
├── app.py                  # Streamlit dashboard (Deliverable #6)
├── spotify-2023.csv        # Cleaned dataset (952 tracks, 24 columns)
├── requirements.txt        # Python dependencies for Streamlit Cloud
└── README.md
```

---

## Dashboard

**Live:** [Streamlit Cloud deployment](https://share.streamlit.io)

The dashboard includes:

| Chart | Description |
|---|---|
| Playlist Appearances vs. Streams | Scatter with OLS trendline — the headline finding |
| Top 20 Songs by Streams | Horizontal bar — filters live with sidebar |
| Avg Streams by Release Year | Line chart — shows accumulation effect over time |
| Audio Feature Correlations | Pearson r for all features vs streams |
| Audio Feature Explorer | Interactive — pick any feature, see its scatter + r value |

**Filters:** Release Year range · Artist · Mode (Major / Minor)

---

## Dataset

| Field | Description |
|---|---|
| `track_name` | Song title |
| `artist_name` | Artist(s) |
| `streams` | Total Spotify streams (target variable) |
| `in_spotify_playlists` | Number of playlists featuring the track |
| `released_year` | Year the song was originally released |
| `bpm` | Tempo in beats per minute |
| `danceability_%` | Suitability for dancing (0–100) |
| `energy_%` | Track intensity (0–100) |
| `valence_%` | Musical positivity (0–100) |
| `acousticness_%` | Acoustic instrumentation level (0–100) |
| `mode` | Major or Minor |
| `key` | Musical key |

**Note:** `released_year` reflects when each song was originally published — not a streaming year. The dataset is a 2023 snapshot of the most-streamed songs, so older tracks appear to have higher average streams simply because they have had more time to accumulate plays.

---

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/andrewmugisa/most_Spotify_streamed_songs_2023.git
cd most_Spotify_streamed_songs_2023

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

---

## Dependencies

```
streamlit >= 1.32.0
pandas >= 2.0.0
plotly >= 5.18.0
numpy >= 1.26.0
scipy >= 1.12.0
statsmodels >= 0.14.0
```

---

## Project Deliverables

| # | Deliverable | Status |
|---|---|---|
| 1 | Project Description | ✅ Pass |
| 2 | Project Scoping | ✅ Pass |
| 3 | Data Curation | ✅ Pass |
| 4 | Exploratory Data Analysis | ✅ Pass |
| 5 | Datafolio | ⏳ Submitted |
| 6 | Dashboard | ⏳ Submitted |

---

## Acknowledgements

Dataset: [Nidula Elgiriyewithana on Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023)  
Programme: Amazon Data Analytics Cohort 19 (AMZN-DANA-019)
