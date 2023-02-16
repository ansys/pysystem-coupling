import re


def _splitCamelCase(name):
    return re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", name)).split()


def to_python_name(name):
    """Convert 'MyPropertyName' to Pythonic 'my_property_name'."""

    components = _splitCamelCase(name)
    return "_".join(comp.lower() for comp in components)
