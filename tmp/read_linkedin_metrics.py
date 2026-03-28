import pandas as pd
import sys
import os

def generate_report():
    out_path = r"D:\GitHub\global_agent\tmp\linkedin_summary.md"
    posts_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-21_2026-03-27_ErikNorris_posts.xlsx"
    audience_file = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-21_2026-03-27_ErikNorris_audience.xlsx"
    
    lines = ["# LinkedIn Metrics Summary"]
    
    # 1. Posts Summary
    try:
        # According to standard LinkedIn exports, the data is on the second sheet or first.
        try:
            df_posts = pd.read_excel(posts_file, sheet_name=1)
        except:
            df_posts = pd.read_excel(posts_file, sheet_name=0)
            
        lines.append("## Posts Data (Mar 21 - Mar 27)")
        lines.append(f"- Total Rows/Posts Found: {len(df_posts)}")
        
        metrics = ['Impressions', 'Clicks', 'Likes', 'Comments', 'Shares', 'Engagements', 'Engagement rate']
        for m in metrics:
            if m in df_posts.columns:
                if m == 'Engagement rate':
                    avg = df_posts[m].mean()
                    lines.append(f"- Average {m}: {avg:.4f} ({avg*100:.2f}%)")
                else:
                    total = df_posts[m].sum()
                    lines.append(f"- Total {m}: {total}")
                    
        # Let's also grab top 3 posts by impressions
        if 'Impressions' in df_posts.columns and 'Post title' in df_posts.columns:
            top = df_posts.nlargest(3, 'Impressions')
            lines.append("\n### Top 3 Posts by Impressions")
            for _, row in top.iterrows():
                title = str(row['Post title'])[:60].replace("\n", " ") + "..."
                imps = row['Impressions']
                lines.append(f"- {imps} impressions: {title}")
                
    except Exception as e:
        lines.append(f"Error reading posts: {str(e)}")

    # 2. Audience Summary
    try:
        xl_aud = pd.ExcelFile(audience_file)
        lines.append("\n## Audience Data")
        for sheet in xl_aud.sheet_names:
            df_aud = xl_aud.parse(sheet)
            lines.append(f"\n### {sheet} Demographics")
            # Try to show top 5 rows
            top5 = df_aud.head(5)
            for _, row in top5.iterrows():
                # Format each row nicely
                row_str = " | ".join([f"{col}: {val}" for col, val in zip(df_aud.columns, row.values) if pd.notna(val)])
                lines.append(f"- {row_str}")
                
    except Exception as e:
        lines.append(f"Error reading audience: {str(e)}")
        
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
if __name__ == '__main__':
    generate_report()
