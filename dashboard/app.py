"""
app.py — Final display stage of the RAP pipeline

Dashboard Features:
  - To write out

Two functions:
  load_data()  — connects to the SQLite database, retrieves the cleaned data, and returns it as a DataFrame for use in the dashboard.

"""

import os

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_data():
    # Get database credentials from environment variables
    db_path = os.getenv('DB_PATH')

    # Create database connection string
    connection_string = f'sqlite:///{db_path}'

    # Create SQLAlchemy engine
    engine = create_engine(connection_string)

    # Load data into DataFrames
    regular_season_df = pd.read_sql("SELECT * FROM regular_season", engine)
    playoffs_df = pd.read_sql("SELECT * FROM playoffs", engine)

    return regular_season_df, playoffs_df


# Page configuration
st.set_page_config(
    page_title="NBA Referee Dashboard", 
    layout="wide"
    )

# --- Theme ---
st.markdown(
    """
    <style>
        .stApp { background-color: #1a1f2e; color: #ffffff; }
        .stSidebar { background-color: #12172a; }
        h1, h2, h3 { color: #ffffff; }
        .stDataFrame { background-color: #12172a; }
    </style>
    """, 
    unsafe_allow_html=True)

# Load Data
try:
    regular_season_df, playoffs_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Title
st.title("NBA Referee Analytics")
st.caption("For the 2025-2026 Season | Source: NBAStuffer")


# Sidebar
st.sidebar.header("Filters")

all_referees = sorted(regular_season_df['referee'].unique().tolist())

selected_referees = st.sidebar.multiselect(
    "Select Referees",
    options=all_referees,
    default=[]
)

# If no referees are selected, show all
if selected_referees:
    df_rs_filtered = regular_season_df[regular_season_df['referee'].isin(selected_referees)]
    df_po_filtered = playoffs_df[playoffs_df['referee'].isin(selected_referees)]
else:
    df_rs_filtered = regular_season_df.copy()
    df_po_filtered = playoffs_df.copy()

