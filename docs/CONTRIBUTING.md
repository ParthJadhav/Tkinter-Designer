# Contributing to Tkinter Designer

Thanks for helping make design-to-Tkinter generation more dependable. Read the
[Code of Conduct](../CODE_OF_CONDUCT.md) before participating.

## Start with the product model

Read [product-direction.md](product-direction.md) and
[architecture.md](architecture.md). Focused fixes and features that improve the
inspect → generate → integrate workflow are easier to evaluate than broad
renderer rewrites.

Search [existing issues](https://github.com/ParthJadhav/Tkinter-Designer/issues)
before opening a new one. For conversion bugs, include:

- the Tkinter Designer and Python versions;
- operating system;
- `tkdesigner --inspect --format json` output;
- a minimal shareable Figma example or sanitized response fixture;
- expected and actual generated behavior.

Never post a Figma token or private design response.

## Local setup

```bash
git clone https://github.com/ParthJadhav/Tkinter-Designer.git
cd Tkinter-Designer
git switch -c your-focused-branch
make setup
make check
```

The Makefile creates `.venv`, installs the package in editable mode, runs the
test and lint suites, and builds both source and wheel distributions. Poetry
users can instead run `poetry install` and the equivalent commands through
`poetry run`.

## Development rules

- Preserve the existing CLI syntax unless a breaking change is explicitly
  accepted for a major release.
- Keep Figma token values out of logs, exceptions, fixtures, and manifests.
- Inspection must remain read-only and use the same classification rules as
  generation.
- Add tests for both the successful path and failure behavior.
- Do not overwrite a valid build until a new build is complete.
- Generated Python should compile and remain safe to import.
- Update user documentation when adding a CLI option or reserved layer name.

## Pull requests

Keep the pull request scoped and explain:

1. the user problem;
2. the chosen behavior and tradeoffs;
3. tests and manual verification;
4. migration impact, if any.

Run `make check` before requesting review. Maintainers may ask for a recorded
Figma fixture when behavior depends on API response details.
