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
- Shared element classification and fidelity warnings.
- Python 3.9–3.13 CI and tag-based trusted publishing workflow.

### Changed

- Complex effects, gradients, opacity, and unsupported nodes preserve fidelity
  through raster export.
- Empty selected frames can generate valid empty windows.
- Non-interactive environments require explicit `--force` for replacement.
- Figma API clients no longer reveal tokens in string representations.
- The desktop app reports deprecated Apple Tk 8.5 instead of opening a blank
  window on modern macOS.

### Fixed

- Boolean values such as `TKDESIGNER_VERBOSE=true` no longer crash at import.
- Asset-heavy files use dramatically fewer Figma image API requests.
- Failed generation no longer leaves stale or partial output.
