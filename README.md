# gitignoregh

<a href="https://github.com/sauljabin/gitignoregh/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/sauljabin/gitignoregh"></a>
<a href="https://github.com/sauljabin/gitignoregh/actions"><img alt="GitHub Actions" src="https://img.shields.io/github/checks-status/sauljabin/gitignoregh/main?label=tests"></a>
<a href="https://app.codecov.io/gh/sauljabin/gitignoregh"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/sauljabin/gitignoregh"></a>
<a href="https://pypi.org/project/gitignoregh"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/gitignoregh"></a>
<a href="https://pypi.org/project/gitignoregh"><img alt="Version" src="https://img.shields.io/pypi/v/gitignoregh"></a>
<a href="https://libraries.io/pypi/gitignoregh"><img alt="Dependencies" src="https://img.shields.io/librariesio/release/pypi/gitignoregh"></a>
<a href="https://pypi.org/project/gitignoregh"><img alt="Platform" src="https://img.shields.io/badge/platform-linux%20%7C%20osx-blueviolet"></a>

`gitignoregh` is a command line tool that generates a `.gitignore` file for a project from the [github gitignore templates repository](https://github.com/github/gitignore).

![https://raw.githubusercontent.com/sauljabin/gitignoregh/main/screenshots/options.png](https://raw.githubusercontent.com/sauljabin/gitignoregh/main/screenshots/options.png)

## Installation

Install with pip:
```sh
pip install gitignoregh
```

Upgrade with pip:
```sh
pip install --upgrade gitignoregh
```

## Usage

Help:
```sh
gitignoregh -h
```

Version:
```sh
gitignoregh --version
```

List all gitignore templates:
```sh
gitignoregh -l
```

Search gitignore templates files:
```sh
gitignoregh -s
```

Print a gitignore: 
```sh
gitignoregh -p
```

Reset github template repository:
```sh
gitignoregh --reset
```

Generate `.gitignore` file (accepts multiple arguments):
```sh
gitignoregh java gradle
```

## Development

Installing poetry:
```sh
pip install poetry
```

Installing development dependencies:
```sh
poetry install
```

Running unit tests:
```sh
poetry run python -m scripts.tests
```

Running multi version tests (`3.7`, `3.8`, `3.9`):

> Make sure you have `python3.7`, `python3.8`, `python3.9` aliases installed

```sh
poetry run python -m scripts.multi-version-tests
```

Applying code styles:
```sh
poetry run python -m scripts.styles
```

Running code analysis:
```sh
poetry run python -m scripts.analyze
```

Running code coverage:
```sh
poetry run python -m scripts.tests-coverage
```

Running cli using `poetry`:
```sh
poetry run gitignoregh
```
