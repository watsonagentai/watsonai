import sys
import subprocess
from logs_config import get_logger

logger = get_logger(__name__)

def run_sherlock_with_partial_logs(username: str) -> str:
    """
    Uses the *exact* Python executable (the venv's python)
    so that `-m sherlock` will find the installed module.
    """
    # Instead of ["python", "-u", "-m", "sherlock", username],
    # we do [sys.executable, "-u", "-m", "sherlock", username].
    cmd = ["sherlock", username]

    logger.info(f"Command: {' '.join(cmd)}")

    lines_buffer = []
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, bufsize=1) as proc:
        for line in proc.stdout:
            logger.info(f"\x1b[36m[Sherlock partial]\x1b[0m {line.rstrip()}")
            lines_buffer.append(line)
        rc = proc.wait()
        if rc != 0:
            logger.error(f"Sherlock exited with code {rc}. Partial output:\n{''.join(lines_buffer)}")

    return "".join(lines_buffer)
