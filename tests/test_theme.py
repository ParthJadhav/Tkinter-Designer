"""Design tokens are shared by the workspace, the widgets, and the report."""

from tkdesigner.theme import (
    COLORS,
    MONO_SCALE,
    SPACE,
    TYPE_SCALE,
    build_fonts,
    shortcut_labels,
)


def test_every_type_role_resolves_to_a_font_tuple():
    fonts = build_fonts("Helvetica", "Courier")
    for role in TYPE_SCALE:
        assert fonts[role][0] == "Helvetica"


def test_mono_roles_use_the_fixed_width_family():
    fonts = build_fonts("Helvetica", "Courier")
    for role in MONO_SCALE:
        assert fonts[role][0] == "Courier"


def test_normal_weight_roles_omit_the_weight_element():
    fonts = build_fonts("Helvetica", "Courier")
    assert fonts["body"] == ("Helvetica", 11)
    assert fonts["body_bold"] == ("Helvetica", 11, "bold")


def test_type_scale_stays_within_the_compact_range():
    sizes = [size for size, _weight in TYPE_SCALE.values()]
    assert min(sizes) >= 9
    assert max(sizes) <= 13


def test_spacing_scale_is_the_documented_set():
    assert sorted(SPACE.values()) == [4, 8, 12, 16, 24]


def test_macos_and_other_platforms_get_different_modifiers():
    mac = shortcut_labels("darwin")
    other = shortcut_labels("win32")
    assert mac["inspect"][0] == "<Command-i>"
    assert other["inspect"][0] == "<Control-i>"
    assert "Ctrl" in other["generate"][1]


def test_every_platform_defines_the_same_actions():
    assert set(shortcut_labels("darwin")) == set(shortcut_labels("linux"))


def test_colors_are_all_hex_triplets():
    for name, value in COLORS.items():
        assert value.startswith("#") and len(value) == 7, name
        int(value[1:], 16)
