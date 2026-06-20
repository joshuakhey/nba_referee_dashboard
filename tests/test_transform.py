"""
test_transform.py - Unit tests for the transform.py module.
"""

import pandas as pd

from transform import remove_columns, rename_columns, add_away_win_pct

def test_remove_columns():
    # Create a sample DataFrame with the columns to be removed
    df = pd.DataFrame({
        "RANK": [None],
        "Unnamed: 13": [None],
        "REFEREE": ["Ref A"],
        "ROLE": ["Role A"]
    })

    # Call the remove_columns function
    df_transformed = remove_columns(df)

    # Check that the output is what it should be
    assert df_transformed.equals(pd.DataFrame({
        "REFEREE": ["Ref A"],
        "ROLE": ["Role A"]
    }))

def test_rename_columns():
    # Create a sample DataFrame with the columns to be renamed
    df = pd.DataFrame({
        "REFEREE": ["Ref A"],
        "ROLE": ["Role A"],
        "GENDER": ["M"],
        "EXPERIENCE (YEARS)": [5],
        "GAMES OFFICIATED": [100],
        "HOME TEAM WIN%": [0.6],
        "HOME TEAM POINTS DIFFERENTIAL": [5],
        "TOTAL POINTS PER GAME": [200],
        "CALLED FOULS PER GAME": [15],
        "FOUL% AGAINST ROAD TEAMS": [0.5],
        "FOUL% AGAINST HOME TEAMS": [0.4],
        "FOUL DIFFERENTIAL (Ag.Rd Tm) - (Ag. Hm Tm)": [0.1]
    }) 

    # Call the rename_columns function
    df_transformed = rename_columns(df)

    # Check that the output is what it should be
    assert df_transformed.equals(pd.DataFrame({
        "referee": ["Ref A"],
        "role": ["Role A"],
        "gender": ["M"],
        "experience": [5],
        "games_officiated": [100],
        "win_pct_home": [0.6],
        "point_diff_home": [5],
        "points_per_game": [200],
        "fouls_per_game": [15],
        "foul_pct_road": [0.5],
        "foul_pct_home": [0.4],
        "foul_diff": [0.1]
    }))

def test_add_away_win_pct():
    # Create a sample DataFrame with the win_pct_home column
    df = pd.DataFrame({
        "win_pct_home": [0.6]
    })

    # Call the add_away_win_pct function
    df_transformed = add_away_win_pct(df)

    # Check that the output is what it should
    assert df_transformed.equals(pd.DataFrame({
        "win_pct_home": [0.6],
        "win_pct_away": [0.4]
    }))

