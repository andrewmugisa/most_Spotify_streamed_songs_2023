import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spotify Streaming Trends 2023",
    page_icon="🎵",
    layout="wide",
)

# ── Theme ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background-color: #111111; color: #ffffff; }
  section[data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #2a2a2a; }
  .metric-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
  }
  .metric-val { font-size: 28px; font-weight: 900; color: #1DB954; line-height: 1; }
  .metric-label { font-size: 10px; color: #a0a0a0; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 4px; }
  .section-title { font-size: 13px; font-weight: 700; color: #1DB954; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 4px; }
  .finding-box {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 8px;
    font-size: 12px;
    color: #c0c0c0;
    line-height: 1.6;
  }
  h1 { color: #ffffff !important; }
  .stSelectbox label, .stMultiSelect label, .stSlider label { color: #a0a0a0 !important; font-size: 12px !important; }
  div[data-testid="stMetric"] { background: #1a1a1a; border-radius: 10px; border: 1px solid #2a2a2a; padding: 12px; }
  div[data-testid="stMetric"] label { color: #a0a0a0 !important; }
  div[data-testid="stMetric"] div { color: #1DB954 !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Load & clean data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("spotify-2023.csv", encoding="latin-1")
    df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
    df = df.dropna(subset=["streams"])
    df["streams_m"] = (df["streams"] / 1_000_000).round(1)
    df["song_age"] = 2023 - df["released_year"]
    df.rename(columns={"artist(s)_name": "artist_name"}, inplace=True)
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.markdown("##    Filters")
st.sidebar.markdown("---")

years = sorted(df["released_year"].unique())
year_range = st.sidebar.slider(
    "Release Year", int(min(years)), int(max(years)),
    (2010, 2023)
)

all_artists = ["All Artists"] + sorted(df["artist_name"].unique().tolist())
selected_artist = st.sidebar.selectbox("Artist", all_artists)

mode_options = ["All"] + sorted(df["mode"].dropna().unique().tolist())
selected_mode = st.sidebar.selectbox("Mode (Major / Minor)", mode_options)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:10px; color:#666; line-height:1.6'>
<b style='color:#1DB954'>Key Finding:</b><br>
Playlist exposure is the strongest driver of streams not audio features like tempo or energy.
</div>
""", unsafe_allow_html=True)

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df[
    (df["released_year"] >= year_range[0]) &
    (df["released_year"] <= year_range[1])
]
if selected_artist != "All Artists":
    filtered = filtered[filtered["artist_name"] == selected_artist]
if selected_mode != "All":
    filtered = filtered[filtered["mode"] == selected_mode]

# ── Header ────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([0.05, 0.95])
with col_title:
    st.markdown("# 🎵 Spotify Streaming Trends 2023")
    st.markdown(
        "<p style='color:#a0a0a0; font-size:13px; margin-top:-10px;'>"
        "What actually drives a song's success? &nbsp;·&nbsp; Analysis by Andrew Mugisa &nbsp;·&nbsp; "
        f"Showing <b style='color:#1DB954'>{len(filtered):,}</b> of {len(df):,} tracks</p>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Tracks", f"{len(filtered):,}")
with k2:
    avg_streams = filtered["streams_m"].mean()
    st.metric("Avg Streams", f"{avg_streams:.0f}M")
with k3:
    top_streams = filtered["streams_m"].max()
    st.metric("Peak Streams", f"{top_streams:.0f}M")
with k4:
    avg_playlists = filtered["in_spotify_playlists"].mean()
    st.metric("Avg Playlists", f"{avg_playlists:,.0f}")
with k5:
    avg_dance = filtered["danceability_%"].mean()
    st.metric("Avg Danceability", f"{avg_dance:.0f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Playlist vs Streams + Top 20 ──────────────────────────────────────
col1, col2 = st.columns([1.1, 0.9])

PLOT_BG = "#111111"
PAPER_BG = "#111111"
GRID = "rgba(255,255,255,0.06)"
TICK = "#707070"
GREEN = "#1DB954"
RED = "#e85d5d"

def base_layout(title):
    return dict(
        title=dict(text=title, font=dict(color="#ffffff", size=13), x=0),
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=TICK, size=10),
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
    )

with col1:
    st.markdown("<div class='section-title'>Playlist Appearances vs. Streams</div>", unsafe_allow_html=True)
    st.caption("Each dot is a track the trend shows playlist exposure drives stream count")

    scatter_df = filtered.copy()
    fig1 = px.scatter(
        scatter_df,
        x="in_spotify_playlists",
        y="streams_m",
        hover_name="track_name",
        hover_data={"artist_name": True, "streams_m": ":.0f", "in_spotify_playlists": True},
        trendline="ols",
        color_discrete_sequence=[GREEN],
        opacity=0.6,
        labels={"in_spotify_playlists": "Number of Spotify Playlists", "streams_m": "Streams (Millions)"},
    )
    fig1.update_traces(marker=dict(size=5), selector=dict(mode="markers"))
    fig1.update_traces(line=dict(color=RED, width=2), selector=dict(mode="lines"))
    fig1.update_layout(**base_layout(""))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("<div class='section-title'>Top 20 Songs by Streams</div>", unsafe_allow_html=True)
    st.caption("Most streamed tracks in the filtered selection")

    top20 = filtered.nlargest(20, "streams_m")[["track_name", "artist_name", "streams_m"]].copy()
    top20["label"] = top20["track_name"].str[:28]
    fig2 = go.Figure(go.Bar(
        x=top20["streams_m"],
        y=top20["label"],
        orientation="h",
        marker_color=GREEN,
        marker_opacity=0.85,
        hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>%{x:.0f}M streams<extra></extra>",
        customdata=top20[["track_name", "artist_name"]].values,
    ))
    layout2 = base_layout("")
    layout2["yaxis"] = dict(autorange="reversed", gridcolor=GRID, tickfont=dict(size=9))
    layout2["xaxis"] = dict(gridcolor=GRID, title="Streams (Millions)")
    layout2["height"] = 420
    fig2.update_layout(**layout2)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Release Year + Correlation ────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("<div class='section-title'>Average Streams by Release Year</div>", unsafe_allow_html=True)
    st.caption("Older tracks score higher more time to accumulate. 2023 releases appear low but are simply newer.")

    year_df = filtered.groupby("released_year")["streams_m"].mean().reset_index()
    year_df.columns = ["Year", "Avg Streams (M)"]
    year_df = year_df[year_df["Year"] >= 2010]

    fig3 = go.Figure(go.Scatter(
        x=year_df["Year"],
        y=year_df["Avg Streams (M)"],
        mode="lines+markers",
        line=dict(color=GREEN, width=2.5),
        marker=dict(color=GREEN, size=6),
        fill="tozeroy",
        fillcolor="rgba(29,185,84,0.1)",
        hovertemplate="<b>%{x}</b><br>Avg Streams: %{y:.0f}M<extra></extra>",
    ))
    layout3 = base_layout("")
    layout3["xaxis"] = dict(gridcolor=GRID, dtick=1)
    layout3["yaxis"] = dict(gridcolor=GRID, title="Avg Streams (M)")
    fig3.update_layout(**layout3)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("<div class='section-title'>Audio Feature Correlations with Streams</div>", unsafe_allow_html=True)
    st.caption("Pearson r how strongly each feature relates to stream count")

    features = ["in_spotify_playlists", "danceability_%", "released_year",
                "acousticness_%", "valence_%", "energy_%", "bpm"]
    labels   = ["Playlist Count", "Danceability", "Release Year",
                "Acousticness", "Valence", "Energy", "BPM"]

    corrs = [filtered[f].corr(filtered["streams_m"]) for f in features]
    colors = [GREEN if c >= 0 else RED for c in corrs]

    sorted_data = sorted(zip(corrs, labels, colors), key=lambda x: x[0])
    corrs_s, labels_s, colors_s = zip(*sorted_data)

    fig4 = go.Figure(go.Bar(
        x=list(corrs_s), y=list(labels_s),
        orientation="h",
        marker_color=list(colors_s),
        marker_opacity=0.8,
        hovertemplate="<b>%{y}</b><br>r = %{x:.3f}<extra></extra>",
    ))
    layout4 = base_layout("")
    layout4["xaxis"] = dict(gridcolor=GRID, range=[-0.25, 0.65], title="Pearson r")
    layout4["yaxis"] = dict(gridcolor=GRID, tickfont=dict(size=10))
    layout4["shapes"] = [dict(type="line", x0=0, x1=0, y0=-0.5, y1=len(labels)-0.5,
                     line=dict(color="#555", width=1, dash="dot"))]
    fig4.update_layout(**layout4)
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Audio feature explorer ────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-title'>Audio Feature Explorer</div>", unsafe_allow_html=True)
st.caption("Select any audio feature to see its relationship with streams across the filtered dataset")

feat_col, chart_col = st.columns([0.25, 0.75])
with feat_col:
    feature_map = {
        "Danceability (%)": "danceability_%",
        "Energy (%)": "energy_%",
        "Valence (%)": "valence_%",
        "Acousticness (%)": "acousticness_%",
        "BPM": "bpm",
        "Liveness (%)": "liveness_%",
        "Speechiness (%)": "speechiness_%",
    }
    chosen = st.selectbox("Choose feature", list(feature_map.keys()))
    st.markdown("<br>", unsafe_allow_html=True)
    r_val = filtered[feature_map[chosen]].corr(filtered["streams_m"])
    direction = "positive" if r_val > 0.05 else ("negative" if r_val < -0.05 else "no meaningful")
    st.markdown(f"""
    <div class='finding-box'>
    <b style='color:#1DB954'>r = {r_val:.3f}</b><br>
    {chosen} shows <b>{direction}</b> correlation with streams in the current selection.
    </div>
    """, unsafe_allow_html=True)

with chart_col:
    fig5 = px.scatter(
        filtered,
        x=feature_map[chosen],
        y="streams_m",
        hover_name="track_name",
        hover_data={"artist_name": True, "streams_m": ":.0f"},
        trendline="ols",
        color_discrete_sequence=[GREEN],
        opacity=0.55,
        labels={feature_map[chosen]: chosen, "streams_m": "Streams (Millions)"},
    )
    fig5.update_traces(marker=dict(size=5), selector=dict(mode="markers"))
    fig5.update_traces(line=dict(color=RED, width=2), selector=dict(mode="lines"))
    fig5.update_layout(**base_layout(""))
    st.plotly_chart(fig5, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='font-size:10px; color:#555; text-align:center;'>"
    "Source: Kaggle - Spotify Most Streamed Songs 2023 &nbsp;·&nbsp; "
    "Analysis: Andrew Mugisa &nbsp;·&nbsp; Portfolio Project Deliverable #6"
    "</p>",
    unsafe_allow_html=True
)
