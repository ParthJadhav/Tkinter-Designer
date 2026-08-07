# Tkinter Designer 2.0 product direction

## Product promise

Help Python developers turn a visual starting point into editable Tkinter code
without making generation feel opaque or disposable.

The primary user job is not merely “export Figma.” It is: **understand what will
translate, generate safely, and keep building in Python.**

## Product model

- **Source design** — a Figma file or selected node that a user can inspect.
- **Design report** — a read-only conversion plan: frames, element kinds, image
  exports, and fidelity warnings.
- **Generation settings** — output path, code template, and ttk theme.
- **Generated project** — code, assets, and a provenance manifest produced as
  one atomic result.

A source design has one current design report for a given selection and set of
generation settings. Generation moves through `preparing → generating → ready`
or `preparing → generating → failed`; failure leaves the prior ready project
unchanged.

This model is still a hypothesis until it is validated with user interviews and
usage data. The implementation makes it measurable without adding telemetry.

## Decisions in this branch

1. Preserve the original one-command workflow and make new capabilities opt-in.
2. Make inspection a first-class action shared by CLI and desktop UI.
3. Prefer visible fidelity warnings over silent lossy conversion.
4. Treat generated output as a reproducible project, not a loose code dump.
5. Never persist or print the Figma token.
6. Replace output only after the entire generation succeeds.
7. Reduce API pressure structurally through batching before adding retry loops
   that might leave users waiting unpredictably.

## Success signals

- More successful generations per rate-limit event.
- Fewer issues where users discover unsupported design details only after export.
- More projects using `class` or `pages` templates and importing generated code.
- Contributors can run tests, lint, and build from one documented workflow.

## Prioritized follow-up bets

### Next

- Stable semantic widget IDs and a binding file so regeneration never overwrites
  application behavior.
- `tkdesigner.toml` for repeatable project settings and token-free commands.
- Better diagnostics for fonts, clipping, mixed text styles, and oversized assets.
- Fixture-based end-to-end tests against recorded Figma responses.

### Later

- Component-property mapping for labels, values, and variants.
- Responsive layout strategies that users choose explicitly instead of an
  unreliable automatic conversion.
- Extensible renderer plugins for custom Tkinter widget libraries.
- Visual regression comparison between a Figma frame and generated app capture.

### Not yet

- A full visual editor inside Tkinter Designer. Figma remains the design surface.
- Cloud accounts or stored tokens. Local, inspectable generation is a strength.
- Automatic application logic. Generated behavior should be explicit Python.
