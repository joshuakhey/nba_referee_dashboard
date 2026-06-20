"""
test_extract.py - Unit tests for the extract.py module.
"""

import pandas as pd
from bs4 import BeautifulSoup
import pytest

from extract import parse_tables


def test_parse_tables():
    soup = BeautifulSoup(open("tests/fixtures/sample_referee_page.html"), "html.parser")

    df_playoffs, df_regular_season = parse_tables(soup)
    
    # Check that the DataFrames are not None and contain expected data
    assert df_playoffs is not None
    assert df_regular_season is not None
    
    assert df_playoffs["REFEREE"].tolist() == ["Tony Brothers", "Zach Zarba", "Natalie Sago"]
    assert df_regular_season["REFEREE"].tolist() == ["Jacyn Goble", "Natalie Sago", "Tony Brothers"]
    


def test_parse_tables_no_tables():
    empty_soup = BeautifulSoup("<html><body><p>No tables here!</p></body></html>", "html.parser")
    with pytest.raises(ValueError):
        parse_tables(empty_soup)



def test_parse_tables_only_one_table():
    only_regular_season_soup = BeautifulSoup(open("tests/fixtures/sample_referee_page_only_regular_season.html"), "html.parser")
    df_no_playoffs, df_only_regular_season = parse_tables(only_regular_season_soup)
    
    assert df_no_playoffs is None
    assert df_only_regular_season is not None
    assert df_only_regular_season["REFEREE"].tolist() == ["Jacyn Goble", "Natalie Sago", "Tony Brothers"]
