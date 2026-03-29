import pandas as pd

posts_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-22_2026-03-28_ErikNorris_posts2.xlsx"
audience_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-22_2026-03-28_ErikNorris_audience2.xlsx"

with open(r"d:\GitHub\global_agent\tmp\li_sheets_output.txt", "w", encoding="utf-8") as f:
    try:
        xl_posts = pd.ExcelFile(posts_file)
        f.write("Posts Sheets: " + str(xl_posts.sheet_names) + "\n")
    except Exception as e:
        f.write("Error posts: " + str(e) + "\n")
        
    try:
        xl_aud = pd.ExcelFile(audience_file)
        f.write("Audience Sheets: " + str(xl_aud.sheet_names) + "\n")
    except Exception as e:
        f.write("Error audience: " + str(e) + "\n")
