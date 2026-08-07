<p align="center">
  <img width="160" src="https://user-images.githubusercontent.com/42001064/120057695-b1f6c680-c062-11eb-96d5-2c43d05f9018.png" alt="Tkinter Designer logo">
</p>

<h1 align="center">Tkinter Designer</h1>

<p align="center"><strong>Turn Figma frames into understandable, editable Tkinter apps.</strong></p>

<p align="center">
  <a href="https://github.com/ParthJadhav/Tkinter-Designer/actions"><img src="https://img.shields.io/github/actions/workflow/status/ParthJadhav/Tkinter-Designer/ci.yml?branch=master" alt="CI status"></a>
  <a href="https://pypi.org/project/tkdesigner/"><img src="https://img.shields.io/pypi/v/tkdesigner" alt="PyPI version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ParthJadhav/Tkinter-Designer" alt="BSD-3-Clause license"></a>
  <a href="https://github.com/ParthJadhav/Tkinter-Designer/stargazers"><img src="https://img.shields.io/github/stars/ParthJadhav/Tkinter-Designer" alt="GitHub stars"></a>
</p>

Tkinter Designer reads a Figma design through the official API, explains how it
will translate the file, and generates Python code plus local image assets. The
2.0 workflow is designed around confidence: inspect first, generate atomically,
then connect your application logic to ordinary Tkinter widgets.

> **2.0 preview:** this branch contains the next-generation workflow. Existing
> `tkdesigner "$FILE_URL" "$FIGMA_TOKEN"` commands remain compatible.

## What is new in 2.0

- **Design inspection** — preview frames, element types, image exports, and
  fidelity warnings with `--inspect` before writing anything.
- **Atomic generation** — a failed download never destroys the last successful
  build. The new output replaces it only after generation completes.
- **Far fewer Figma API calls** — image export URLs are requested in batches and
  reused during the run, reducing rate-limit pressure on asset-heavy designs.
- **Higher visual fidelity** — gradients, effects, opacity, and unsupported
  shapes are preserved as raster images instead of silently becoming flat
  rectangles.
- **Machine-readable output** — use `--format json` in scripts and CI.
- **Project provenance** — every build includes `tkdesigner.json` with source,
  settings, warnings, generator version, and generated files. Tokens are never
  stored.
- **A modern desktop app** — resizable native UI, code-style and theme controls,
  an inspection report, and non-blocking background generation.
- **Production-quality CLI behavior** — `--version`, useful exit errors,
  non-interactive overwrite safety, and robust environment flags.

## Install

Tkinter Designer supports Python 3.9 and newer.

```bash
python -m pip install tkdesigner
```

To try the 2.0 branch from source:

```bash
git clone https://github.com/ParthJadhav/Tkinter-Designer.git
cd Tkinter-Designer
python -m pip install -e .
```

Linux users may also need their distribution's Tk package, such as
`python3-tk`.

## Quick start

1. Create a Figma personal access token and make sure it can read the design.
2. Copy the design or selected-frame URL from Figma.
3. Inspect the conversion plan.
4. Generate the project after the report looks right.

```bash
export FIGMA_TOKEN="your-token"

tkdesigner --inspect "$FILE_URL"
tkdesigner --template class --theme clam --output ./my-app "$FILE_URL"
python ./my-app/build/gui.py
```

Always quote Figma URLs in a shell because they commonly contain `?` and `&`.
You can also pass a bare Figma file key instead of a full URL.

## CLI

```text
tkdesigner [options] FILE_URL [TOKEN]
```

| Option | Purpose |
| --- | --- |
| `--inspect`, `--dry-run` | Preview conversion without creating output |
| `--format text\|json` | Human- or machine-readable results |
| `-o`, `--output PATH` | Parent folder for the generated `build/` |
| `-f`, `--force` | Replace a non-empty build after generation succeeds |
| `-t`, `--template script\|class\|pages` | Select generated code structure |
| `--theme NAME` | Apply an installed ttk theme |
| `--no-manifest` | Skip `tkdesigner.json` |
| `-v`, `--verbose` | Enable diagnostic logging |
| `--version` | Print the installed version |

Examples:

```bash
# Inspect one selected frame as JSON
tkdesigner --inspect --format json "$FRAME_URL"

# Generate an importable class-based app
tkdesigner --template class "$FILE_URL"

# Generate one app with Back/Next navigation across frames
tkdesigner --template pages --theme clam "$FILE_URL"

# Safe automation: no prompt, JSON result, token kept out of shell history
FIGMA_TOKEN="$TOKEN" tkdesigner --force --format json -o ./release "$FILE_URL"
```

## Desktop app

Launch the redesigned desktop workflow after installation:

```bash
tkdesigner-gui
```

The app can inspect or generate without freezing while the Figma API and image
downloads are running. `gui/gui.py` remains as a compatibility launcher.

## Figma conventions

Tkinter Designer converts ordinary text, rectangles, and lines directly. Name
layers with the following reserved names when you want interactive widgets:

| Figma layer name | Generated element |
| --- | --- |
| `Button` / `ButtonHover` | Image-backed clickable button with optional hover state |
| `TextBox` | `Entry` |
| `TextArea` | `Text` |
| `Image` | Canvas image |
| `CheckBox` / `CheckButton` | `Checkbutton` |
| `RadioButton` / `Radio` | `Radiobutton` |
| `ComboBox` | `ttk.Combobox` |
| `ListBox` | `Listbox` |
| `Toggle` / `ToggleButton` | Toggle-style `Checkbutton` |
| `Table` | `ttk.Treeview` starter |
| `TabView` / `Tabs` / `Notebook` | `ttk.Notebook` starter |

Groups, components, instances, and sections are traversed automatically.
Unrecognized or visually complex elements are exported as images so the build
stays faithful and the inspection report tells you where that happens.

## Generated project

```text
build/
├── gui.py
├── gui1.py                 # additional frames with script/class templates
├── assets/
│   ├── frame0/
│   └── frame1/
└── tkdesigner.json         # source, settings, report, and file inventory
```

Generated modules only start `mainloop()` when run directly, so class and script
outputs can be imported from your application code. Regeneration stays separate
from your hand-written behavior.

## Project direction

The product model, v2 decisions, and prioritized follow-up bets live in
[docs/product-direction.md](docs/product-direction.md). The implementation map is
in [docs/architecture.md](docs/architecture.md).

The next high-value bets are component-aware bindings, responsive layout
strategies, and a project configuration file. They are intentionally staged
after the inspect/generate foundation so future features can be previewed,
validated, and reproduced.

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). A local quality pass is:

```bash
make setup
make check
```

Bug reports and focused feature proposals are welcome in
[GitHub Issues](https://github.com/ParthJadhav/Tkinter-Designer/issues). Share
generated projects in
[Show and Tell](https://github.com/ParthJadhav/Tkinter-Designer/discussions/categories/show-and-tell).

## Community and translations

Join the [Discord community](https://discord.gg/QfE5jMXxJv). Existing translated
1.x documentation remains under `docs/`; translations can be refreshed for 2.0
once the preview vocabulary stabilizes.

## License

Tkinter Designer is available under the [BSD 3-Clause License](LICENSE).
