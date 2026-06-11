# Spotify Streaming Trends 2023

**Author:** Andrew Mugisa

---

## Overview

An end-to-end data analysis project exploring what drives song popularity on Spotify, using a dataset of the platform's most-streamed tracks in 2023.

> **Central question:** Do musical attributes like tempo, energy, and danceability predict streaming success — or do distribution factors matter more?

---

## Key Finding

**Playlist exposure is the strongest predictor of streams.** Tracks appearing in more Spotify playlists consistently accumulate more streams. Audio features — BPM, energy, danceability — show negligible correlation. This emerged from the data and contradicted the original hypothesis.

---

## Live Dashboard

👉 **[View the interactive dashboard](https://andrewmugisa-most-spotify-streamed-songs-2023.streamlit.app)**

Built with Python (Streamlit + Plotly). Includes:
- Playlist appearances vs. streams scatter plot with trendline
- Top 20 most-streamed songs
- Average streams by release year
- Audio feature correlation chart
- Interactive feature explorer with live Pearson r

Sidebar filters: Release Year · Artist · Mode (Major / Minor)

---

## Repository Structure

```
├── app.py              # Interactive dashboard
├── spotify-2023.csv    # Dataset (952 tracks, 24 columns)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Dataset

Source: [Kaggle — Spotify Most Streamed Songs 2023](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023)

952 tracks · 24 columns · includes audio features, release metadata, and playlist/chart appearances across Spotify, Apple Music, and Deezer.

---

## Run Locally

```bash
git clone https://github.com/andrewmugisa/most_Spotify_streamed_songs_2023.git
cd most_Spotify_streamed_songs_2023
pip install -r requirements.txt
streamlit run app.py
```

---

## Tech Stack

Python · Pandas · Plotly · Streamlit · Statsmodels
