import pandas as pd

# 1. Читаем уже очищенный файл
df = pd.read_csv("data/cleaned/leaders_clean.csv")

# 2. Список hitting статистик
hitting_stats = [
    "Base on Balls",
    "Batting Average",
    "Doubles",
    "Hits",
    "Home Runs",
    "On Base Percentage",
    "RBI",
    "Runs",
    "Slugging Average",
    "Stolen Bases",
    "Total Bases",
    "Triples",
]

# 3. Список pitching статистик
pitching_stats = [
    "Complete Games",
    "ERA",
    "Games",
    "Saves",
    "Shutouts",
    "Strikeouts",
    "Winning Percentage",
    "Wins",
]

# 4. Берём только hitting строки
hitting_df = df[df["statistic"].isin(hitting_stats)]

# 5. Берём только pitching строки
pitching_df = df[df["statistic"].isin(pitching_stats)]

# 6. Сохраняем в два новых CSV
hitting_df.to_csv("data/cleaned/leaders_hitting.csv", index=False)
pitching_df.to_csv("data/cleaned/leaders_pitching.csv", index=False)

# 7. Проверка
print("Hitting rows:", len(hitting_df))
print("Pitching rows:", len(pitching_df))
print("Saved -> data/cleaned/leaders_hitting.csv")
print("Saved -> data/cleaned/leaders_pitching.csv")