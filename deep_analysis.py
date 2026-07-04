import duckdb

folder = "/Users/merit2luv/Downloads/Fitabase Data 3.12.16-4.11.16"

duckdb.sql(f"""
    CREATE OR REPLACE TABLE activity_sleep_merged AS
    SELECT * FROM read_csv_auto('{folder}/activity_sleep_combined.csv')
""")

print("=== ACTIVITY LEVEL BREAKDOWN (avg minutes per day) ===")
print(duckdb.sql("""
    SELECT ROUND(AVG(VeryActiveMinutes), 1) AS avg_very_active,
           ROUND(AVG(FairlyActiveMinutes), 1) AS avg_fairly_active,
           ROUND(AVG(LightlyActiveMinutes), 1) AS avg_lightly_active,
           ROUND(AVG(SedentaryMinutes), 1) AS avg_sedentary
    FROM activity_sleep_merged
"""))

print("=== STEPS AND CALORIES SUMMARY ===")
print(duckdb.sql("""
    SELECT ROUND(AVG(TotalSteps), 0) AS avg_daily_steps,
           ROUND(AVG(Calories), 0) AS avg_daily_calories,
           ROUND(AVG(TotalDistance), 2) AS avg_daily_distance_km
    FROM activity_sleep_merged
"""))

print("=== SLEEP SUMMARY (where sleep data exists) ===")
print(duckdb.sql("""
    SELECT ROUND(AVG(minutes_asleep), 1) AS avg_minutes_asleep,
           ROUND(AVG(minutes_asleep) / 60, 1) AS avg_hours_asleep,
           ROUND(AVG(total_minutes_in_bed), 1) AS avg_minutes_in_bed,
           ROUND(AVG(total_minutes_in_bed - minutes_asleep), 1) AS avg_minutes_restless
    FROM activity_sleep_merged
    WHERE minutes_asleep IS NOT NULL
"""))

print("=== SEDENTARY TIME vs SLEEP (relationship check) ===")
print(duckdb.sql("""
    SELECT 
        CASE WHEN SedentaryMinutes > 700 THEN 'High Sedentary (700+ min)'
             ELSE 'Lower Sedentary (<700 min)' END AS sedentary_group,
        ROUND(AVG(minutes_asleep), 1) AS avg_minutes_asleep,
        COUNT(*) AS num_days
    FROM activity_sleep_merged
    WHERE minutes_asleep IS NOT NULL
    GROUP BY sedentary_group
"""))

print("=== PER-USER AVERAGE ACTIVITY (sample of individual variation) ===")
print(duckdb.sql("""
    SELECT Id, 
           COUNT(*) AS days_tracked,
           ROUND(AVG(TotalSteps), 0) AS avg_steps,
           ROUND(AVG(VeryActiveMinutes), 1) AS avg_very_active_min
    FROM activity_sleep_merged
    GROUP BY Id
    ORDER BY avg_steps DESC
    LIMIT 10
"""))
