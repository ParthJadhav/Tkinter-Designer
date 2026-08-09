# Changelog

All notable changes are documented here. Tkinter Designer follows semantic
versioning once a preview is promoted to a stable release.

## 2.0.0a1 — unreleased

### Added

- Read-only design inspection with text and JSON reports.
- Atomic generation that preserves the previous successful build on failure.
- Batched and per-run cached Figma image export URLs.
- Build provenance manifests without tokens.
- JSON generation results, `--version`, `--quiet`, and `--verbose`.
- Redesigned, responsive desktop application with background generation.
- Desktop keyboard shortcuts for inspect, generate, browse, and copy report.
- Copy report and Open folder actions in the desktop report pane.
- Shared element classification and fidelity warnings.
- Python 3.10–3.13 CI and tag-based trusted publishing workflow.

### Changed

- The desktop app is now a workbench: a compact configuration rail holds every
  input and both actions, and the design report fills the main pane. The
  marketing sidebar is gone and the window starts from a compact 920x640
  baseline instead of 980x760, expanding only when local font metrics require it.
- The design report reads as a document — the design name, one line of counts,
  a block per frame with its dimensions and element breakdown, and a list of
  warnings — instead of a block of plain text in a six-line box.
- Input validation appears inline beside the field that needs attention and
  moves focus there, replacing the modal error dialog. The only remaining
  dialog is the destructive build-replacement confirmation.
- Figma failures render in the report pane with an actionable hint, and keep the
  previous inspection visible below the error.
- The two actions are no longer equal weight: Generate is the primary action and
  Inspect is secondary, both pinned below the inputs they act on.
- Desktop design tokens, reusable controls, and the report document moved into
  `tkdesigner.theme`, `tkdesigner.widgets`, and `tkdesigner.report_view`; the
  theme and report document remain testable without a display.
- Tkinter Designer 2.0 now requires Python 3.10 or newer; Python 3.9 is
  end-of-life and its common macOS runtime uses an unsupported TLS stack.
- Complex effects, gradients, opacity, and unsupported nodes preserve fidelity
  through raster export.
- Empty selected frames can generate valid empty windows.
- Non-interactive environments require explicit `--force` for replacement.
- Figma API clients no longer reveal tokens in string representations.
- The desktop app reports deprecated Apple Tk 8.5 instead of opening a blank
  window on modern macOS.
- The desktop launcher reports a clear installation error when Python was built
  without Tk support.

### Fixed

- Generated windows now use their Figma frame names as native titles.
- Toggle controls keep their Figma fill and render with a visible label.
- Inspection failures use inspection-specific status text in the desktop app.
- Packaged desktop builds default output to a writable user directory.
- Generated asset paths use a portable representation on Windows and POSIX.

- The desktop window sizes its minimum from real font metrics and reserves room
  for inline validation, so the design report and the action buttons can no
  longer be clipped on a small window or a platform with taller fonts.
- Boolean values such as `TKDESIGNER_VERBOSE=true` no longer crash at import.
- Asset-heavy files use dramatically fewer Figma image API requests.
- Failed generation no longer leaves stale or partial output.
