# Bellabeat Wellness Analysis: Smart Device Usage Trends

## Business Task
Bellabeat is a high-tech manufacturer of health-focused smart products for women, offering devices including Leaf, Time, and Spring, alongside a companion wellness app. Bellabeat's cofounder believes analyzing existing smart device fitness data could reveal growth opportunities for the company.

**Goal of this analysis:** Identify trends in smart device usage (using non-Bellabeat FitBit data as a proxy), determine how these trends could apply to Bellabeat customers, and translate these insights into marketing strategy recommendations for one specific Bellabeat product.

**Product selected for recommendations: Time** — Bellabeat's wellness watch, which tracks activity, sleep, and stress, aligning closely with the data available in this analysis.

## Data Source
- FitBit Fitness Tracker Data (Möbius, CC0: Public Domain, via Kaggle)
- 35 unique users, daily activity data spanning March 12 – April 12, 2016
- 457 total daily activity records
- Minute-level sleep data available for 23 of the 35 users (199 of 457 days have matching sleep data)
- Weight log data available for only 11 of 35 users (33 entries total) — too sparse for reliable analysis

**Data limitations (explicitly noted, per case study guidance):** This is a small, self-selected sample (30-35 Amazon Mechanical Turk participants) collected in 2016 using third-party FitBit devices, not actual Bellabeat users or products. Findings should be treated as directional indicators of general smart-device-user behavior, not definitive or statistically representative conclusions. Sleep and weight data in particular are incomplete, limiting the confidence of any findings tied to those fields.

## Tools Used
- **Python + DuckDB** — data cleaning, aggregation (minute-level sleep data rolled up to daily totals), and SQL-based analysis
- **Tableau Public** — interactive dashboard
- **GitHub** — version control and portfolio hosting

## Data Cleaning & Transformation
Using DuckDB:
- Loaded and inspected `dailyActivity_merged.csv` as the primary activity dataset
- Aggregated `minuteSleep_merged.csv` (minute-by-minute sleep state) into daily sleep totals per user (minutes asleep, minutes restless/awake, total time in bed)
- Left-joined daily activity and daily sleep by user ID and date, preserving all activity records even where sleep data was missing
- Reviewed `weightLogInfo_merged.csv` and excluded it from deeper analysis due to sparse coverage (11 users, 33 entries)

Scripts included in this repo:
- [`analyze.py`](./analyze.py) — loads, cleans, and merges activity and sleep data
- [`deep_analysis.py`](./deep_analysis.py) — activity breakdowns, sleep summaries, and the sedentary/sleep relationship analysis
- [`aggregate_for_viz.py`](./aggregate_for_viz.py) — produces summary tables used to build the dashboard

## Key Findings

**1. Users are overwhelmingly sedentary**
Of roughly 1,195 tracked minutes per day, 995 minutes (83%) are sedentary. Only 16.6 minutes average "very active" time and 13.1 minutes "fairly active" time — light activity (170 minutes) makes up most of the non-sedentary time.

**2. Average steps fall below common benchmarks**
Users average 6,547 steps per day, below the commonly cited 10,000-step target, reinforcing the high-sedentary pattern.

**3. Sleep duration is below recommended levels**
Average sleep across users with available data is 6.6 hours per night, below the general 7–9 hour recommendation for adults, with an average of 36 minutes spent restless or awake while in bed.

**4. Headline finding — sedentary time is strongly associated with reduced sleep**
On days with high sedentary time (700+ minutes), users averaged 5.7 hours of sleep, compared to 7.8 hours on lower-sedentary days — a difference of over 2 hours. This is a correlational finding, not a causal one; the direction of the relationship (whether inactivity reduces sleep, poor sleep leads to inactivity, or both are driven by another factor) cannot be determined from this dataset alone.

**5. Wide variation between individual users**
Daily step averages among the most active tracked users range from roughly 6,000 to over 17,000 steps, indicating that a single, generalized wellness message is unlikely to resonate equally with all users.

## Recommendations (for Bellabeat's Time watch)

1. **Surface the sedentary–sleep connection directly in the app.** Since high sedentary time is associated with meaningfully shorter sleep, Time could notify users when a sedentary day is trending toward this pattern, framed around better rest rather than generic activity goals — a more personally motivating angle for a wellness-focused product.

2. **De-emphasize step-count-only messaging in marketing.** Given the wide variation in user activity levels, marketing that centers exclusively on hitting a step target risks alienating less active users. Messaging centered on sleep quality and gradual reduction of sedentary time may resonate more broadly.

3. **Address the data gap as a product opportunity.** Since built-in sleep tracking was inconsistently used even among engaged FitBit users, Bellabeat could invest in making Time's sleep-tracking experience simpler and more consistent to use, ensuring more complete data for users and, at scale, more reliable insights for Bellabeat's own product development.

## Dashboard
An interactive Tableau dashboard visualizing these findings is available here: **[Bellabeat Wellness Dashboard](https://public.tableau.com/app/profile/matthew.ofikwu8795/viz/BellabeatSmartDeviceInsightsHowSedentaryTimeImpactsSleep/Dashboard1)**

## Author 
Analysis conducted by Ofikwu Matthew as a self-directed portfolio project, extending the Google Data Analytics Certificate capstone case study (Bellabeat) using a local Python/DuckDB environment in place of cloud-based tools.
