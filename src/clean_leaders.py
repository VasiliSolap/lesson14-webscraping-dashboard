import pandas as pd

df = pd.read_csv("data/cleaned/leaders_all.csv")

# 1) delete row-title
df = df[df["statistic"] != "Statistic"]

# 2) statistic
good_stats = [
    # hitting
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
    # pitching
    "Complete Games",
    "ERA",
    "Games",
    "Saves",
    "Shutouts",
    "Strikeouts",
    "Winning Percentage",
    "Wins",
]

df = df[df["statistic"].isin(good_stats)]

# 3) delete duplicates
df = df.drop_duplicates()

# 4) save clean file
df.to_csv("data/cleaned/leaders_clean.csv", index=False)

print("Rows after cleaning:", len(df))
print(df.head(15))
print("Saved -> data/cleaned/leaders_clean.csv")