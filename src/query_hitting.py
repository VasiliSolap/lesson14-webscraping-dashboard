import sqlite3
import pandas as pd

conn = sqlite3.connect("mlb_history.db")

year = input("Enter year (e.g., 2000): ").strip()

query = """
SELECT h.year, h.statistic, h.player, h.team, h.value
FROM leaders_hitting h
JOIN years y
ON h.year = y.year
WHERE h.year = YEAR_HERE
ORDER BY h.statistic;
"""

query = query.replace("YEAR_HERE", year)

df = pd.read_sql_query(query, conn)
print(df)

conn.close()