from queue import Queue

from tkdesigner.app import supports_desktop_tk
from tkdesigner.app import DesignerApp


def test_modern_tk_is_supported_on_macos():
    assert supports_desktop_tk("darwin", "8.6.14")


def test_deprecated_apple_tk_is_rejected_on_macos():
    assert not supports_desktop_tk("darwin", "8.5.9")


def test_other_platforms_are_not_subject_to_apple_tk_guard():
    assert supports_desktop_tk("linux", "8.5.9")


def test_operation_specific_failure_status(monkeypatch):
    app = DesignerApp.__new__(DesignerApp)
    app.events = Queue()

    class FailingDesigner:
        def __init__(self, *args, **kwargs):
            pass

        def inspect(self):
            raise RuntimeError("verification failure")

    monkeypatch.setattr("tkdesigner.app.Designer", FailingDesigner)
    app._run_operation(
        "inspect", type("Reference", (), {"file_key": "ABC", "node_id": None})(),
        "token", None, False, "class", "clam"
    )

    assert app.events.get_nowait() == (
        "error", "verification failure", "Inspection failed"
    )
