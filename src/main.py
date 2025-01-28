# main.py
import sys
import os
from dotenv import load_dotenv

from logs_config import get_logger
from partial_sherlock import run_sherlock_with_partial_logs
from parser import parse_sherlock_output
from categorizer import categorize_sites
from openai_wrapper import interpret_histogram

logger = get_logger('Watson')


def main():
    load_dotenv()

    # Collect user arguments or fallback to .env
    usernames = sys.argv[1:]
    if not usernames:
        usernames = [os.getenv("SHERLOCK_USERNAME", "defaultuser")]

    logger.info(f"\x1b[93mProcessing usernames: {usernames}\x1b[0m")

    for username in usernames:
        logger.info(f"\x1b[92m=== Running Sherlock for '{username}' ===\x1b[0m")

        # 1) Run Sherlock, partial logs in real-time
        sherlock_output = run_sherlock_with_partial_logs(username)

        # 2) Parse discovered accounts
        found_sites = parse_sherlock_output(sherlock_output)
        if not found_sites:
            logger.info(f"\x1b[95mNo sites found for '{username}'\x1b[0m")
            continue
        logger.info(f'\x1b[95mFound sites: {len(found_sites)}\x1b[0m')

        # 3) Categorize
        histogram = categorize_sites(found_sites)
        logger.info(f'\x1b[95mCategorized: {histogram}\x1b[0m')

        # 4) Use new OpenAI approach
        summary = interpret_histogram(histogram)

        # 5) Log final summary in bright white
        logger.info(f"\x1b[97m\n----- FINAL SUMMARY for '{username}' -----\n{summary}\n\x1b[0m")


if __name__ == "__main__":
    main()
