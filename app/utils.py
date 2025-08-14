import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from waybackpy import WaybackMachineCDXServerAPI


def http_get(url, timeout=10, retries=3, backoff_factor=0.5, **kwargs):
    """GET request with retries and error handling."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    try:
        resp = session.get(url, timeout=timeout, **kwargs)
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
