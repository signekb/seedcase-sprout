from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from seedcase_sprout.constants import TEMPLATES_PATH
from seedcase_sprout.paths import PackagePath
from seedcase_sprout.properties import PackageProperties
from seedcase_sprout.write_file import write_file


def create_properties_script(path: Path | None = None) -> Path:
    """Creates the properties script with default values.

    Args:
        path: The path to the package folder. Defaults to the current working directory.

    Returns:
        The path to the newly created properties script.

    Examples:
        ```{python}
        import seedcase_sprout as sp

        sp.create_properties_script()
        ```
    """
    package_path = PackagePath(path)

    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH), autoescape=True)
    template = env.get_template("properties.py.jinja2")
    text = template.render(
        properties=PackageProperties.from_default(name=package_path.root().name)
    )

    script_path = package_path.properties_script()
    script_path.parent.mkdir(exist_ok=True)
    return write_file(text, script_path)
