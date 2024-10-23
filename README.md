<p align=center>
    <a href="https://sprout.seedcase-project.org/">
        <img src="_extensions/seedcase-project/seedcase-theme/logos/navbar-logo-seedcase-sprout.svg" height="150" alt="Sprout website"/>
    </a>
</p> 

## Grow structured and scalable data

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
return here to install Poetry and clone the repository.
<!--TODO add link above--> 

We use Poetry to manage
dependencies. If you haven't worked with Poetry before, you will find an
excellent introduction to it in the [Poetry
documentation](https://python-poetry.org/docs/). If you have worked with
it before you can find a quick guide to installing it below.

To install Poetry, run:

``` bash
pipx install poetry
```

Then, open a terminal so that the working directory is the root of this project (`seedcase-sprout/`) and run:


``` bash
just install-deps
```
