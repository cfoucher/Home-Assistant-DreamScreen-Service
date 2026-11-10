"""Serialize DreamScreen state reads sharing UDP port 8888."""
import logging
import threading
import time

_LOGGER = logging.getLogger(__name__)

RETRY_DELAY = 0.5
_READ_LOCK = threading.Lock()


def read_state(device, timeout):
    """Read the device state, retrying once, under the shared port lock."""
    with _READ_LOCK:
        if device.update_current_state(timeout):
            return True
        _LOGGER.debug("DreamScreen state read failed; retrying once")
        time.sleep(RETRY_DELAY)
        if device.update_current_state(timeout):
            _LOGGER.warning("DreamScreen state read recovered on retry")
            return True
        _LOGGER.warning("DreamScreen state read failed twice")
        return False
