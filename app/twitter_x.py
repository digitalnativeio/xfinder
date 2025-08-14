from waybackpy import WaybackMachineCDXServerAPI
from bs4 import BeautifulSoup
import requests

def get_current_user_info_x(username):
    """Get latest archived Twitter profile info using Wayback Machine."""
    url = f"https://twitter.com/{username}"

    # Get newest snapshot from Wayback
    try:
        cdx_api = WaybackMachineCDXServerAPI(url, user_agent="xfinder-archive-client")
        snapshot = cdx_api.newest()
        snapshot_url = snapshot.archive_url
        print(f"[Wayback] Using snapshot: {snapshot_url}")
    except Exception as e:
        print(f"[Wayback] Error fetching snapshot: {e}")
        return None

    # Fetch archived HTML
    try:
        html = requests.get(snapshot_url, timeout=10).text
    except Exception as e:
        print(f"[Wayback] Error fetching HTML: {e}")
        return None

    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Display name
    display_name = None
    if soup.title:
        display_name = soup.title.get_text(strip=True)

    # Location
    location = None
    location_tag = soup.find("span", {"class": "ProfileHeaderCard-locationText"})
    if location_tag:
        location = location_tag.get_text(strip=True)

    return {
        "user_id": None,
        "handle": username,
        "display_name": display_name,
        "location": location,
        "platform": "x",
        "username": username,
    }
