import pytest

from tkdesigner.designer import Designer
from tkdesigner.figma.custom_elements import Button, TextEntry
from tkdesigner.figma.endpoints import FigmaAPIError, Files
from tkdesigner.figma.frame import Frame
from tkdesigner.template import CLASS_TEMPLATE, TEMPLATE


def solid_fill(r, g, b):
    return [{"type": "SOLID", "color": {"r": r, "g": g, "b": b, "a": 1}}]


def frame_node(children=None):
    return {
        "id": "1:1",
        "name": "Window",
        "type": "FRAME",
        "absoluteBoundingBox": {"x": 100, "y": 50, "width": 320, "height": 240},
        "fills": solid_fill(1, 1, 1),
        "children": children or [],
    }


def test_generated_code_preserves_negative_coordinates_and_escapes_text(tmp_path):
    child = {
        "id": "2:1",
        "name": "Title",
        "type": "TEXT",
        "absoluteBoundingBox": {"x": 75, "y": 60, "width": 100, "height": 20},
        "fills": solid_fill(0, 0.5, 0),
        "characters": 'Hello "Tk"\nDesigner',
        "style": {
            "fontFamily": "Fira Code",
            "fontSize": 14,
            "fontWeight": 700,
            "italic": True,
        },
    }

    frame = Frame(frame_node([child]), object(), tmp_path, 0)
    code = frame.to_code(TEMPLATE)

    assert "-25" in code
    assert "10" in code
    assert 'text="Hello \\"Tk\\"\\nDesigner"' in code
    assert 'font=("Fira Code", 14 * -1, "bold", "italic")' in code
    assert 'if __name__ == "__main__":' in code
    compile(code, "gui.py", "exec")


def test_textbox_names_generate_entry_widgets(tmp_path):
    element = {
        "id": "2:2",
        "name": "textbox",
        "type": "RECTANGLE",
        "absoluteBoundingBox": {"x": 110, "y": 75, "width": 160, "height": 40},
        "fills": solid_fill(0, 0, 0),
    }

    entry = TextEntry(element, Frame(frame_node([]), object(), tmp_path, 0), "entry.png", id_="1")
    code = entry.to_code()

    assert "entry_1 = Entry(" in code
    assert "None(" not in code
    assert "load_photo_image(\n    relative_to_assets" in code
    assert "file=relative_to_assets" not in code
    assert 'fg="#FFFFFF"' in code
    assert 'insertbackground="#FFFFFF"' in code


def test_image_buttons_use_label_backed_button_to_avoid_tk_borders(tmp_path):
    element = {
        "id": "2:9",
        "name": "Button",
        "type": "RECTANGLE",
        "absoluteBoundingBox": {"x": 110, "y": 75, "width": 120, "height": 32},
        "fills": solid_fill(0.2, 0.4, 0.9),
    }

    button = Button(element, Frame(frame_node([]), object(), tmp_path, 0), "button.png", id_="1")
    code = button.to_code()

    assert "button_1 = ImageButton(" in code
    assert "command=lambda: print" in code


def test_class_template_compiles_for_simple_frame(tmp_path):
    child = {
        "id": "2:3",
        "name": "Rectangle",
        "type": "RECTANGLE",
        "absoluteBoundingBox": {"x": 120, "y": 80, "width": 80, "height": 32},
        "fills": solid_fill(0.9, 0.2, 0.2),
        "cornerRadius": 8,
    }

    frame = Frame(frame_node([child]), object(), tmp_path, 0)
    code = frame.to_code(CLASS_TEMPLATE)

    assert "create_rounded_rectangle(" in code
    assert "ASSETS_PATH = OUTPUT_PATH / Path(r\"assets/frame0\")" in code
    assert 'if __name__ == "__main__":' in code
    compile(code, "gui.py", "exec")


