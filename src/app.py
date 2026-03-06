import sqlite3
import pandas as pd
import streamlit as st

st.title("MLB Leaders Dashboard (2000–2005)")

# 1) подключение к базе
conn = sqlite3.connect("mlb_history.db")

# 2) получаем список годов из таблицы years
years_df = pd.read_sql_query("SELECT year FROM years ORDER BY year;", conn)
year_list = years_df["year"].tolist()

# 3) элементы управления
year = st.selectbox("Select a year", year_list)
mode = st.radio("Select leaderboard type", ["Hitting", "Pitching"])

# 4) выбираем таблицу
if mode == "Hitting":
    table = "leaders_hitting"
else:
    table = "leaders_pitching"

# 5) читаем данные за выбранный год
query = f"""
SELECT year, statistic, player, team, value
FROM {table}
WHERE year = {int(year)}
ORDER BY statistic;
"""
df = pd.read_sql_query(query, conn)

st.subheader(f"{mode} leaders for {year}")
st.dataframe(df, use_container_width=True)

# ---- Visualization 1: counts by statistic (bar) ----
st.subheader("1) Number of rows per statistic")
counts = df["statistic"].value_counts().reset_index()
counts.columns = ["statistic", "count"]
st.bar_chart(counts.set_index("statistic"))

# ---- Visualization 2: Top teams by number of appearances (bar) ----
st.subheader("2) Teams with most leaderboard entries")
team_counts = df["team"].value_counts().head(10).reset_index()
team_counts.columns = ["team", "count"]
st.bar_chart(team_counts.set_index("team"))

# ---- Visualization 3: show top N by value (table) ----
st.subheader("3) Top N rows by value (numeric)")
top_n = st.slider("Top N", min_value=5, max_value=30, value=10)

df2 = df.copy()

# value иногда число, иногда может быть текст — пытаемся превратить в число
df2["value_num"] = pd.to_numeric(df2["value"], errors="coerce")
df2 = df2.dropna(subset=["value_num"]).sort_values("value_num", ascending=False).head(top_n)

st.table(df2[["statistic", "player", "team", "value"]])

conn.close()
