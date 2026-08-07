import sys

import pytest

from tkdesigner import cli


def test_cli_missing_token_explains_quoted_figma_urls(monkeypatch, capsys):
    monkeypatch.delenv("FIGMA_TOKEN", raising=False)
    monkeypatch.setattr(sys, "argv", ["tkdesigner", "ABCdef123456"])

    with pytest.raises(SystemExit):
        cli.main()

    assert "wrap the URL in quotes" in capsys.readouterr().err


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])

    assert exc.value.code == 0
    assert "tkdesigner 2.0.0a1" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("value", "expected"),
    [("true", True), ("YES", True), ("0", False), ("off", False)],
)
def test_environment_flag_accepts_human_friendly_values(
    monkeypatch, value, expected
):
    monkeypatch.setenv("FEATURE_FLAG", value)

    assert cli.environment_flag("FEATURE_FLAG") is expected
