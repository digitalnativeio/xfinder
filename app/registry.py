from .twitter_x import get_current_user_info_x

PLATFORMS = {
    "x": {
        "get_current_user_info": get_current_user_info_x,
        "get_history": None  # We'll swap this later if you want archive-based history
    }
}
