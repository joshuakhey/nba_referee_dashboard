"""
transform.py — Stage 2 of the RAP pipeline

Responsibilities for both playoff and regular season tables:
  - Remove columns RANK, Unnamed: 13
  - Rename columns to lowercase and snake_case
    - REFEREE                                       -> referee
    - ROLE                                          -> role
    - GENDER                                        -> gender
    - EXPERIENCE (YEARS)                            -> experience
    - GAMES OFFICIATED                              -> games_officiated
    - HOME TEAM WIN%                                -> win_pct_home
    - HOME TEAM POINTS DIFFERENTIAL                 -> point_diff_home
    - TOTAL POINTS PER GAME                         -> points_per_game
    - CALLED FOULS PER GAME                         -> fouls_per_game
    - FOUL % AGAINST ROAD TEAMS                     -> foul_pct_road
    - FOUL % AGAINST HOME TEAMS                     -> foul_pct_home
    - FOUL DIFFERENTIAL (Ag.Rd Tm) - (Ag.Hm Tm)     -> foul_diff
  - Add a new column for away team win percentage (win_pct_away = 1 - win_pct_home)



Two functions:
  remove_columns()   — removes columns RANK, Unnamed: 13
  rename_columns()   — renames columns to lowercase and snake_case
  add_away_win_pct() — adds a new column for away team win percentage

"""

import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def remove_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove columns RANK and Unnamed: 13 from the DataFrame.
    """
    columns_to_remove = ["RANK", "Unnamed: 13"]
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns to lowercase and snake_case.
    """
    
    df = df.rename(columns=
                   {"REFEREE": "referee",
                    "ROLE": "role",
                    "GENDER": "gender",
                    "EXPERIENCE (YEARS)": "experience",
                    "GAMES OFFICIATED": "games_officiated",
                    "HOME TEAM WIN%": "win_pct_home",
                    "HOME TEAM POINTS DIFFERENTIAL": "point_diff_home",
                    "TOTAL POINTS PER GAME": "points_per_game",
                    "CALLED FOULS PER GAME": "fouls_per_game",
                    "FOUL% AGAINST ROAD TEAMS": "foul_pct_road",
                    "FOUL% AGAINST HOME TEAMS": "foul_pct_home",
                    "FOUL DIFFERENTIAL (Ag.Rd Tm) - (Ag. Hm Tm)": "foul_diff"})
    return df


def add_away_win_pct(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a new column for away team win percentage.
    """
    df["win_pct_away"] = 1 - df["win_pct_home"]
    return df


def save_processed(df: pd.DataFrame, filename: str) -> None:
    """
    Save the transformed DataFrame to data/processed as a CSV.
    """
    file_src = os.path.dirname(__file__)
    processed_dir = os.path.join(file_src, "..", "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    df.to_csv(os.path.join(processed_dir, filename), index=False)



if __name__ == "__main__":
    # Load the raw data
    raw_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    df_playoffs = pd.read_csv(os.path.join(raw_data_path, "playoffs.csv"))
    df_regular_season = pd.read_csv(os.path.join(raw_data_path, "regular_season.csv"))

    # Transform the playoff DataFrame
    try:
        df_playoffs = pd.read_csv(os.path.join(raw_data_path, "playoffs.csv"))
        df_playoffs = remove_columns(df_playoffs)
        df_playoffs = rename_columns(df_playoffs)
        df_playoffs = add_away_win_pct(df_playoffs)
        save_processed(df_playoffs, "playoffs_processed.csv")
    except FileNotFoundError:
        print("No playoffs data found, skipping.")


    # Transform the regular season DataFrame
    try:
        df_regular_season = pd.read_csv(os.path.join(raw_data_path, "regular_season.csv"))
        df_regular_season = remove_columns(df_regular_season)
        df_regular_season = rename_columns(df_regular_season)
        df_regular_season = add_away_win_pct(df_regular_season)
        save_processed(df_regular_season, "regular_season_processed.csv")
    except FileNotFoundError:
        print("No regular season data found, skipping.")
