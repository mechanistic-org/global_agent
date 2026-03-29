import pandas as pd
import sys

posts_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-22_2026-03-28_ErikNorris_posts2.xlsx"
audience_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-22_2026-03-28_ErikNorris_audience2.xlsx"

with open(r"d:\GitHub\global_agent\tmp\li_stats_output.txt", "w", encoding="utf-8") as f:
    try:
        posts_df = pd.read_excel(posts_file)
        f.write("=== POSTS DATA ===\n")
        f.write(posts_df.to_string() + "\n")
        f.write("\nColumns: " + str(posts_df.columns.tolist()) + "\n")
        if 'Impressions' in posts_df.columns:
            f.write("\nTotal Impressions: " + str(posts_df['Impressions'].sum()) + "\n")
    except Exception as e:
        f.write("Error reading posts file: " + str(e) + "\n")

    try:
        audience_df = pd.read_excel(audience_file)
        f.write("\n=== AUDIENCE DATA ===\n")
        f.write(audience_df.to_string() + "\n")
        f.write("\nColumns: " + str(audience_df.columns.tolist()) + "\n")
    except Exception as e:
        f.write("Error reading audience file: " + str(e) + "\n")
