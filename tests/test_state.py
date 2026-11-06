"""Tests for serialized DreamScreen state reads."""

import importlib.util
import threading
import time
from pathlib import Path

import pytest

STATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "custom_components"
    / "dreamscreen"
    / "state.py"
)


@pytest.fixture
def state():
    """Load state.py without importing the Home Assistant package."""
    spec = importlib.util.spec_from_file_location("dreamscreen_state", STATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeDevice:
    """Simulate a blocking state read."""

    def __init__(self, events):
        self.events = events

    def update_current_state(self, timeout):
        self.events.append("start")
        time.sleep(0.1)
        self.events.append("end")
        return True


def test_read_state_serializes_concurrent_reads(state):
    events = []
    device = FakeDevice(events)
    barrier = threading.Barrier(2)

    def read():
        barrier.wait()
        state.read_state(device, 1)

    threads = [threading.Thread(target=read) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert events == ["start", "end", "start", "end"]
