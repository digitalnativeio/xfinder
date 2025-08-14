from .twitter_x import get_current_user_info_x

PLATFORMS = {
    "x": {
        "get_current_user_info": get_current_user_info_x,
        # History lookup can be swapped in later; None indicates not implemented
        "get_user_history": None
    }
}
