
import streamlit as st
import pandas as pd
from .registry import PLATFORMS

st.set_page_config(page_title="Handle History App", page_icon="🔎")

st.title("Handle History App")
st.write("Enter a username and pick a platform. The app will try to recover handle changes and profile location history from Wayback snapshots.")

platform_key = st.selectbox("Platform", options=list(PLATFORMS.keys()), format_func=lambda k: PLATFORMS[k]["label"])
username = st.text_input("Username (without @)", value="")

if st.button("Fetch") and username.strip():
    with st.spinner("Fetching..."):
        current = PLATFORMS[platform_key]["current_info"](username.strip())
        result = PLATFORMS[platform_key]["history"](username.strip())

    st.subheader("Current")
    st.json(current)

    history = result.get("history", [])
    if not history:
        st.warning("No history found. This is common if Wayback has no intent/user snapshots or didn’t crawl the profile often.")
    else:
        df = pd.DataFrame(history)
        st.subheader("History")
        st.dataframe(df)
