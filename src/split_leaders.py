import pandas as pd

# 1) read the cleaned leaderboard file
df = pd.read_csv("data/cleaned/leaders_clean.csv")

# 2) hitting statistics (whitelist)
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

# 3) pitching statistics (whitelist)
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

# 4) keep only hitting rows
hitting_df = df[df["statistic"].isin(hitting_stats)]

# 5) keep only pitching rows
pitching_df = df[df["statistic"].isin(pitching_stats)]

# 6) save to two separate CSV files
hitting_df.to_csv("data/cleaned/leaders_hitting.csv", index=False)
pitching_df.to_csv("data/cleaned/leaders_pitching.csv", index=False)

# 7) quick check
print("Hitting rows:", len(hitting_df))
print("Pitching rows:", len(pitching_df))
print("Saved -> data/cleaned/leaders_hitting.csv")
print("Saved -> data/cleaned/leaders_pitching.csv")