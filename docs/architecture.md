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

## Adding an element type

1. Add its reserved name and kind to `figma/schema.py`.
2. Implement or reuse a renderer in `custom_elements.py` or
   `vector_elements.py`.
3. Route the kind in `Frame.create_element`.
4. Add generation and inspection tests.
5. Document the Figma naming convention in the README.
