import sys

import pytest

from tkdesigner import cli


def test_cli_missing_token_explains_quoted_figma_urls(monkeypatch, capsys):
    monkeypatch.delenv("FIGMA_TOKEN", raising=False)
    monkeypatch.setattr(sys, "argv", ["tkdesigner", "ABCdef123456"])

    with pytest.raises(SystemExit):
        cli.main()

    assert "wrap the URL in quotes" in capsys.readouterr().err
