# KU Basketball Analytics

This project explores how Bill Self's Kansas basketball teams have evolved over time. It analyzes trends in performance, strength of schedule, AP rankings, and NCAA tournament results.

## Project Goals
- Analyze win/loss performance over time
- Track trends in metrics like SRS, SOS, and scoring
- Visualize AP rankings and NCAA tournament outcomes
- Cluster seasons by statistical profile
- (Optional) Explore player development and transitions to the NBA

## Tech Stack
- Python for data ingestion and ETL
- Snowflake as cloud data warehouse
- R for statistical analysis and visualization
- Power BI for dashboards
- Git and GitHub for version control

## Project Structure
Kansas Basketball/
├── KU_Stats_Self.csv # Cleaned input data
├── load_ku_team_stats_to_snowflake.py # ETL script
├── .env # Snowflake credentials (not tracked)
├── notebooks/ # R analysis and EDA
├── README.md
├── requirements.txt
└── .gitignore


## Project Status
- Cleaned and structured team stats
- Successfully loaded to Snowflake
- R visualizations in progress
- Power BI dashboard to follow
