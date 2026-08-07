from tkdesigner.app import supports_desktop_tk


def test_modern_tk_is_supported_on_macos():
    assert supports_desktop_tk("darwin", "8.6.14")


def test_deprecated_apple_tk_is_rejected_on_macos():
    assert not supports_desktop_tk("darwin", "8.5.9")


def test_other_platforms_are_not_subject_to_apple_tk_guard():
    assert supports_desktop_tk("linux", "8.5.9")
