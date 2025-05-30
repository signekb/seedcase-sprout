from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import patch
from uuid import UUID
from zoneinfo import ZoneInfo

import time_machine

from seedcase_sprout.create_properties_template import create_properties_template
from seedcase_sprout.paths import PackagePath
from seedcase_sprout.properties import LicenseProperties, PackageProperties


@patch("seedcase_sprout.properties.uuid4", return_value=UUID(int=1))
@time_machine.travel(datetime(2024, 5, 14, 5, 0, 1, tzinfo=ZoneInfo("UTC")), tick=False)
def test_creates_template_with_default_values(mock_uuid, tmp_cwd):
    """Should create a template with default values."""
    template_path = create_properties_template()

    assert template_path == PackagePath().properties_template()
    properties = load_properties(template_path)
    assert properties == PackageProperties(
        name=tmp_cwd.name,
        title="",
        description="",
        licenses=[LicenseProperties(name="")],
        id=str(mock_uuid()),
        version="0.1.0",
        created="2024-05-14T05:00:01+00:00",
    )


def test_works_with_custom_path(tmp_path):
    """Should work with a custom path."""
    template_path = create_properties_template(tmp_path)

    assert template_path == PackagePath(tmp_path).properties_template()
    assert load_properties(template_path).name == tmp_path.name


def load_properties(path: Path) -> PackageProperties:
    """Loads `properties` object from file."""
    spec = spec_from_file_location("test_module", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.properties
