import pandas as pd
import json

posts_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-22_2026-03-28_ErikNorris_posts2.xlsx"
audience_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-22_2026-03-28_ErikNorris_audience2.xlsx"

output = []
def add_section(title, content):
    output.append(f"\n======================\n{title}\n======================\n")
    output.append(content)

try:
    top_posts = pd.read_excel(posts_file, sheet_name='TOP POSTS')
    # Filter columns to most relevant ones to avoid overly wide output
    cols_to_keep = ['Post title', 'Post link', 'Post date', 'Impressions', 'Views', 'Clicks', 'Reactions', 'Comments', 'Reposts', 'Engagement rate']
    cols_present = [c for c in cols_to_keep if c in top_posts.columns]
    
    if 'Post title' in top_posts.columns and 'Impressions' in top_posts.columns:
        top_posts_sorted = top_posts.sort_values(by='Impressions', ascending=False)
        add_section("TOP POSTS (Sorted by Impressions)", top_posts_sorted[cols_present].to_string(index=False))
    else:
        add_section("TOP POSTS raw", top_posts.head(10).to_string(index=False))
        
    engagement = pd.read_excel(posts_file, sheet_name='ENGAGEMENT')
    add_section("ENGAGEMENT TRENDS", engagement.tail(7).to_string(index=False)) # Last 7 days

except Exception as e:
    add_section("POSTS ERROR", str(e))

try:
    demographics = pd.read_excel(audience_file, sheet_name='DEMOGRAPHICS')
    add_section("AUDIENCE DEMOGRAPHICS", demographics.head(20).to_string(index=False))
    
    followers = pd.read_excel(audience_file, sheet_name='FOLLOWERS')
    add_section("NEW FOLLOWERS", followers.tail(7).to_string(index=False))
except Exception as e:
    add_section("AUDIENCE ERROR", str(e))

with open(r"d:\GitHub\global_agent\tmp\li_stats_detail.txt", "w", encoding="utf-8") as f:
    f.writelines(output)
