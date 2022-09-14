from typing import Any

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


def yaml_dump_to_file(data: Any, filepath: str, sort_keys: bool = False) -> None:
    """Dump provided data as YAML to specified filepath.

    Multiline strings are output with the literal block scalar style,
    preserving newlines.

    Default is not to sort dictionary keys, thus preserving
    order of insertion."""
    with open(filepath, "w") as f:
        yaml.dump(data, stream=f, indent=4, sort_keys=sort_keys)


def yaml_load_from_file(filepath: str) -> Any:
    """Simple wrapper function to load YAML from a specified file."""
    with open(filepath, "r") as f:
        return yaml.load(stream=f, Loader=Loader)


def yaml_load_from_string(strdata: str) -> Any:
    """Simple wrapper function to load YAML from a provided string."""
    return yaml.safe_load(strdata)