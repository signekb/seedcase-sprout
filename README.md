<p align=center>
    <a href="https://sprout.seedcase-project.org/">
        <img src="https://raw.githubusercontent.com/seedcase-project/seedcase-sprout/main/_extensions/seedcase-project/seedcase-theme/logos/navbar-logo-seedcase-sprout.svg" height="150" alt="Link to Sprout website"/>
    </a>
</p>

## Grow structured and scalable data

[![PyPI Version](https://img.shields.io/pypi/v/seedcase-sprout)](https://pypi.org/project/seedcase-sprout/)
[![GitHub Release](https://img.shields.io/github/v/release/seedcase-project/seedcase-sprout)](https://github.com/seedcase-project/seedcase-sprout/releases/latest)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/seedcase-project/seedcase-sprout/badge)](https://scorecard.dev/viewer/?uri=github.com/seedcase-project/seedcase-sprout)
[![Build package](https://github.com/seedcase-project/seedcase-sprout/actions/workflows/build-package.yml/badge.svg)](https://github.com/seedcase-project/seedcase-sprout/actions/workflows/build-package.yml)
[![Build documentation](https://github.com/seedcase-project/seedcase-sprout/actions/workflows/build-website.yml/badge.svg)](https://github.com/seedcase-project/seedcase-sprout/actions/workflows/build-website.yml)
[![CodeQL](https://github.com/seedcase-project/seedcase-sprout/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/seedcase-project/seedcase-sprout/actions/workflows/github-code-scanning/codeql)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/seedcase-project/seedcase-sprout/main.svg)](https://results.pre-commit.ci/latest/github/seedcase-project/seedcase-sprout/main)
[![code coverage](https://raw.githubusercontent.com/seedcase-project/seedcase-sprout/coverage/coverage.svg?raw=true)](https://htmlpreview.github.io/?https://raw.githubusercontent.com/seedcase-project/seedcase-sprout/coverage/index.html)
[![lifecycle](https://lifecycle.r-lib.org/articles/figures/lifecycle-experimental.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)

Sprout is a component of the Seedcase framework that aims to take data
created or collected for research studies and "grow" it in a structured
way using modern data engineering best practices.

Sprout is the backbone of the Seedcase family; this is where data is
uploaded, described, and stored.

Seedcase Sprout is designed to receive data files and guide the user
through adding metadata to the research data that the user of Seedcase
would like to store in a responsible way.

## Install

Seedcase Sprout can be installed in two ways. The first is to install it
as a user, and the second is to install it as a contributor.

To install it as a user, see our [Installation Guide](https://sprout.seedcase-project.org/docs/guide/installation).

### Installation for contributors

If you would like to contribute, please
read the [contribution guidelines]() first. Then
return here to install uv and clone the repository.
<!--TODO add link above-->

We use uv to manage
dependencies. If you haven't worked with uv before, you will find an
excellent introduction to it in the [uv
documentation](https://docs.astral.sh/uv/). If you have worked with
it before you can find a quick guide to installing it below.

To install uv, run:

``` bash
pipx install uv
```

Then, open a terminal so that the working directory is the root of this project (`seedcase-sprout/`) and run:

``` bash
just install-deps
```
