from logs_config import get_logger
from category_mapping import SITE_CATEGORIES

logger = get_logger(__name__)


DEFAULT_CATEGORIES = ["unknown"]

def categorize_sites(found_sites: dict) -> dict:
    """
    Returns a histogram of categories.
    E.g. { 'music': 2, 'blogging': 1, ... }
    """
    category_hist = {}
    for site in found_sites.keys():
        cats = SITE_CATEGORIES.get(site, DEFAULT_CATEGORIES)
        for c in cats:
            category_hist[c] = category_hist.get(c, 0) + 1

    logger.info(f"Built histogram with {len(category_hist)} categories.")
    return category_hist
