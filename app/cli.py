import argparse
from .registry import PLATFORMS

def main():
    parser = argparse.ArgumentParser(description="Handle lookup tool")
    parser.add_argument("platform", help="Platform key, e.g., x")
    parser.add_argument("username", help="Username to lookup")
    parser.add_argument("--no-history", action="store_true", help="Skip history lookup")

    args = parser.parse_args()

    if args.platform not in PLATFORMS:
        print(f"Platform '{args.platform}' not supported")
        return

    platform = PLATFORMS[args.platform]
    get_current_user_info = platform["get_current_user_info"]
    get_user_history = platform["get_user_history"]

    # Current info
    current_info = get_current_user_info(args.username)
    if current_info:
        print("\nCurrent:")
        for k, v in current_info.items():
            print(f"- {k}: {v}")
    else:
        print("\nCurrent: No current info found.")

    # History
    if args.no_history:
        print("\nNo history found or history skipped.")
        return

    history = []
    try:
        history = get_user_history(args.username)
    except Exception as e:
        print(f"[History] Error: {e}")

    if not history:
        print("\nNo history found.")
    else:
        print("\nHistory:")
        for entry in history:
            print(f"- {entry['timestamp']} | {entry['url']}")

if __name__ == "__main__":
    main()
