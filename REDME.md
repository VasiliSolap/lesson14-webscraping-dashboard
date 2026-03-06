# Lesson 14 — Web Scraping and Dashboard Project (MLB Leaders)

This project scrapes MLB year-by-year leaderboard data, cleans and transforms it into structured CSV files, stores the data in a SQLite database, and presents the results in an interactive Streamlit dashboard.

## Tech Stack
- Python
- Selenium (web scraping)
- Pandas (data cleaning & transformation)
- SQLite (database)
- Streamlit (dashboard)

## Data Source
Baseball Almanac year-by-year MLB pages.

## Project Pipeline
1. **Scrape** MLB year pages and extract HTML tables → `data/cleaned/years.csv` and `data/cleaned/leaders_all.csv`
2. **Clean** the scraped tables to remove non-leaderboard rows → `data/cleaned/leaders_clean.csv`
3. **Split** into separate datasets:
   - `data/cleaned/leaders_hitting.csv`
   - `data/cleaned/leaders_pitching.csv`
4. **Import** CSV files into SQLite database `mlb_history.db`:
   - `years`
   - `leaders_hitting`
   - `leaders_pitching`
5. **Query** the database via CLI using JOINs
6. **Dashboard** built with Streamlit

## Project Files
- `src/scrape_mlb_history.py` — scraping program (Selenium → CSV)
- `src/clean_leaders.py` — data cleaning
- `src/split_leaders.py` — split hitting vs pitching CSV files
- `src/import_to_sqlite.py` — import CSV → SQLite
- `src/query_hitting.py` — CLI query with JOIN (hitting)
- `src/query_pitching.py` — CLI query with JOIN (pitching)
- `src/app.py` — Streamlit dashboard

## How to Run Locally (macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/scrape_mlb_history.py
python src/clean_leaders.py
python src/split_leaders.py
python src/import_to_sqlite.py

python src/query_hitting.py
python src/query_pitching.py

streamlit run src/app.py