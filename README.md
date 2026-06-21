# NBA Referee Analytics Dashboard

A Reproducible Analytical Pipeline (RAP) for NBA referee statistics.

## Project Structure
nba_referee_dashboard/
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── dashboard/
│   └── app.py
├── tests/
│   ├── fixtures/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── data/
│   ├── raw/
│   └── processed/
├── .env.example
└── requirements.txt


## Setup
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    ```


## Running the Pipeline
Terminal test command:
    ```
    python -m pytest -v
    ```

Terminal recreate commands:
    ```
    python src/extract.py
    python src/transform.py
    python src/load.py
    streamlit run dashboard/app.py
    ```

## Data Source:
    https://www.nbastuffer.com/2025-2026-nba-referee-stats/


## Dashboard:
