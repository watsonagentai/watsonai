import re
from logs_config import get_logger

logger = get_logger(__name__)

def parse_sherlock_output(sherlock_output: str) -> dict:
    """
    Parse lines like '[+] SITENAME: URL'. Return {SITENAME: URL, ...}.
    """
    pattern = re.compile(r'^\[\+\]\s+(.+?):\s+(.*?)$', re.MULTILINE)
    found = {}
    matches = pattern.findall(sherlock_output)
    for site_name, url in matches:
        found[site_name.strip()] = url.strip()

    logger.info(f"Parsed {len(found)} results from Sherlock.")
    return found
