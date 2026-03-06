import sqlite3
import pandas as pd

# 1. Подключаемся к базе
conn = sqlite3.connect("mlb_history.db")

# 2. Читаем CSV файлы
years_df = pd.read_csv("data/cleaned/years.csv")
hitting_df = pd.read_csv("data/cleaned/leaders_hitting.csv")
pitching_df = pd.read_csv("data/cleaned/leaders_pitching.csv")

# 3. Записываем их в SQLite как отдельные таблицы
years_df.to_sql("years", conn, if_exists="replace", index=False)
hitting_df.to_sql("leaders_hitting", conn, if_exists="replace", index=False)
pitching_df.to_sql("leaders_pitching", conn, if_exists="replace", index=False)

# 4. Проверка
print("Imported tables:")
print("- years:", len(years_df), "rows")
print("- leaders_hitting:", len(hitting_df), "rows")
print("- leaders_pitching:", len(pitching_df), "rows")

# 5. Закрываем соединение
conn.close()