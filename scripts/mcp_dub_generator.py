import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Ensure we load the global .env securely
ENOS_ROOT = os.environ.get("ENOS_ROOT", r"D:\GitHub\global_agent")
load_dotenv(os.path.join(ENOS_ROOT, ".env"))

DUB_API_KEY = os.environ.get("DUB_API_KEY")

mcp = FastMCP("dub-link-generator")

@mcp.tool()
def generate_short_link(destination_url: str, slug: str = None) -> str:
    """
    Creates a branded short link (link.eriknorris.com) using Dub.co.
    
    Args:
        destination_url: The long target URL to shorten (e.g. GitHub Ticket, raw LinkedIn post).
        slug: Optional custom vanity alias (e.g., 'fmea', 'arc1'). If omitted, a random string is used.
    
    Returns:
        The generated short link as a string (e.g., 'https://link.eriknorris.com/fmea') or an ERROR string.
    """
    if not DUB_API_KEY:
        return "ERROR: DUB_API_KEY environment variable not set in .env."

    url = "https://api.dub.co/links"
    headers = {
        "Authorization": f"Bearer {DUB_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "domain": "link.eriknorris.com",
        "url": destination_url
    }
    
    if slug:
        payload["key"] = slug
        
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("shortLink", f"ERROR: Unexpected response format: {data}")
    except requests.exceptions.HTTPError:
        # Dub often returns detailed JSON errors (e.g., "key already exists")
        return f"HTTP Error creating link. Dub.co returned: {response.text}"
    except Exception as e:
        return f"CRITICAL: Dub.co API execution violently failed: {str(e)}"

if __name__ == "__main__":
    # Standard FastMCP lifecycle hook
    mcp.run()
