"""
extract.py — Stage 1 of the RAP pipeline

Responsibilities:
  - Fetch the raw HTML from NBAstuffer
  - Parse playoff and regular season tables into DataFrames
  - Save raw CSVs to data/raw/

Two functions:
  fetch_page()   — downloads HTML, returns a BeautifulSoup object
  parse_tables() — receives that BeautifulSoup, returns two DataFrames

Keeping them separate means tests can feed parse_tables() a local
HTML fixture without ever touching the network.
"""

import os
from io import StringIO

import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def fetch_page(url: str) -> BeautifulSoup:
    """
    Fetch the HTML at `url` and return it as a BeautifulSoup object.
    """
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_tables(soup: BeautifulSoup) -> tuple[pd.DataFrame | None, pd.DataFrame]:
    """
    Parse the playoff and regular season tables from the BeautifulSoup object
    and return them as df_playoffs and df_regular_season.
    """
    tables = pd.read_html(StringIO(str(soup)))

    if len(tables) == 0:
        raise ValueError("No tables found in the HTML.")
    
    if len(tables) == 1:
        df_regular_season = tables[0]
        return None, df_regular_season

    df_playoffs = tables[0]
    df_regular_season = tables[1]

    return df_playoffs, df_regular_season


def save_raw(df: pd.DataFrame, filename: str) -> None:
    """
    Save the DataFrame to data/raw as a CSV.
    Raw data is saved unmodified, without any cleaning or processing.
    """
    file_src = os.path.dirname(__file__)
    save_path = os.path.join(file_src, "..", "data", "raw")
    os.makedirs(save_path, exist_ok=True)

    save_file = os.path.join(save_path, filename)
    df.to_csv(save_file, index=False)


if __name__ == "__main__":
    url = os.getenv("NBASTUFFER_URL")
    if not url:
        raise ValueError("NBASTUFFER_URL environment variable is not set.")
    soup = fetch_page(url)
    df_playoffs, df_regular_season = parse_tables(soup)

    if df_playoffs is not None:
        save_raw(df_playoffs, "playoffs.csv")
    save_raw(df_regular_season, "regular_season.csv")