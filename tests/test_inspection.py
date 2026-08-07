import json

from tkdesigner.inspection import build_design_report


def test_inspection_report_explains_generation_without_exporting_assets():
    frame = {
        "id": "1:1",
        "name": "Dashboard",
        "type": "FRAME",
        "absoluteBoundingBox": {"x": 0, "y": 0, "width": 800, "height": 600},
        "children": [
            {
                "id": "2:1",
                "name": "Title",
                "type": "TEXT",
                "absoluteBoundingBox": {"x": 10, "y": 10, "width": 100, "height": 20},
            },
            {
                "id": "2:2",
                "name": "Chart",
                "type": "ELLIPSE",
                "absoluteBoundingBox": {"x": 10, "y": 50, "width": 200, "height": 200},
            },
        ],
    }

    report = build_design_report(
        file_data={"name": "Analytics", "lastModified": "2026-08-07T10:00:00Z"},
        file_key="ABC123",
        selected_node_id="1:1",
        template="class",
        frame_nodes=[frame],
    )
    payload = json.loads(report.to_json())

    assert payload["summary"] == {"elements": 2, "frames": 1, "image_exports": 1}
    assert payload["frames"][0]["element_kinds"] == {"raster": 1, "text": 1}
    assert "unsupported element(s)" in payload["warnings"][0]
    assert "Dashboard (800x600)" in report.to_text()


def test_pages_report_warns_about_mixed_frame_sizes():
    def frame(frame_id, width):
        return {
            "id": frame_id,
            "name": frame_id,
            "type": "FRAME",
            "absoluteBoundingBox": {"width": width, "height": 600},
            "children": [],
        }

    report = build_design_report(
        file_data={},
        file_key="ABC123",
        selected_node_id=None,
        template="pages",
        frame_nodes=[frame("Desktop", 1200), frame("Mobile", 390)],
    )

    assert any("different dimensions" in warning for warning in report.warnings)
