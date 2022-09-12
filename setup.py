"""Template setup file."""
import codecs
from io import open as io_open
import os

from setuptools import find_namespace_packages, setup

# Use single source package versioning.  Follows:
# https://packaging.python.org/guides/single-sourcing-package-version/
#
# With this approach, we can include the version within the setup file
# while at the same time allowing the user to print the version from
# the module
HERE = os.path.abspath(os.path.dirname(__file__))
__version__ = None
version_file = os.path.join(
    HERE, "src", "ansys", "systemcoupling", "core", "_version.py"
)
with io_open(version_file, mode="r") as fd:
    exec(fd.read())


# Get the long description from the README file
# This is needed for the description on PyPI
def read(rel_path):
    with codecs.open(os.path.join(HERE, rel_path), "r") as fp:
        return fp.read()


with open(os.path.join(HERE, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

packages = [
    pkg
    for pkg in find_namespace_packages(where="src", include="ansys*")
    if pkg.startswith("ansys.systemcoupling.core") or pkg.startswith("ansys.api")
]
setup(
    name="ansys-systemcoupling-core",
    packages=packages,
    package_dir={"": "src"},
    version=__version__,
    description="Python API to System Coupling",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/pyansys/pysystem-coupling/",
    license="MIT",
    author="ANSYS, Inc.",  # this is required
    maintainer="Ian Boyd",  # you can change this
    # this email group works
    maintainer_email="ian.boyd@ansys.com",
    # Include all install requirements here.  If you have a longer
    # list, feel free just to create the list outside of ``setup`` and
    # add it here.
    install_requires=[
        "grpcio>=1.30.0",
        "grpcio-status>=1.30.0",
        "googleapis-common-protos>=1.50.0",
        "protobuf>=3.12.2,<4.0.0",
        "psutil>=5.7.0",
        "pyyaml",
    ],
    # Plan on supporting only the currently supported versions of Python
    python_requires=">=3.6",
    # Less than critical but helpful
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
