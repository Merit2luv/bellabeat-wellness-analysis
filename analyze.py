import duckdb

folder = "/Users/merit2luv/Downloads/Fitabase Data 3.12.16-4.11.16"

# 1. Load daily activity
duckdb.sql(f"""
    CREATE OR REPLACE TABLE daily_activity AS
    SELECT * FROM read_csv_auto('{folder}/dailyActivity_merged.csv')
""")

print("=== DAILY ACTIVITY ===")
print(duckdb.sql("SELECT COUNT(*) AS total_rows, COUNT(DISTINCT Id) AS unique_users FROM daily_activity"))
print(duckdb.sql("SELECT MIN(ActivityDate) AS earliest, MAX(ActivityDate) AS latest FROM daily_activity"))

# 2. Aggregate minute-level sleep data up to daily totals per user
duckdb.sql(f"""
    CREATE OR REPLACE TABLE daily_sleep AS
    SELECT Id,
           CAST(date AS DATE) AS SleepDate,
           COUNT(*) FILTER (WHERE value = 1) AS minutes_asleep,
           COUNT(*) FILTER (WHERE value != 1) AS minutes_restless_or_awake,
           COUNT(*) AS total_minutes_in_bed
    FROM read_csv_auto('{folder}/minuteSleep_merged.csv')
    GROUP BY Id, CAST(date AS DATE)
""")

print("=== DAILY SLEEP (aggregated from minute data) ===")
print(duckdb.sql("SELECT COUNT(*) AS total_rows, COUNT(DISTINCT Id) AS unique_users FROM daily_sleep"))

# 3. Merge activity + sleep by user and date
duckdb.sql("""
    CREATE OR REPLACE TABLE activity_sleep_merged AS
    SELECT a.*,
           s.minutes_asleep,
           s.minutes_restless_or_awake,
           s.total_minutes_in_bed
    FROM daily_activity a
    LEFT JOIN daily_sleep s
      ON a.Id = s.Id AND CAST(a.ActivityDate AS DATE) = s.SleepDate
""")

print("=== MERGED ACTIVITY + SLEEP ===")
print(duckdb.sql("SELECT COUNT(*) AS total_rows FROM activity_sleep_merged"))
print(duckdb.sql("SELECT COUNT(*) AS rows_with_sleep_data FROM activity_sleep_merged WHERE minutes_asleep IS NOT NULL"))

# 4. Check weight log — likely sparse
duckdb.sql(f"""
    CREATE OR REPLACE TABLE weight_log AS
    SELECT * FROM read_csv_auto('{folder}/weightLogInfo_merged.csv')
""")
print("=== WEIGHT LOG ===")
print(duckdb.sql("SELECT COUNT(*) AS total_rows, COUNT(DISTINCT Id) AS unique_users FROM weight_log"))

# 5. Export merged daily file for further analysis
duckdb.sql(f"""
    COPY activity_sleep_merged TO '{folder}/activity_sleep_combined.csv' (HEADER, DELIMITER ',')
""")

print("Done — activity_sleep_combined.csv created.")

















