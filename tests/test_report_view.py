"""The design report document is built without Tkinter, so it is asserted here."""

from tkdesigner import report_view
from tkdesigner.report_view import (
    PARAGRAPH_TAGS,
    TAG_STYLES,
    empty_segments,
    error_hint,
    error_segments,
    generation_segments,
    inspection_segments,
    kind_label,
    kind_summary,
    segments_to_text,
    working_segments,
)
from tkdesigner.theme import COLORS, build_fonts


def build_report(frames=None, warnings=()):
    return {
        "source": {
            "file_key": "aBcD1234xYz",
            "file_name": "Dashboard UI Kit",
            "selected_node_id": None,
            "last_modified": "2026-08-07T09:14:22Z",
        },
        "generation": {"template": "class"},
        "summary": {"frames": 2, "elements": 40, "image_exports": 7},
        "frames": frames if frames is not None else [
            {
                "id": "1:2", "name": "Window", "width": 1440, "height": 900,
                "elements": 30,
                "element_kinds": {"text": 20, "button": 6, "rectangle": 4},
            },
            {
                "id": "1:3", "name": "Login", "width": 480, "height": 640,
                "elements": 10, "element_kinds": {"text": 7, "text_input": 3},
            },
        ],
        "warnings": list(warnings),
    }


def tags_of(segments):
    return [segment.tag for segment in segments]


def test_inspection_renders_name_key_and_template():
    text = segments_to_text(inspection_segments(build_report()))
    assert "Dashboard UI Kit" in text
    assert "aBcD1234xYz" in text
    # Phrased as provenance: it describes the run that produced this report,
    # not whatever the code-style control currently shows.
    assert "inspected as class" in text


def test_modified_timestamp_is_reduced_to_a_date():
    text = segments_to_text(inspection_segments(build_report()))
    assert "modified 2026-08-07" in text
    assert "T09:14:22Z" not in text


def test_headline_counts_render_as_one_line():
    counts = [s.text for s in inspection_segments(build_report()) if s.tag == "counts"]
    assert counts == ["2 frames · 40 elements · 7 image exports\n"]


def test_every_frame_gets_a_row_with_its_dimensions():
    text = segments_to_text(inspection_segments(build_report()))
    assert "Window" in text and "1440×900" in text
    assert "Login" in text and "480×640" in text


def test_element_breakdown_is_one_line_per_frame_ordered_by_count():
    kinds = [s.text for s in inspection_segments(build_report()) if s.tag == "frame_kinds"]
    assert kinds == ["text 20 · button 6 · rect 4\n", "text 7 · input 3\n"]


def test_kind_summary_uses_short_labels():
    assert kind_summary({"text_input": 3, "rectangle": 9}) == "rect 9 · input 3"


def test_unmapped_kinds_fall_back_to_their_raw_name():
    assert kind_label("text") == "text"
    assert kind_label("mystery") == "mystery"


def test_frames_without_elements_say_so():
    empty_frame = build_report(frames=[{
        "id": "1:9", "name": "Scratch", "width": 800, "height": 600,
        "elements": 0, "element_kinds": {},
    }])
    text = segments_to_text(inspection_segments(empty_frame))
    assert "no renderable elements" in text


def test_warnings_are_listed_under_one_heading():
    segments = inspection_segments(build_report(warnings=["Frame X is empty."]))
    text = segments_to_text(segments)
    assert "WARNINGS" in text
    assert "Frame X is empty." in text
    assert tags_of(segments).count("warn_text") == 1


def test_no_warnings_means_no_warnings_section():
    assert "WARNINGS" not in segments_to_text(inspection_segments(build_report()))


def test_generation_block_reports_path_and_counts():
    text = segments_to_text(generation_segments("/tmp/app/build", 3, 21))
    assert "/tmp/app/build" in text
    assert "3 code files · 21 assets" in text
    assert "generated successfully" in text


def test_known_failures_map_to_an_actionable_hint():
    assert "token" in error_hint("Figma returned 403 Forbidden").lower()
    assert "access" in error_hint("404 Not Found").lower()
    assert error_hint("something unexpected happened") == ""


def test_error_document_leads_with_the_message():
    segments = error_segments("Figma returned 403 Forbidden")
    assert tags_of(segments)[0] == "err_text"
    assert "hint_text" in tags_of(segments)


def test_a_failure_keeps_the_previous_inspection_visible():
    text = segments_to_text(error_segments("Network timed out", build_report()))
    assert "LAST INSPECTION" in text
    assert "Dashboard UI Kit" in text


def test_empty_state_names_the_shortcut_and_where_to_get_a_token():
    text = segments_to_text(empty_segments("⌘I"))
    assert "⌘I" in text
    assert "Personal access" in text


def test_working_placeholder_names_the_operation():
    assert "Inspecting" in segments_to_text(working_segments("inspect"))
    assert "Generating" in segments_to_text(working_segments("generate"))


def test_the_document_uses_no_background_fills():
    """Severity reads from colour and heading, not from badges or boxes."""
    for style in TAG_STYLES.values():
        assert "bg" not in style


def test_every_emitted_tag_has_a_style():
    documents = [
        inspection_segments(build_report(warnings=["w"])),
        generation_segments("/tmp/build", 1, 2),
        error_segments("403 Forbidden", build_report()),
        empty_segments("Ctrl+I"),
        working_segments("inspect"),
    ]
    for segments in documents:
        for segment in segments:
            assert segment.tag is None or segment.tag in TAG_STYLES


def test_tag_styles_reference_real_tokens_and_font_roles():
    fonts = build_fonts("Helvetica", "Courier")
    for tag, style in TAG_STYLES.items():
        assert style.get("font", "body") in fonts, tag
        if "fg" in style:
            assert style["fg"] in COLORS, tag


def test_paragraph_tags_all_exist():
    for tag in PARAGRAPH_TAGS:
        assert tag in TAG_STYLES


def test_report_view_does_not_depend_on_tkinter():
    assert "tkinter" not in vars(report_view)
