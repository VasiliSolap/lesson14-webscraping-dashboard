import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_MENU_URL = "https://www.baseball-almanac.com/yearmenu.shtml"

OUT_DIR = "data/cleaned"
os.makedirs(OUT_DIR, exist_ok=True)

START_YEAR = 1990
END_YEAR = 2025

def normalize_url(href: str) -> str:
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return "https://www.baseball-almanac.com" + href 
    return "https://www.baseball-almanac.com/" + href
    
def main():
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_MENU_URL)
        time.sleep(1)
        links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        years = []

        for a in links:
            text = (a.text or "").strip()
            href = a.get_attribute("href") or ""

            if text.isdigit():
                year = int(text)
                if year >= START_YEAR and year <= END_YEAR:
                    if "/yearly/yr" in href and href.endswith("a.shtml"):
                        years.append({"year": year, "year_url": href})

        years_df = pd.DataFrame(years).drop_duplicates(subset=["year"]).sort_values("year")
        years_df.to_csv(f"{OUT_DIR}/years.csv", index=False)
        all_tables = []

        for _, row in years_df.iterrows():
            year = int(row["year"])
            url = normalize_url(row["year_url"])
            driver.get(url)
            time.sleep(1)
            tables = pd.read_html(driver.page_source)

            for t in tables:
                if t.shape[1] >= 4:
                    t = t.iloc[:, :4].copy()
                    t.columns = ["statistic", "player", "team", "value"]
                    t["year"] = year
                    all_tables.append(t)
        print(f"✅ scraped tables for year {year}")

        if all_tables:
            leaders_df = pd.concat(all_tables, ignore_index=True)
            leaders_df.to_csv(f"{OUT_DIR}/leaders_all.csv", index=False)
        else:
            pd.DataFrame(columns=["statistic","player","team","value","year"]).to_csv(
                f"{OUT_DIR}/leaders_all.csv", index=False
            )
        print("DONE -> data/cleaned/ (years.csv, leaders_all.csv)")
    
    finally:
        driver.quit()
if __name__ == "__main__":
    main()