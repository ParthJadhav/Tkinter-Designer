from pathlib import Path
from queue import Queue

import pytest

from tkdesigner.app import (
    INVALID_URL,
    MISSING_OUTPUT,
    MISSING_TOKEN,
    MISSING_URL,
    DesignerApp,
    FieldError,
    middle_truncate,
    supports_desktop_tk,
)


class Value:
    """A stand-in for a Tk variable so validation is testable without a display."""

    def __init__(self, value=""):
        self._value = value

    def get(self):
        return self._value


def make_app(url="", token="", output="/tmp/out"):
    app = DesignerApp.__new__(DesignerApp)
    app.url = Value(url)
    app.token = Value(token)
    app.output = Value(output)
    return app


VALID_URL = "https://www.figma.com/design/aBcD1234/Dashboard"


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


def test_successful_inspection_carries_the_report_object(monkeypatch):
    app = DesignerApp.__new__(DesignerApp)
    app.events = Queue()
    sentinel = object()

    class StubDesigner:
        def __init__(self, *args, **kwargs):
            pass

        def inspect(self):
            return sentinel

    monkeypatch.setattr("tkdesigner.app.Designer", StubDesigner)
    app._run_operation(
        "inspect", type("Reference", (), {"file_key": "ABC", "node_id": None})(),
        "token", None, False, "class", "clam"
    )

    event, detail, status = app.events.get_nowait()
    assert (event, detail, status) == ("inspected", sentinel, "Inspection complete")


def test_missing_url_points_at_the_url_field():
    with pytest.raises(FieldError) as error:
        make_app()._inputs()
    assert error.value.field == "url"
    assert str(error.value) == MISSING_URL


def test_unparseable_url_points_at_the_url_field():
    with pytest.raises(FieldError) as error:
        make_app(url="https://example.com/nope", token="t")._inputs()
    assert error.value.field == "url"
    assert str(error.value) == INVALID_URL


def test_missing_token_is_reported_after_the_url_parses():
    with pytest.raises(FieldError) as error:
        make_app(url=VALID_URL)._inputs()
    assert error.value.field == "token"
    assert str(error.value) == MISSING_TOKEN


def test_missing_output_is_reported_last():
    with pytest.raises(FieldError) as error:
        make_app(url=VALID_URL, token="t", output="  ")._inputs()
    assert error.value.field == "output"
    assert str(error.value) == MISSING_OUTPUT


def test_valid_inputs_resolve_to_a_reference_and_absolute_path():
    reference, token, output = make_app(
        url=VALID_URL, token="  secret  ", output="~/designs"
    )._inputs()
    assert reference.file_key == "aBcD1234"
    assert token == "secret"
    assert output.is_absolute()
    assert output == Path("~/designs").expanduser().resolve()


def test_a_bare_file_key_is_accepted_like_the_cli():
    reference, _token, _output = make_app(url="aBcD1234", token="t")._inputs()
    assert reference.file_key == "aBcD1234"


def test_short_paths_are_left_alone():
    assert middle_truncate("/tmp/build") == "/tmp/build"


def test_long_paths_are_truncated_in_the_middle_and_keep_the_leaf():
    value = "/Users/someone/very/deeply/nested/project/folder/output/build"
    result = middle_truncate(value, limit=30)
    assert len(result) == 30
    assert result.startswith("/Users/someone")
    assert result.endswith("build")
    assert "…" in result
