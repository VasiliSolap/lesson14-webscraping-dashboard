import os
import sqlite3
import pandas as pd
import streamlit as st

st.title("MLB Leaders Dashboard (1990–2025)")

DB_PATH = "mlb_history.db"

def build_db_from_csv(db_path: str) -> None:
    """Create SQLite DB from committed CSV files."""
    years_df = pd.read_csv("data/cleaned/years.csv")
    hitting_df = pd.read_csv("data/cleaned/leaders_hitting.csv")
    pitching_df = pd.read_csv("data/cleaned/leaders_pitching.csv")

    conn = sqlite3.connect(db_path)
    years_df.to_sql("years", conn, if_exists="replace", index=False)
    hitting_df.to_sql("leaders_hitting", conn, if_exists="replace", index=False)
    pitching_df.to_sql("leaders_pitching", conn, if_exists="replace", index=False)
    conn.close()

def ensure_db(db_path: str) -> None:
    """
    Streamlit Cloud starts with a fresh environment.
    If DB file or tables are missing, rebuild the DB from CSV.
    """
    rebuild = False

    if not os.path.exists(db_path):
        rebuild = True
    else:
        try:
            conn = sqlite3.connect(db_path)
            # Check that required tables exist
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='years';")
            has_years = cur.fetchone() is not None
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leaders_hitting';")
            has_h = cur.fetchone() is not None
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leaders_pitching';")
            has_p = cur.fetchone() is not None
            conn.close()
            if not (has_years and has_h and has_p):
                rebuild = True
        except Exception:
            rebuild = True

    if rebuild:
        build_db_from_csv(db_path)

# ✅ Make sure DB exists before querying
ensure_db(DB_PATH)

# Connect and continue with your existing queries/UI
conn = sqlite3.connect(DB_PATH)

years_df = pd.read_sql_query("SELECT year FROM years ORDER BY year;", conn)
year_list = years_df["year"].tolist()

year = st.selectbox("Select a year", year_list)
mode = st.radio("Select leaderboard type", ["Hitting", "Pitching"])

table = "leaders_hitting" if mode == "Hitting" else "leaders_pitching"

query = f"""
SELECT year, statistic, player, team, value
FROM {table}
WHERE year = {int(year)}
ORDER BY statistic;
"""
df = pd.read_sql_query(query, conn)

st.subheader(f"{mode} leaders for {year}")
st.dataframe(df, use_container_width=True)

st.subheader("1) Number of rows per statistic")
counts = df["statistic"].value_counts().reset_index()
counts.columns = ["statistic", "count"]
st.bar_chart(counts.set_index("statistic"))

st.subheader("2) Teams with most leaderboard entries")
team_counts = df["team"].value_counts().head(10).reset_index()
team_counts.columns = ["team", "count"]
st.bar_chart(team_counts.set_index("team"))

st.subheader("3) Top N rows by value (numeric)")
top_n = st.slider("Top N", min_value=5, max_value=30, value=10)

df2 = df.copy()
df2["value_num"] = pd.to_numeric(df2["value"], errors="coerce")
df2 = df2.dropna(subset=["value_num"]).sort_values("value_num", ascending=False).head(top_n)
st.table(df2[["statistic", "player", "team", "value"]])

conn.close()