import requests
from waybackpy import WaybackMachineCDXServerAPI

def http_get(url, **kwargs):
    """GET request with error handling."""
    try:
        resp = requests.get(url, timeout=10, **kwargs)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"[HTTP] GET error for {url}: {e}")
        return None


def fetch_json(url):
    """Fetch JSON from a URL."""
    resp = http_get(url)
    if not resp:
        return None
    try:
        return resp.json()
    except Exception:
        print(f"[HTTP] Failed to decode JSON from {url}")
        print(f"[HTTP] Raw body: {resp.text[:300]}...")
        return None


def wayback_fetch_snapshots(url, limit=50):
    """
    Fetch Wayback Machine snapshots using waybackpy.
    Returns a list of snapshot objects.
    """
    try:
        cdx = WaybackMachineCDXServerAPI(url, user_agent="xfinder/1.0")
        snapshots = list(cdx.snapshots())  # correctly call method
        return snapshots[:limit]
    except Exception as e:
        print(f"[Wayback] Snapshot fetch error: {e}")
        return []
