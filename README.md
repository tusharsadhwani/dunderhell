# dunderhell

Turn all your Python code into dunders.

## Installation

```bash
pip install dunderhell
```

## Usage

```console
$ cat foo.py
print(1)
$ dunderhell foo.py
print(__name__.__len__().__floordiv__(__name__.__len__()))
```

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -r requirements-dev.txt` to do an editable install
- Run `pytest` to run tests

## Type Checking

Run `mypy .`

## Create and upload a package to PyPI

Make sure to bump the version in `setup.cfg`.

Then run the following commands:

```bash
rm -rf build dist
python setup.py sdist bdist_wheel
```

Then upload it to PyPI using [twine](https://twine.readthedocs.io/en/latest/#installation):

```bash
twine upload dist/*
```