# --- KPI Cards ---
avg_games = df_rs_filtered["games_officiated"].mean()
avg_fouls = df_rs_filtered["fouls_per_game"].mean()
avg_foul_diff = df_rs_filtered["foul_diff"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Avg Games Officiated", f"{avg_games:.1f}")
col2.metric("Avg Fouls Per Game", f"{avg_fouls:.1f}")
col3.metric("Avg Foul Differential", f"{avg_foul_diff:.2f}")

# Section Regular Season vs Playoff Comparison
st.header("Regular Season vs Playoffs Comparison")

# Filter to only referees in both datasets
both = set(df_rs_filtered["referee"]) & set(df_po_filtered["referee"])
df_rs_both = df_rs_filtered[df_rs_filtered["referee"].isin(both)]
df_po_both = df_po_filtered[df_po_filtered["referee"].isin(both)]

# Get averages per season
# Split stats into two groups — rate stats and counting stats
rate_stats = ["win_pct_home", "win_pct_away", "foul_pct_road", "foul_pct_home", "foul_diff", "point_diff_home"]
counting_stats = ["fouls_per_game", "points_per_game"]

col1, col2 = st.columns(2)

# Section 1, Regular Season vs Playoffs
for stats, title, col in [
    (rate_stats, "Rate Stats (Season vs Playoffs)", col1),
    (counting_stats, "Counting Stats (Season vs Playoffs)", col2)
]:
    rs_avg = df_rs_both[stats].mean().reset_index()
    rs_avg.columns = ["stat", "value"]
    rs_avg["season"] = "Regular Season"

    po_avg = df_po_both[stats].mean().reset_index()
    po_avg.columns = ["stat", "value"]
    po_avg["season"] = "Playoffs"

    fig = px.bar(
        pd.concat([rs_avg, po_avg]),
        x="stat",
        y="value",
        color="season",
        barmode="group",
        color_discrete_map={
            "Regular Season": "#f5a623",
            "Playoffs": "#4a90d9"
        },
        title=title
    )
    fig.update_layout(
        plot_bgcolor="#1a1f2e",
        paper_bgcolor="#1a1f2e",
        font_color="#ffffff",
    )
    col.plotly_chart(fig, use_container_width=True)


# Section 2, Role Comparison
st.header("Role Comparison: Chief vs Crew")

role_stats = df_rs_filtered.groupby("role")[
    ["fouls_per_game", "foul_diff", "win_pct_home", "points_per_game"]
].mean().reset_index()

role_melted = pd.melt(role_stats, id_vars="role", var_name="stat", value_name="value")

col1, col2 = st.columns(2)

rate_role = ["win_pct_home", "foul_diff"]
counting_role = ["fouls_per_game", "points_per_game"]

for stats, title, col in [
    (rate_role, "Rate Stats by Role", col1),
    (counting_role, "Counting Stats by Role", col2)
]:
    fig = px.bar(
        role_melted[role_melted["stat"].isin(stats)],
        x="stat",
        y="value",
        color="role",
        barmode="group",
        color_discrete_map={
            "CHIEF": "#f5a623",
            "CREW": "#4a90d9"
        },
        title=title
    )
    fig.update_layout(
        plot_bgcolor="#1a1f2e",
        paper_bgcolor="#1a1f2e",
        font_color="#ffffff",
    )
    col.plotly_chart(fig, use_container_width=True)



# Section 3, Experience Trends
st.header("Referee Experience Trends")

exp_stats = ["fouls_per_game", "points_per_game", "win_pct_home"]
df_exp = regular_season_df.copy()

# Create experience buckets
df_exp["exp_bucket"] = pd.cut(
    df_exp["experience"],
    bins=[0, 5, 10, 15, 20, 25, 35],
    labels=["0-5", "6-10", "11-15", "16-20", "21-25", "26+"]
)

df_exp["games_bucket"] = pd.cut(
    df_exp["games_officiated"],
    bins=[0, 20, 35, 50, 65],
    labels=["0-20", "21-35", "36-50", "51-65"]
)

col1, col2 = st.columns(2)

for bucket_col, title, col in [
    ("exp_bucket", "Years Experience vs Avg Stats", col1),
    ("games_bucket", "Games Officiated vs Avg Stats", col2)
]:
    bucket_avg = df_exp.groupby(bucket_col, observed=True)[exp_stats].mean().reset_index()
    
    # Normalize each stat to % deviation from its overall mean
    for stat in exp_stats:
        overall_mean = df_exp[stat].mean()
        bucket_avg[stat] = ((bucket_avg[stat] - overall_mean) / overall_mean) * 100

    bucket_melted = pd.melt(
        bucket_avg,
        id_vars=bucket_col,
        value_vars=exp_stats,
        var_name="stat",
        value_name="pct_deviation"
    )

    fig = px.line(
        bucket_melted,
        x=bucket_col,
        y="pct_deviation",
        color="stat",
        markers=True,
        color_discrete_map={
            "fouls_per_game": "#f5a623",
            "points_per_game": "#4a90d9",
            "win_pct_home": "#ffffff"
        },
        title=title,
        labels={"pct_deviation": "% Above/Below Average", bucket_col: bucket_col.replace("_", " ").title()}
    )
    fig.add_hline(y=0, line_dash="dash", line_color="grey")
    fig.update_layout(
        plot_bgcolor="#1a1f2e",
        paper_bgcolor="#1a1f2e",
        font_color="#ffffff",
    )
    col.plotly_chart(fig, use_container_width=True)


# Section 4: Full Stats Table
st.header("Referee Stats Table")

table_season = st.radio(
    "Select Season",
    options=["Regular Season", "Playoffs"],
    horizontal=True
)

df_table = df_rs_filtered if table_season == "Regular Season" else df_po_filtered

st.dataframe(
    df_table.sort_values("games_officiated", ascending=False).reset_index(drop=True),
    use_container_width=True
)