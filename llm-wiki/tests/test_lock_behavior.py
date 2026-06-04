"""single-session lock 동작 simulate."""
import tempfile
from pathlib import Path


def simulate_session_start(lock_path: Path) -> str:
    """세션 시작 시 lock 동작 simulate.

    Returns:
        'acquired' if lock taken, 'blocked' if already held.
    """
    if lock_path.exists():
        return "blocked"
    lock_path.touch()
    return "acquired"


def simulate_session_end(lock_path: Path) -> None:
    if lock_path.exists():
        lock_path.unlink()


def test_first_session_acquires_lock():
    with tempfile.TemporaryDirectory() as tmp:
        lock = Path(tmp) / ".lock"
        assert simulate_session_start(lock) == "acquired"


def test_second_session_blocked():
    with tempfile.TemporaryDirectory() as tmp:
        lock = Path(tmp) / ".lock"
        simulate_session_start(lock)
        assert simulate_session_start(lock) == "blocked"


def test_session_end_releases_lock():
    with tempfile.TemporaryDirectory() as tmp:
        lock = Path(tmp) / ".lock"
        simulate_session_start(lock)
        simulate_session_end(lock)
        assert simulate_session_start(lock) == "acquired"


def test_double_release_safe():
    """lock 이 이미 없을 때 release 호출 — 에러 X."""
    with tempfile.TemporaryDirectory() as tmp:
        lock = Path(tmp) / ".lock"
        simulate_session_end(lock)
        simulate_session_end(lock)
