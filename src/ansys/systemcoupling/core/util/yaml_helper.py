import io
from typing import Any, TextIO

import yaml

"""Simple utility wrappers for common YAML functionality."""

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Define and add a "representer" so that we get the "|" format
# for multiline strings.


def _str_presenter(dumper, data):
    # If multiline string set block format
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, _str_presenter)


def yaml_dump_to_file(
    data: Any, filepath: str, sort_keys: bool = False
) -> None:  # pragma: no cover
    """Save data to a YAML file in the filepath specified.

    Multiline strings are output with the literal block scalar style,
    preserving new lines.

    The default is not to sort dictionary keys, thus preserving
    the order of insertion."""
    with open(filepath, "w") as f:
        _yaml_dump_to_stream(data, f, sort_keys)


def yaml_dump_to_string(data: Any, sort_keys: bool = False) -> str:
    """Save data to a YAML file in the filepath specified and return this
    file's content as a string."""
    stream = io.StringIO()
    _yaml_dump_to_stream(data, stream, sort_keys)
    return stream.getvalue()


def _yaml_dump_to_stream(data: Any, stream: TextIO, sort_keys: bool) -> None:
    yaml.dump(data, stream=stream, indent=4, sort_keys=sort_keys)


def yaml_load_from_file(filepath: str) -> Any:  # pragma: no cover
    """Load the content in a specified YAML file."""
    with open(filepath, "r") as f:
        return yaml.load(stream=f, Loader=Loader)


def yaml_load_from_string(strdata: str) -> Any:
    """Load the YAML content from a provided string."""
    return yaml.safe_load(strdata)
