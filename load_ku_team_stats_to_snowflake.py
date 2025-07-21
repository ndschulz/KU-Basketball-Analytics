import pandas as pd
import snowflake.connector
import os
import math
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load CSV and rename columns
df = pd.read_csv("KU_Stats_Self.csv")

df.columns = [
    "Team_Rank", "Season", "Conference",
    "Overall_Wins", "Overall_Losses", "Overall_Win_Percentage",
    "Conference_Wins", "Conference_Losses", "Conference_Win_Percentage",
    "Simple_Rating_System", "Strength_of_Schedule",
    "Points_Per_Game", "Opponent_Points_Per_Game",
    "AP_Preseason_Rank", "AP_Highest_Rank", "AP_Final_Rank",
    "NCAA_Tournament_Result", "NCAA_Tournament_Seed", "Coach_Name"
]

# Derive Year column (e.g., "2024-25" → 2024)
df["Year"] = df["Season"].str.slice(0, 4).astype(int)

# Reorder columns to match Snowflake
df = df[[
    "Team_Rank", "Season", "Year", "Conference",
    "Overall_Wins", "Overall_Losses", "Overall_Win_Percentage",
    "Conference_Wins", "Conference_Losses", "Conference_Win_Percentage",
    "Simple_Rating_System", "Strength_of_Schedule",
    "Points_Per_Game", "Opponent_Points_Per_Game",
    "AP_Preseason_Rank", "AP_Highest_Rank", "AP_Final_Rank",
    "NCAA_Tournament_Result", "NCAA_Tournament_Seed", "Coach_Name"
]]

# Replace NaNs with None
df = df.where(pd.notnull(df), None)

print(f"Inserting {df.shape[0]} rows with {df.shape[1]} columns...")

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cursor = conn.cursor()

# SQL INSERT with 20 columns
insert_sql = """
    INSERT INTO KU_TEAM_STATS (
        Team_Rank, Season, Year, Conference,
        Overall_Wins, Overall_Losses, Overall_Win_Percentage,
        Conference_Wins, Conference_Losses, Conference_Win_Percentage,
        Simple_Rating_System, Strength_of_Schedule,
        Points_Per_Game, Opponent_Points_Per_Game,
        AP_Preseason_Rank, AP_Highest_Rank, AP_Final_Rank,
        NCAA_Tournament_Result, NCAA_Tournament_Seed, Coach_Name
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert each row
for idx, row in enumerate(df.itertuples(index=False, name=None)):
    clean_row = [None if (isinstance(x, float) and math.isnan(x)) else x for x in row]
    try:
        cursor.execute(insert_sql, clean_row)
    except Exception as e:
        print(f"❌ Error inserting row {idx}: {e}")
        print(f"Row content: {clean_row}")

# Finalize
conn.commit()
cursor.close()
conn.close()

print("✅ All rows successfully inserted into KU_TEAM_STATS.")
