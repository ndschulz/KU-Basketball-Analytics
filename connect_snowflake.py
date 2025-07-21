import snowflake.connector
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Connect using env variables
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

cursor = conn.cursor()
cursor.execute("SELECT CURRENT_DATE;")
result = cursor.fetchone()
print("Connected to Snowflake! Today's date is:", result[0])
