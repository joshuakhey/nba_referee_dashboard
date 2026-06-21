"""
load.py — Stage 3 of the RAP pipeline

Responsibilities:
  - Load the cleaned CSVs from data/processed/ into a SQLite database
  - Create tables for playoffs and regular season data

Two functions:
  load_to_sqlite()  — loads the cleaned CSVs into a SQLite database, 
                        creating tables for playoffs and regular season data
                        orchestrating the connection and table creation.
"""


import os

import sqlite3
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def load_to_sqlite(csv_path: str, db_path: str, table_name: str) -> None:
    """
    Load the cleaned CSV at `csv_path` into a SQLite database at `db_path`
    under the table name `table_name`.
    """
    df = pd.read_csv(csv_path)

    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)


if __name__ == "__main__":
    db_path = os.getenv("DB_PATH")
    if not db_path:
        raise ValueError("DB_PATH environment variable is not set.")

    file_src = os.path.dirname(__file__)
    file_path = os.path.join(file_src, "..", "data", "processed")

    load_to_sqlite(os.path.join(file_path, "playoffs_processed.csv"), db_path, "playoffs")
    load_to_sqlite(os.path.join(file_path, "regular_season_processed.csv"), db_path, "regular_season")
    
