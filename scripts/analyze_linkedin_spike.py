import pandas as pd
import datetime

def analyze_spike():
    posts_path = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-18_2026-03-31_ErikNorris_posts.xlsx"
    audience_path = r"D:\portfolio\portfolio_LinkedIn_working\Content_2026-03-25_2026-03-31_ErikNorris_audience.xlsx"
    
    print(f"ANALYSIS REPORT: LinkedIn Spike - March 2026")
    print("=" * 60)
    
    # --- POSTS ANALYSIS ---
    try:
        df_raw = pd.read_excel(posts_path, header=None)
        header_idx = -1
        for i, row in df_raw.iterrows():
            row_vals = [str(x).strip().lower() for x in row.values]
            if 'post title' in row_vals or 'impressions' in row_vals:
                header_idx = i
                break
        
        if header_idx == -1:
            print("Could not find post table header automatically.")
            # Fallback based on typical export
            header_idx = 4 
            
        df_posts = pd.read_excel(posts_path, skiprows=header_idx)
        df_posts = df_posts.fillna('')
        
        if 'Posted date' in df_posts.columns:
            df_posts['Posted date'] = pd.to_datetime(df_posts['Posted date'])
            
        # Spike Window: March 25 - March 31
        window_start = pd.to_datetime("2026-03-25")
        window_end = pd.to_datetime("2026-03-31")
        
        spike_posts = df_posts[(df_posts['Posted date'] >= window_start) & (df_posts['Posted date'] <= window_end)]
        spike_posts = spike_posts.sort_values(by='Impressions', ascending=False)
        
        print(f"\n[PHASE 1] Spike Window Post Performance:")
        for _, row in spike_posts.iterrows():
            date = row.get('Posted date').strftime('%Y-%m-%d')
            title = row.get('Post title', row.get('Post link', 'No Title'))[:80]
            print(f"- {date} | {title}")
            print(f"  Impressions: {row.get('Impressions', 0)} | Engagements: {row.get('Engagements', 0)} | Rate: {row.get('Engagement rate', '0%')}")
            
    except Exception as e:
        print(f"Post Analysis Error: {e}")

    # --- AUDIENCE ANALYSIS ---
    try:
        xls = pd.ExcelFile(audience_path)
        print(f"\n[PHASE 2] Audience Dynamics:")
        for sheet in xls.sheet_names:
            df_raw = pd.read_excel(audience_path, sheet_name=sheet, header=None)
            h_idx = 0
            for i, row in df_raw.iterrows():
                row_vals = [str(x).strip().lower() for x in row.values]
                if 'growth' in row_vals or 'followers' in row_vals or 'job titles' in row_vals or 'value' in row_vals:
                    h_idx = i
                    break
            df_aud = pd.read_excel(audience_path, sheet_name=sheet, skiprows=h_idx)
            print(f"\n--- Sheet: {sheet} ---")
            print(df_aud.head(8).to_string(index=False))
            
    except Exception as e:
        print(f"Audience Analysis Error: {e}")

if __name__ == '__main__':
    analyze_spike()
