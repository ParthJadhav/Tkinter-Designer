# Building & Releasing to Pypi with Poetry

## A Note:
Python packaging is a hot topic, and everyone has an opinion about it.
We migrated to poetry based on discussion in [pull request #84](https://github.com/ParthJadhav/Tkinter-Designer/pull/84)
Have we made a huge mistake? If so, open an issue and let us know!

## Publishing to testpypi
1. [Install Poetry](https://python-poetry.org/docs/#installation) - ! do not pip install poetry
2. `poetry install` - installs dependencies
3. `poetry config repositories.testpypi https://test.pypi.org/legacy/`
4. `poetry version $VERSION` - bump the version number to the value of <$VERSION>
5. `poetry publish --build -r testpypi -u __token__ -p $TESTPYPI_TOKEN`
  

## Packaging [deprecated in Tkinter-Designer as of 1.0.100]

> This was preserved as a reference for anyone interested

A brief explanation: packages in python are implicitly declared by providing an \_\_init\_\_.py file.
Any directory with that file present is a package, every file within a package is a module.

So, point the build environment at the dir(s) you want to include in your package in the setup.cfg file.

pyproject.toml is a declarative description of the build environment.
Our build environment needs wheel and setuptools packages to handle building for us.

[Here's a tutorial](https://packaging.python.org/tutorials/packaging-projects/) on building/releasing packages for anyone with more interest.

### Manual Release

Staging environment:
- Make sure conventions are followed and tests pass: `flake8 && pytest`
- Sign up for an account at [test.pypi.org](https://test.pypi.org/) and get an API key.
- Change the package name in setup.cfg to end in "-<YOUR_USERNAME>"
- Create an API key/token for yourself
- Create a .pypirc file in your home directory with something like:

```
[testpypi]
  username = __token__
  password = pypi-<YOUR_TOKEN>
```

- `pip install --upgrade build twine`
- Run `python -m build` from the main project dir, it will create a './dist' dir with the tarball and zip files.
- Run twine to publish the dist to the test pypi registry: `python -m twine upload --repository testpypi dist/*`
- To test:
    - create a new project directory, blank
    - create a venv or whatever you're into: `python -m venv .venv`
    - activate your virtualenv
    - `pip install -i https://test.pypi.org/simple/ tkdesigner-cli-jvendegna==1.0.11` for example. That one works, feel free to test it.
    - `tkdesigner <URL_TO_FIGMA_FILE> $YOUR_FIGMA_TOKEN -f`
    - `python build/gui.py`


* Note: everywhere you see `python` is python3, not python2
