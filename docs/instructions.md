# Using Tkinter Designer 2.0

Tkinter Designer turns top-level Figma frames into Tkinter windows or pages.
The safest workflow is to inspect, address warnings, and then generate.

## 1. Prepare the Figma file

- Put each window or page in a Figma frame.
- Keep layers inside their frame bounds when possible.
- Use the reserved layer names in the [README](../README.md#figma-conventions)
  for interactive widgets.
- Select a frame before copying its link when you only want that frame.

Complex shapes, gradients, effects, and unsupported node types are exported as
PNG assets. Ordinary text, rectangles, lines, and named widgets become editable
Tkinter code.

## 2. Create a Figma token

Create a personal access token in Figma and grant it read access to the source
file. Keep it out of source control. The recommended setup is an environment
variable:

```bash
export FIGMA_TOKEN="your-token"
```

PowerShell:

```powershell
$env:FIGMA_TOKEN = "your-token"
```

## 3. Inspect before generating

```bash
tkdesigner --inspect "$FILE_URL"
```

Inspection fetches the design document but does not export images or create the
output folder. It reports:

- selected frames and dimensions;
- the number and kinds of generated elements;
- the number of Figma image exports;
- rasterization and multi-page sizing warnings.

Use JSON for automation:

```bash
tkdesigner --inspect --format json "$FILE_URL" > design-report.json
```

## 4. Generate

```bash
tkdesigner --output ./my-project --template class "$FILE_URL"
```

Templates:

- `script` creates one straightforward module per frame.
- `class` wraps each generated window in `GeneratedApp` for easier importing.
- `pages` creates one app with Back/Next navigation across all selected frames.

If `build/` already contains files, Tkinter Designer asks before replacing it.
In automation, pass `--force`. Generation is staged first; the existing build is
only replaced when every code file and asset is ready.

## 5. Connect behavior

Run the result directly:

```bash
python ./my-project/build/gui.py
```

Or import a class-based build:

```python
from build.gui import GeneratedApp

app = GeneratedApp()
# Attach commands or populate widgets here.
app.run()
```

Keep business logic outside the generated module when you plan to regenerate.
The `tkdesigner.json` manifest records the exact source, template, warnings,
version, and generated files, without storing the Figma token.

## Desktop workflow

```bash
tkdesigner-gui
```

The window is a workbench: every input and both actions sit in the left rail,
and the design report fills the main pane.

Paste the design URL, use the token from `FIGMA_TOKEN` or enter one, choose the
output and template, and select **Inspect design**. Generate after reviewing the
report. Network work runs in the background so the app remains responsive, and
the inputs lock while a run is in flight so the request cannot drift.

The report lists a summary, every frame with its dimensions and element
breakdown, and any fidelity warnings. **Copy report** puts the plain-text
version on the clipboard; after a successful generate, **Open folder** reveals
the build. A failed run keeps the previous inspection below the error.

| Shortcut | Action |
| --- | --- |
| `⌘I` / `Ctrl+I` | Inspect design |
| `⌘↩` / `Ctrl+Return` | Generate project |
| `⌘O` / `Ctrl+O` | Choose the output folder |
| `⌘⇧C` / `Ctrl+Shift+C` | Copy the report |

The token stays masked unless you press **Show**, re-masks whenever a run
starts, and never appears in the report, the status line, or the clipboard.

The window starts from a 920x640 baseline and measures the minimum height its
controls need on the active Tk runtime, so taller platform fonts do not clip the
form. On macOS the desktop app requires Tk 8.6 or newer. If the launcher reports
an older Tk runtime, install a current Python distribution with modern Tk
support and recreate the virtual environment.

## Troubleshooting

### The token is missing

Set `FIGMA_TOKEN` or pass the token as the final argument. Quote the Figma URL so
shell characters such as `&` do not split the command.

### Figma denied access

Confirm the token owner can open the file and the token has file-read access.

### API rate limit

Wait for the quota to reset, then retry. Tkinter Designer 2.0 batches image URL
requests, so large designs make substantially fewer API calls than 1.x.

### The result does not match Figma

Run `--inspect` and review rasterization warnings. Ensure the desired content is
inside a frame, visible, and has an `absoluteBoundingBox`. File a bug with the
inspection JSON and a minimal shareable Figma example; never include your token.
