# Building & Releasing to Pypi

A brief explanation: packages in python are implicitly declared by providing an \_\_init\_\_.py file.
Any directory with that file present is a package, every file within a package is a module.

So, point the build environment at the dir(s) you want to include in your package in the setup.cfg file.

pyproject.toml is a declarative description of the build environment.
Our build environment needs wheel and setuptools packages to handle building for us.

[Here's a tutorial](https://packaging.python.org/tutorials/packaging-projects/) on building/releasing packages for anyone with more interest.

## Manual Release

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
    - `pip install -i https://test.pypi.org/simple/ tkinter-designer-cli-jvendegna==0.0.3` for example. That one works, feel free to test it.
    - `python -m tkdesigner.cli <URL_TO_FIGMA_FILE> $YOUR_FIGMA_TOKEN -f`


* Note: everywhere you see `python` is python3, not python2