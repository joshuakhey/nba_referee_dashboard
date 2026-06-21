<img width="1877" height="926" alt="Screenshot 2026-06-21 at 00 18 28" src="https://github.com/user-attachments/assets/07ae6425-de8f-4965-830b-1215926ec8a5" />
# NBA Referee Analytics Dashboard

A Reproducible Analytical Pipeline (RAP) for NBA referee statistics.

## Project Structure
```
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
```

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
<img width="1913" height="889" alt="Screenshot 2026-06-21 at 00 17 56" src="https://github.com/user-attachments/assets/88c309d1-6c54-402c-bede-95a981a91875" />
<img width="1876" height="933" alt="Screenshot 2026-06-21 at 00 18 14" src="https://github.com/user-attachments/assets/55709da5-2eda-45d9-8ed8-7e6e5763aa7b" />
<img width="1877" height="926" alt="Screenshot 2026-06-21 at 00 18 28" src="https://github.com/user-attachments/assets/933bbb2a-f5ab-47a6-9d7b-0a0ee3fdb88e" />
