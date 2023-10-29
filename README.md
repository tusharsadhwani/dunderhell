# dunderhell

Turn your Python code entirely into dunders.

## Installation

```bash
pip install dunderhell
```

## Usage

```python
$ cat foo.py
print(1)

$ cat foo.py | python3
1

$ dunderhell foo.py
__chr__ = __builtins__.__getattribute__(__name__.__reduce__.__name__[
__name__.__len__().__floordiv__(__name__.__len__()).__add__(__name__.__len__()
.__floordiv__(__name__.__len__())).__add__(__name__.__len__().__floordiv__(
__name__.__len__())).__add__(__name__.__len__().__floordiv__(__name__.__len__()
)).__add__(__name__.__len__().__floordiv__(__name__.__len__())).__add__(
__name__.__len__().__floordiv__(__name__.__len__()))].__add__(
__name__.__add__.__class__.__name__[__name__.__len__().__floordiv__(
__name__.__len__()).__add__(__name__.__len__().__floordiv__(__name__.__len__())
).__add__(__name__.__len__().__floordiv__(__name__.__len__()))]).__add__(
__name__.__class__.__name__[__name__.__len__().__floordiv__(__name__.__len__())
.__neg__()]))

__builtins__.__getattribute__(__chr__(__name__.__len__().__mul__(
__name__.__len__()).__add__(__name__.__len__()).__add__(__name__.__len__())
.__add__(__name__.__len__()).__add__(__name__.__len__()).__add__(
__name__.__len__()).__add__(__name__.__len__())).__add__(__chr__(
__name__.__len__().__mul__(__name__.__len__()).__add__(__name__.__len__())
.__add__(__name__.__len__()).__add__(__name__.__len__()).__add__(
__name__.__len__()).__add__(__name__.__len__()).__add__(__name__.__len__())
.__add__(__name__.__len__().__floordiv__(__name__.__len__()).__add__(
__name__.__len__().__floordiv__(__name__.__len__()))))).__add__(__chr__(
__name__.__len__().__mul__(__name__.__len__()).__add__(__name__.__len__())
.__add__(__name__.__len__()).__add__(__name__.__len__()).__add__(
__name__.__len__()).__add__(__name__.__len__()).__add__(__name__.__len__()
.__floordiv__(__name__.__len__())))).__add__(__chr__(__name__.__len__()
.__mul__(__name__.__len__()).__add__(__name__.__len__()).__add__(
__name__.__len__()).__add__(__name__.__len__()).__add__(__name__.__len__())
.__add__(__name__.__len__()).__add__(__name__.__len__().__floordiv__(
__name__.__len__()).__add__(__name__.__len__().__floordiv__(__name__.__len__()
)).__add__(__name__.__len__().__floordiv__(__name__.__len__())).__add__(
__name__.__len__().__floordiv__(__name__.__len__())).__add__(__name__.__len__()
.__floordiv__(__name__.__len__())).__add__(__name__.__len__().__floordiv__(
__name__.__len__()))))).__add__(__chr__(__name__.__len__().__mul__(
__name__.__len__()).__add__(__name__.__len__()).__add__(__name__.__len__())
.__add__(__name__.__len__()).__add__(__name__.__len__()).__add__(
__name__.__len__()).__add__(__name__.__len__()).__add__(__name__.__len__()
.__floordiv__(__name__.__len__()).__add__(__name__.__len__().__floordiv__(
__name__.__len__())).__add__(__name__.__len__().__floordiv__(__name__.__len__()
)).__add__(__name__.__len__().__floordiv__(__name__.__len__()))))))(
__name__.__len__().__floordiv__(__name__.__len__()))

$ dunderhell foo.py | python3
1
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
