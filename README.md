
# Handle History App (OSINT-lite)

This Python app lets you enter a **username** (currently focused on X/Twitter) and attempts to recover a **history of handle changes** and **profile data like location** using the **Wayback Machine**.

It works in two parts:
1. Gets the user's **numeric user ID** from the current profile page.
2. Uses Wayback's snapshots of `intent/user?user_id=...` to recover the handle over time, then fetches matching archived profile pages to pull the location field over time.

> Note: Social sites change often, and some pages block scraping. Treat this as **best-effort OSINT**. If Wayback never crawled the profile at the right times, you won't get complete history.


## Quick start

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) CLI usage
```bash
python -m app.cli x a_username
# Example:
python -m app.cli x elonmusk
```

This will print a table of handle snapshots and any location text we could extract per snapshot.

### 3) Streamlit UI
```bash
streamlit run app/app_streamlit.py
```
Open the local URL shown in your terminal, type a username, and click **Fetch**.

## Platforms supported

- **X/Twitter**: Implemented. We detect the user's numeric ID from the current profile page, then use Wayback data to infer past handles and try to extract profile locations per snapshot.
- **Instagram, GitHub, others**: Stubs are included to make it easy to add later. Some sites do not expose handle history, so Wayback snapshots and indirect signals are your friend.

## Caveats

- Handle history is **not officially exposed** by most platforms.
- All results depend on **archived snapshots**. If the Wayback Machine did not capture the redirects or the profile at certain times, history will be incomplete.
- Modern profile pages are often client-rendered, which can make parsing brittle. The code includes multiple fallback patterns.
- Be mindful of each platform's Terms of Service if you extend this beyond Wayback and public pages.

## Tips for better hit rates

- Try both `twitter.com` and `x.com` when scraping Wayback.
- If you know the **user ID** already, you can call the functions directly and skip scraping for it.
- Try requesting **more snapshots** and then deduplicate the results by handle and day to reduce noise.

## Extending to other platforms

- Add a `get_current_user_info_*` function that returns at least: `{ "platform": "...", "username": "...", "user_id": "...", "location": "..." }`.
- Add a corresponding `get_handle_history_*` that uses Wayback snapshots, or any first-party API you have access to.
- Register the platform in `app/registry.py`.

## Legal and ethical use

Use responsibly. This is for research and recruitment due diligence, not harassment. Stick to public info and comply with local laws and each site's policies.
