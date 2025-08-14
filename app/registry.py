from .twitter_x import get_current_user_info_x, get_user_history_x

PLATFORMS = {
    "x": {
        "get_current_user_info": get_current_user_info_x,
        # History lookup returns first tweet and its earliest reply
        "get_user_history": get_user_history_x
    }
}
