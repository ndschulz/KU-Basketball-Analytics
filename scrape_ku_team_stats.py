import requests
import pandas as pd
from bs4 import BeautifulSoup, Comment

# URL and output file
URL = "https://www.sports-reference.com/cbb/schools/kansas/"
OUTPUT_CSV = "ku_team_stats_template.csv"

# Step 1: Request and parse the page
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Search all HTML comments for the stats table
comments = soup.find_all(string=lambda text: isinstance(text, Comment))

found = False
df = None  # So it's defined before we use it

for i, comment in enumerate(comments):
    if "<table" in comment and "Season" in comment and "W" in comment and "FG%" in comment:
        print(f"\n--- Found candidate table in Comment {i} ---")
        table_soup = BeautifulSoup(comment, "html.parser")
        table = table_soup.find("table")
        try:
            df = pd.read_html(str(table))[0]
            print(f"✅ Loaded table with shape {df.shape}")
            found = True
            break
        except Exception as e:
            print(f"⚠️ Failed to parse table in Comment {i}: {e}")

if not found or df is None:
    print("❌ Still couldn't locate a valid KU season stats table.")
    exit()

# Step 3: Error handling if the table isn't found
if not table:
    print("❌ Could not find 'school_stats'. Dumping all comment blocks with <table> for debugging...\n")
    for i, comment in enumerate(comments):
        if "<table" in comment:
            print(f"\n--- Comment {i} ---")
            print(comment[:750])  # print first 750 characters of each comment
    exit()

# Step 4: Convert HTML table to DataFrame
df = pd.read_html(str(table))[0]

# Step 5: Clean multi-level headers (if any)
df.columns = df.columns.droplevel(0)
df.columns.name = None

# Step 6: Filter to Bill Self era (2003–present)
df = df[df["Season"] >= "2003-04"]

# Step 7: Build the cleaned output
result = pd.DataFrame()
result["season"] = df["Season"]
result["year"] = df["Season"].str[-2:].astype(int) + 2000
result["games_played"] = df["G"]
result["wins"] = df["W"]
result["losses"] = df["L"]
result["fg_pct"] = df["FG%"]
result["three_pt_pct"] = df["3P%"]
result["ft_pct"] = df["FT%"]
result["off_rtg"] = None
result["def_rtg"] = None
result["pace"] = None
result["opp_fg_pct"] = df["Opp FG%"]
result["opp_three_pt_pct"] = df["Opp 3P%"]

# Step 8: Save to CSV
result.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Scraped and saved {len(result)} KU team seasons to {OUTPUT_CSV}")
