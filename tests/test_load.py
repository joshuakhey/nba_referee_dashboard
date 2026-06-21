"""
test_load.py - Unit tests for the load.py module.
"""
import os
import sqlite3
import tempfile

import pandas as pd


from load import load_to_sqlite


def test_load_to_sqlite():
    test_df = pd.read_csv("tests/fixtures/sample_processed.csv")

    temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_db.close()

    try:
        load_to_sqlite("tests/fixtures/sample_processed.csv", temp_db.name, "test_table")

        with sqlite3.connect(temp_db.name) as conn:
            loaded_df = pd.read_sql_query("SELECT * FROM test_table", conn)

            # Assert that the loaded DataFrame matches the original DataFrame
            assert loaded_df is not None, "The loaded DataFrame is None."
            assert test_df.shape[0] == loaded_df.shape[0], "The number of rows in the loaded DataFrame does not match the original DataFrame."
            assert test_df["games_officiated"].sum() == loaded_df["games_officiated"].sum(), "The sum of 'games_officiated' in the loaded DataFrame does not match the original DataFrame."
            pass

    finally:
        os.unlink(temp_db.name)
