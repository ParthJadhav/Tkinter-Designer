# Architecture

Tkinter Designer has one application core with two interfaces.

```text
CLI (tkdesigner) ──────┐
                      ├── Designer ── inspection ── DesignReport
Desktop app ──────────┘      │
                             ├── Figma Files client ── batched API exports
                             ├── Frame + element renderers
                             └── atomic build ── code + assets + manifest
```

## Modules

- `tkdesigner.cli` parses shell inputs, handles safe overwrite policy, and emits
  text or JSON.
- `tkdesigner.app` is the responsive desktop client. It performs network work on
  a background thread and sends display results back to the Tk event loop.
- `tkdesigner.theme` holds the desktop design tokens: palette, spacing scale,
  type roles, and per-platform keyboard shortcuts. It imports no Tkinter.
- `tkdesigner.widgets` holds the reusable desktop controls, each painting its
  own rest, hover, pressed, focused, and disabled states so the interface looks
  the same on every platform instead of inheriting three native themes.
- `tkdesigner.report_view` turns a `DesignReport` into the tagged document the
  desktop report pane renders. It imports no Tkinter, so the document is
  asserted in tests without a display.
- `tkdesigner.gui_cli` is the optional desktop dependency boundary and turns a
  missing Tk runtime into an actionable launcher error.
- `tkdesigner.designer` selects frames, coordinates inspection and rendering,
  stages output, and atomically commits successful builds.
- `tkdesigner.inspection` contains immutable report objects and serialization.
- `tkdesigner.figma.endpoints` owns Figma HTTP calls and per-run image URL cache.
- `tkdesigner.figma.schema` is the single classification policy shared by
  inspection and rendering.
- `tkdesigner.figma.frame`, `custom_elements`, and `vector_elements` render Figma
  nodes into Jinja template inputs and local PNG assets.
- `tkdesigner.template` contains the generated Tkinter application templates.

## Invariants

- Inspection never creates output or downloads image assets.
- Inspection and rendering classify nodes with the same policy.
- A Figma token is used only in request headers and never enters logs or output.
- Non-empty output requires explicit confirmation or `--force`.
- Failed generation does not mutate the previous successful build.
- Generated Python remains import-safe: `mainloop()` runs only under `__main__`.
- The desktop window measures its own minimum size from real font metrics at
  startup, so no control is ever clipped on a platform whose fonts are taller.

## Adding an element type

1. Add its reserved name and kind to `figma/schema.py`.
2. Implement or reuse a renderer in `custom_elements.py` or
   `vector_elements.py`.
3. Route the kind in `Frame.create_element`.
4. Add generation and inspection tests.
5. Document the Figma naming convention in the README.
