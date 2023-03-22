"""Version of ansys-systemcoupling-core library.

On the ``main`` branch, use 'dev0' to denote a development version.
For example:

version_info = 0, 1, 'dev0'

"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

# Read from the pyproject.toml
# major, minor, patch
__version__ = importlib_metadata.version("ansys.systemcoupling.core")
