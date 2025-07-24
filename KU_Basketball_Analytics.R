# Load required libraries
library(DBI)
library(odbc)
library(dotenv)
library(dplyr)
library(ggplot2)

# Load environment variables from .env
dotenv::load_dot_env(".env")

# Build connection variables
user      <- Sys.getenv("SNOWFLAKE_USER")
password  <- Sys.getenv("SNOWFLAKE_PASSWORD")
account   <- Sys.getenv("SNOWFLAKE_ACCOUNT")
warehouse <- Sys.getenv("SNOWFLAKE_WAREHOUSE")
database  <- Sys.getenv("SNOWFLAKE_DATABASE")
schema    <- Sys.getenv("SNOWFLAKE_SCHEMA")
server    <- paste0(account, ".snowflakecomputing.com")

# Connect to Snowflake
con <- dbConnect(
  odbc::odbc(),
  Driver     = "SnowflakeDSIIDriver",
  Server     = server,
  UID        = user,
  PWD        = password,
  Warehouse  = warehouse,
  Database   = database,
  Schema     = schema
)

# Pull data
ku_df <- dbGetQuery(con, "SELECT * FROM KU_TEAM_STATS ORDER BY Year")

# Disconnect after query (optional here since connection stays open during session)
# dbDisconnect(con)

# Confirm structure
str(ku_df)
summary(ku_df)

# Plot: Win Percentage Over Time
ggplot(ku_df, aes(x = YEAR, y = OVERALL_WIN_PERCENTAGE)) +
  geom_line(color = "blue", size = 1) +
  geom_point(size = 2) +
  labs(
    title = "KU Win Percentage Over Time",
    x = "Season Start Year",
    y = "Overall Win Percentage"
  ) +
  theme_minimal()

# Plot: NCAA Tournament Seed by Year
ggplot(ku_df, aes(x = YEAR, y = NCAA_TOURNAMENT_SEED)) +
  geom_line(color = "darkred", size = 1) +
  geom_point(size = 2) +
  scale_y_reverse(breaks = seq(1, 16, 1)) +
  labs(
    title = "KU NCAA Tournament Seed Over Time",
    x = "Season Start Year",
    y = "Seed (lower is better)"
  ) +
  theme_minimal()

#AP Rankings (PReseason, High, Final)
ggplot(ku_df, aes(x = YEAR)) +
  geom_line(aes(y = AP_PRESEASON_RANK), color = "darkblue") +
  geom_line(aes(y = AP_FINAL_RANK), color = "red") +
  scale_y_reverse(breaks = seq(1, 25, 1)) +
  labs(
    title = "AP Rankings (Preseason vs Final)",
    y = "Rank (Lower is Better)",
    x = "Season Start Year"
  ) +
  theme_minimal()


# Simple Rating and Strength of Schedule
ggplot(ku_df, aes(x = YEAR)) +
  geom_line(aes(y = SIMPLE_RATING_SYSTEM), color = "darkgreen", size = 1) +
  geom_line(aes(y = STRENGTH_OF_SCHEDULE), color = "gray40", size = 1, linetype = "dashed") +
  labs(
    title = "KU SRS and SOS Over Time",
    x = "Season Start Year",
    y = "Rating"
  ) +
  theme_minimal()
