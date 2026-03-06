import sqlite3
import pandas as pd

conn = sqlite3.connect("mlb_history.db")

year = input("Enter year (e.g., 2000): ").strip()

query = """
SELECT p.year, p.statistic, p.player, p.team, p.value
FROM leaders_pitching p
JOIN years y
ON p.year = y.year
WHERE p.year = YEAR_HERE
ORDER BY p.statistic;
"""

query = query.replace("YEAR_HERE", year)

df = pd.read_sql_query(query, conn)
print(df)

conn.close()