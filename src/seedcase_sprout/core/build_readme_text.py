from datetime import datetime
from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from seedcase_sprout.core.properties import (
    LicenseProperties,
    PackageProperties,
)

TEMPLATES_PATH: Path = files("seedcase_sprout.core").joinpath("templates")


def build_readme_text(properties: PackageProperties) -> str:
    """Creates a string containing the README text.

    Args:
      properties: An object containing the package and resource properties.

    Returns:
      A string with the README text based on the properties.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    env.filters["join_names"] = join_names
    env.filters["format_date"] = format_date
    env.filters["inline_code"] = inline_code
    env.filters["format_link"] = format_link
    template = env.get_template("README.jinja2")
    return template.render(properties=properties)


def join_names(licenses: list[LicenseProperties] | None) -> str:
    """Joins license names into a comma-separated list.

    Args:
        licenses: The licenses.

    Returns:
        A comma-separated list of names.
    """
    return ", ".join(license.name for license in licenses) if licenses else "N/A"


def format_date(created: str | None) -> str:
    """Transforms ISO date stamp to human-readable format.

    Args:
        created: The ISO date stamp.

    Returns:
        The date in a human-readable format.
    """
    return (
        datetime.fromisoformat(created).strftime("%d %B %Y, %H:%M")
        if created
        else "N/A"
    )


def inline_code(value: str | None) -> str:
    """Adds inline code formatting to the input.

    Args:
        value: The value to format as inline code.

    Returns:
        The value formatted as inline code.
    """
    return f"`{value}`" if value else "N/A"


def format_link(url: str | None, title: str = "See more") -> str:
    """Formats a URL as a markdown link.

    Args:
        url: The URL to format.
        title: The title to show for the link. Defaults to "See more".

    Returns:
        A markdown link using the URL and the title.
    """
    return f"[{title}]({url})" if url else "N/A"
