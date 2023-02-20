"""Version of ansys-systemcoupling-core library.

On the ``main`` branch, use 'dev0' to denote a development version.
For example:

version_info = 0, 1, 'dev0'

"""
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as metadata

    __version__ = metadata.version("ansys.systemcoupling.core")

else:
    from importlib_metadata import metadata as metadata_backport

    __version__ = metadata_backport("ansys.systemcoupling.core")["version"]
