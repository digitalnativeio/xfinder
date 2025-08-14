from waybackpy import WaybackMachineCDXServerAPI
from bs4 import BeautifulSoup
import re
import importlib.machinery

if not hasattr(importlib.machinery.FileFinder, "find_module"):
    def _find_module(self, fullname):
        spec = self.find_spec(fullname)
        return spec.loader if spec else None
    importlib.machinery.FileFinder.find_module = _find_module

import snscrape.modules.twitter as sntwitter

from .utils import http_get

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
    resp = http_get(snapshot_url, timeout=30)
    if not resp:
        print(f"[Wayback] Error fetching HTML: unable to retrieve {snapshot_url}")
        return None
    html = resp.text

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


def get_user_history_x(username):
    """Return first tweet and its first reply for a user using snscrape.

    This uses public web scraping via snscrape, so it does not require API
    credentials. It returns a list of history entries each containing a
    timestamp and URL. The first item is the earliest tweet by the user and
    the second (if available) is the earliest reply to that tweet. Mentioned
    handles in the reply are extracted to help infer prior usernames.
    """

    # Fetch all tweets from the user and locate the oldest one
    tweet_scraper = sntwitter.TwitterSearchScraper(f"from:{username}")
    tweets = list(tweet_scraper.get_items())
    if not tweets:
        return []

    first_tweet = tweets[-1]
    history = [
        {
            "timestamp": first_tweet.date.isoformat(),
            "url": first_tweet.url,
            "type": "first_tweet",
            "content": first_tweet.rawContent,
        }
    ]

    # Find replies to the first tweet and pick the earliest one
    reply_scraper = sntwitter.TwitterSearchScraper(
        f"conversation_id:{first_tweet.id}"
    )
    replies = list(reply_scraper.get_items())
    if replies:
        first_reply = replies[-1]
        mentions = re.findall(r"@([A-Za-z0-9_]+)", first_reply.rawContent)
        history.append(
            {
                "timestamp": first_reply.date.isoformat(),
                "url": first_reply.url,
                "type": "first_reply",
                "user": first_reply.user.username,
                "content": first_reply.rawContent,
                "mentions": mentions,
            }
        )

    return history
