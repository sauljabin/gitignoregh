# gitignoregh

<a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/-python-success?logo=python&logoColor=white"></a>
<a href="https://github.com/sauljabin/gitignoregh"><img alt="GitHub" src="https://img.shields.io/badge/status-active-brightgreen"></a>
<a href="https://github.com/sauljabin/gitignoregh/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/sauljabin/gitignoregh"></a>
<a href="https://github.com/sauljabin/gitignoregh/actions"><img alt="GitHub Actions" src="https://img.shields.io/github/actions/workflow/status/sauljabin/gitignoregh/main.yml?branch=main"></a>
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
pipx install gitignoregh
```

Upgrade with pip:
```sh
pipx upgrade gitignoregh
```

## Usage

> Alias: `gigh`

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
pipx install poetry
```

Installing development dependencies:
```sh
poetry install
```

Running unit tests:
```sh
poetry run python -m scripts.tests
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

## Release a new version

> Check https://python-poetry.org/docs/cli/#version

```shell
poetry version <major|minor|patch>
git add -A
git commit -m "new version: $(poetry version -s)"
git tag $(poetry version -s)
git push origin main
git push --tags
```