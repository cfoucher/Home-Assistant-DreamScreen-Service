"""Serialize DreamScreen state reads sharing UDP port 8888."""
import threading

_READ_LOCK = threading.Lock()


def read_state(device, timeout):
    """Read the device state while holding the shared port lock."""
    with _READ_LOCK:
        return device.update_current_state(timeout)
