# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from pathlib import Path
import re

from ansys.systemcoupling.core.syc_version import (
    SycVersion,
    normalize_version,
)
from ansys.systemcoupling.core.util.logging import LOG

_IS_WINDOWS = os.name == "nt"

_INSTALL_ROOT_ENV = "AWP_ROOT"
_SC_ROOT_ENV = "SYSC_ROOT"

_SCRIPT_EXT = ".bat" if _IS_WINDOWS else ""
_SCRIPT_NAME = "systemcoupling" + _SCRIPT_EXT

_version_re = re.compile(r"\bv[0-9][0-9][0-9]\b")


def path_to_system_coupling(version: str | None = None) -> str:
    """Find the path to the System Coupling launch script.

    Parameters
    ----------
    version : str, optional
        Specific version string to locate. If None, System Coupling is located
        from the environment: first via ``SYSC_ROOT`` if set, otherwise by
        scanning ``AWP_ROOT*`` variables for the latest installed version. If no
        installation can be found, a ``RuntimeError`` is raised.

    Returns
    -------
    str
        Path to the System Coupling launch script.

    Raises
    ------
    RuntimeError
        If System Coupling installation cannot be located or script doesn't exist.
    """
    if version is not None:

        if os.environ.get(_SC_ROOT_ENV, None) is None:
            install_path = os.environ.get(_INSTALL_ROOT_ENV, None)
            if install_path:
                if m := _version_re.search(install_path):
                    implied_version = m.group(0)[1:]
                    if normalize_version(implied_version) != normalize_version(version):
                        raise RuntimeError(
                            f"The specified version string '{version}' is "
                            "inconsistent with the version implied by the "
                            f"environment variable '{_INSTALL_ROOT_ENV}'. "
                            "To avoid ambiguity, unset the variable or do not "
                            "provide the version, or adjust one or both to "
                            "make them consistent."
                        )

        if os.environ.get(_SC_ROOT_ENV, None) or os.environ.get(
            _INSTALL_ROOT_ENV, None
        ):
            LOG.warning(
                f"An explicit version, {version}, has been specified for "
                "launching System Coupling, while at least one of the "
                f"environment variables {_SC_ROOT_ENV} and {_INSTALL_ROOT_ENV} "
                "is set. Only the environment variable will be used to locate "
                "System Coupling but the version string might still be used "
                "to determine certain version-dependent behavior."
            )

    scroot = os.environ.get(_SC_ROOT_ENV, None)

    if not scroot:
        scroot = os.environ.get(_INSTALL_ROOT_ENV, None)
        if scroot is None:
            if version is None:
                # Look for the latest installed version
                for member in SycVersion:
                    env_var = member.awp_var
                    if env_var in os.environ:
                        potential_scroot = Path(os.environ[env_var])
                        potential_script_path = (
                            potential_scroot / "SystemCoupling" / "bin" / _SCRIPT_NAME
                        )
                        if potential_script_path.is_file():
                            scroot = str(potential_scroot)
                            break
            else:
                ver_maj, ver_min = normalize_version(version)
                scroot = os.environ.get(f"{_INSTALL_ROOT_ENV}{ver_maj}{ver_min}", None)
        if scroot:
            scroot = str(Path(scroot) / "SystemCoupling")

    if scroot is None:
        raise RuntimeError("Failed to locate System Coupling from environment.")

    script_path = Path(scroot) / "bin" / _SCRIPT_NAME

    if not script_path.is_file():
        raise RuntimeError(f"System Coupling script does not exist at {script_path}.")

    return str(script_path)