def test_table_and_tabview_generate_native_ttk_widgets(tmp_path):
    children = [
        {
            "id": "2:5",
            "name": "Table",
            "type": "RECTANGLE",
            "absoluteBoundingBox": {"x": 110, "y": 70, "width": 180, "height": 80},
            "fills": solid_fill(1, 1, 1),
        },
        {
            "id": "2:6",
            "name": "TabView",
            "type": "RECTANGLE",
            "absoluteBoundingBox": {"x": 110, "y": 160, "width": 180, "height": 60},
            "fills": solid_fill(1, 1, 1),
        },
    ]

    frame = Frame(frame_node(children), object(), tmp_path, 0)
    code = frame.to_code(TEMPLATE)

    assert "ttk.Treeview(" in code
    assert "ttk.Notebook(" in code
    compile(code, "gui.py", "exec")


def test_pages_template_generates_navigation_app(tmp_path):
    designer = Designer.__new__(Designer)
    designer.output_path = tmp_path
    designer.figma_file = object()
    designer.node_id = None
    designer.template_style = "pages"
    designer.theme = "clam"
    designer.file_data = {
        "document": {
            "children": [
                {
                    "id": "0:1",
                    "type": "CANVAS",
                    "children": [
                        frame_node([
                            {
                                "id": "2:7",
                                "name": "Rectangle",
                                "type": "RECTANGLE",
                                "absoluteBoundingBox": {
                                    "x": 120,
                                    "y": 80,
                                    "width": 80,
                                    "height": 32,
                                },
                                "fills": solid_fill(0.2, 0.4, 0.9),
                            }
                        ]),
                        {
                            **frame_node([
                                {
                                    "id": "2:8",
                                    "name": "Title",
                                    "type": "TEXT",
                                    "absoluteBoundingBox": {
                                        "x": 120,
                                        "y": 90,
                                        "width": 100,
                                        "height": 20,
                                    },
                                    "fills": solid_fill(0, 0, 0),
                                    "characters": "Second",
                                    "style": {"fontFamily": "Arial", "fontSize": 12},
                                }
                            ]),
                            "id": "1:2",
                        },
                    ],
                }
            ]
        }
    }

    code = designer.to_code()[0]

    assert 'THEME = "clam"' in code
    assert "class Page0(Frame):" in code
    assert "class Page1(Frame):" in code
    assert "def next_page(self):" in code
    assert 'set_assets_path(r"assets/frame0")' in code
    assert 'set_assets_path(r"assets/frame1")' in code
    compile(code, "gui.py", "exec")


def test_design_clean_removes_stale_build_files(tmp_path):
    output_path = tmp_path / "build"
    output_path.mkdir()
    stale_file = output_path / "stale.txt"
    stale_file.write_text("old", encoding="UTF-8")

    designer = Designer.__new__(Designer)
    designer.output_path = output_path
    designer.to_code = lambda: ["print('new')"]

    designer.design(clean=True)

    assert not stale_file.exists()
    assert output_path.joinpath("gui.py").read_text(encoding="UTF-8") == "print('new')"


def test_designer_uses_selected_node_when_url_has_node_id():
    designer = Designer.__new__(Designer)
    designer.node_id = "2:4"
    designer.file_data = {
        "document": {
            "children": [
                {
                    "id": "0:1",
                    "type": "CANVAS",
                    "children": [
                        frame_node([
                            {
                                "id": "2:4",
                                "name": "Nested",
                                "type": "FRAME",
                                "absoluteBoundingBox": {
                                    "x": 0,
                                    "y": 0,
                                    "width": 100,
                                    "height": 100,
                                },
                                "fills": solid_fill(1, 1, 1),
                                "children": [{"id": "leaf", "type": "TEXT"}],
                            }
                        ])
                    ],
                }
            ]
        }
    }

    frames = designer._target_frame_nodes()

    assert [frame["id"] for frame in frames] == ["2:4"]


def test_figma_rate_limit_errors_are_human_readable(monkeypatch):
    class Response:
        status_code = 429

        def json(self):
            return {"err": "Rate limit exceeded"}

    monkeypatch.setattr(
        "tkdesigner.figma.endpoints.requests.get",
        lambda *args, **kwargs: Response(),
    )

    with pytest.raises(FigmaAPIError, match="rate limit exceeded"):
        Files("token", "file").get_file()
