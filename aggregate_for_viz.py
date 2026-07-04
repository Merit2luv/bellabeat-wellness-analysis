import duckdb

folder = "/Users/merit2luv/Downloads/Fitabase Data 3.12.16-4.11.16"

duckdb.sql(f"""
    CREATE OR REPLACE TABLE activity_sleep_merged AS
    SELECT * FROM read_csv_auto('{folder}/activity_sleep_combined.csv')
""")

# Summary 1: Activity type breakdown (for a stacked/pie chart)
duckdb.sql(f"""
    COPY (
        SELECT 'Very Active' AS activity_type, ROUND(AVG(VeryActiveMinutes), 1) AS avg_minutes
        FROM activity_sleep_merged
        UNION ALL
        SELECT 'Fairly Active', ROUND(AVG(FairlyActiveMinutes), 1) FROM activity_sleep_merged
        UNION ALL
        SELECT 'Lightly Active', ROUND(AVG(LightlyActiveMinutes), 1) FROM activity_sleep_merged
        UNION ALL
        SELECT 'Sedentary', ROUND(AVG(SedentaryMinutes), 1) FROM activity_sleep_merged
    ) TO '{folder}/summary_activity_breakdown.csv' (HEADER, DELIMITER ',')
""")

# Summary 2: Sedentary vs Sleep relationship (your headline finding)
duckdb.sql(f"""
    COPY (
        SELECT 
            CASE WHEN SedentaryMinutes > 700 THEN 'High Sedentary (700+ min)'
                 ELSE 'Lower Sedentary (<700 min)' END AS sedentary_group,
            ROUND(AVG(minutes_asleep), 1) AS avg_minutes_asleep,
            ROUND(AVG(minutes_asleep) / 60, 1) AS avg_hours_asleep,
            COUNT(*) AS num_days
        FROM activity_sleep_merged
        WHERE minutes_asleep IS NOT NULL
        GROUP BY sedentary_group
    ) TO '{folder}/summary_sedentary_vs_sleep.csv' (HEADER, DELIMITER ',')
""")

# Summary 3: Per-user activity and steps (for a ranked bar chart)
duckdb.sql(f"""
    COPY (
        SELECT Id,
               COUNT(*) AS days_tracked,
               ROUND(AVG(TotalSteps), 0) AS avg_steps,
               ROUND(AVG(VeryActiveMinutes), 1) AS avg_very_active_min,
               ROUND(AVG(Calories), 0) AS avg_calories
        FROM activity_sleep_merged
        GROUP BY Id
        ORDER BY avg_steps DESC
    ) TO '{folder}/summary_per_user.csv' (HEADER, DELIMITER ',')
""")

# Summary 4: Daily trend across the month (steps and sleep over time)
duckdb.sql(f"""
    COPY (
        SELECT CAST(ActivityDate AS DATE) AS activity_date,
               ROUND(AVG(TotalSteps), 0) AS avg_steps,
               ROUND(AVG(minutes_asleep), 1) AS avg_minutes_asleep,
               COUNT(*) AS num_users_tracked
        FROM activity_sleep_merged
        GROUP BY CAST(ActivityDate AS DATE)
        ORDER BY activity_date
    ) TO '{folder}/summary_daily_trend.csv' (HEADER, DELIMITER ',')
""")

# Summary 5: Overall scorecards
duckdb.sql(f"""
    COPY (
        SELECT 
            COUNT(DISTINCT Id) AS total_users,
            COUNT(*) AS total_days_tracked,
            ROUND(AVG(TotalSteps), 0) AS avg_daily_steps,
            ROUND(AVG(Calories), 0) AS avg_daily_calories,
            ROUND(AVG(minutes_asleep) / 60, 1) AS avg_hours_sleep
        FROM activity_sleep_merged
    ) TO '{folder}/summary_scorecards.csv' (HEADER, DELIMITER ',')
""")

print("Done — 5 summary CSVs created for dashboard building.")
