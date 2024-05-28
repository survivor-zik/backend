from datetime import datetime
import time


def generate_unique_id():
    """Generates a unique ID by combining the current date and time with a random number.

    Returns:
        str: A unique ID string.
    """

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    random_part = str(int(time.time() * 1000) % 1000).zfill(3)  # Pad with zeros
    unique_id = f"{timestamp}{random_part}"
    return unique_id
