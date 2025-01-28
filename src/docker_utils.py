import subprocess
import shlex

from logs_config import get_logger

logger = get_logger(__name__)

SHERLOCK_IMAGE = "sherlock/sherlock"

def ensure_sherlock_image_pulled(force_pull: bool = False):
    """
    Ensures the sherlock/sherlock Docker image is present locally.
    If force_pull is True, it always pulls from Docker Hub.
    """
    if force_pull:
        logger.info("Force-pulling the latest sherlock/sherlock image...")
        pull_image()
    else:
        # Check if the image is locally available
        result = subprocess.run(
            shlex.split(f"docker images -q {SHERLOCK_IMAGE}"),
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            logger.info(f"No local {SHERLOCK_IMAGE} found. Pulling now...")
            pull_image()
        else:
            logger.info(f"Found local {SHERLOCK_IMAGE} image. Skipping pull.")

def pull_image():
    logger.info(f"Pulling Docker image: {SHERLOCK_IMAGE}")
    subprocess.check_call(shlex.split(f"docker pull {SHERLOCK_IMAGE}"))
    logger.info("Pull complete.")

def run_sherlock(username: str, output_file: str = None) -> str:
    """
    Runs sherlock in a Docker container with the given username.
    Returns stdout as a string.
    If output_file is set, it is passed as:
      -o /opt/sherlock/results/<output_file>
    """
    base_cmd = f"docker run --rm -t {SHERLOCK_IMAGE}"
    if output_file:
        base_cmd += f" -o /opt/sherlock/results/{output_file}"
    base_cmd += f" {username}"

    logger.info(f"Running Sherlock command:\n{base_cmd}")
    process = subprocess.run(
        shlex.split(base_cmd),
        capture_output=True,
        text=True
    )

    if process.returncode != 0:
        logger.error(f"Sherlock command failed: {process.stderr}")
        raise RuntimeError("Sherlock Docker run failed. See logs for details.")

    return process.stdout
