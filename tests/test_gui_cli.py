from tkdesigner import gui_cli


def test_gui_launcher_reports_missing_tk(monkeypatch, capsys):
    def fail_to_load():
        raise ModuleNotFoundError("No module named '_tkinter'", name="_tkinter")

    monkeypatch.setattr(gui_cli, "load_app", fail_to_load)

    assert gui_cli.main() == 1
    assert "Tkinter is not available" in capsys.readouterr().err


def test_gui_launcher_returns_app_exit_code(monkeypatch):
    monkeypatch.setattr(gui_cli, "load_app", lambda: lambda: 7)

    assert gui_cli.main() == 7
