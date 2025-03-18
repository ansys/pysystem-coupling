# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

from copy import deepcopy
import os
import platform
import subprocess

import psutil

from ansys.systemcoupling.core.syc_version import SYC_VERSION_CONCAT, normalize_version
from ansys.systemcoupling.core.util.logging import LOG

_isWindows = any(platform.win32_ver())

_CURR_VER = SYC_VERSION_CONCAT
_INSTALL_ROOT_ENV = "AWP_ROOT"
_INSTALL_ROOT_VER_ENV = _INSTALL_ROOT_ENV + _CURR_VER
_SC_ROOT_ENV = "SYSC_ROOT"

_SCRIPT_EXT = ".bat" if _isWindows else ""
_SCRIPT_NAME = "systemcoupling" + _SCRIPT_EXT

# NB: Coverage disabled in this file as coverage is obtained in context of
#     GitHub CI where we are restricted to launching SyC in container mode.


class SycProcess:  # pragma: no cover
    def __init__(self, host, port, working_dir, version=None, **kwargs):
        self.__process = _start_system_coupling(
            host, port, working_dir, version, **kwargs
        )

    @property
    def path_to_system_coupling(self) -> str:
        return self.__process.args[0]

    def end(self):
        if self.__process and self.__process.poll() is None:
            pid = self.__process.pid
            try:
                LOG.info("Waiting for process to exit...")
                self.__process.wait(5)
                LOG.info("...process exited.")
            except subprocess.TimeoutExpired:
                LOG.warning(
                    "Process still alive - forcible kill of "
                    "process and children will be attempted."
                )
                _kill_process_tree(pid, timeout=0.5)
            self.__process = None


def _start_system_coupling(
    host, port, working_dir, version, **kwargs
):  # pragma: no cover
    env = deepcopy(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    env["SYC_GUI_SILENT_SERVER"] = "1"
    args = [
        _path_to_system_coupling(version),
        "-m",
        "cosimgui",
        f"--grpcport={host}:{port}",
    ]

    # Extract arguments that we currently recognize - scope to extend in future
    nprocs = kwargs.pop("nprocs", None)
    if nprocs:
        args += ["--nprocs", str(nprocs)]

    sycnprocs = kwargs.pop("sycnprocs", None)
    if sycnprocs:
        args += ["--sycnprocs", str(sycnprocs)]

    # "extra_args" gives us the option to pass though any arguments that we want to.
    # However, it's user beware.
    extra_args = kwargs.pop("extra_args", [])
    if extra_args:
        args += extra_args

    LOG.info(f"Starting System Coupling: {args[0]}")
    return subprocess.Popen(
        args,
        env=env,
        cwd=working_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


def _path_to_system_coupling(version):  # pragma: no cover
    if version is not None:
        if os.environ.get(_SC_ROOT_ENV, None) or os.environ.get(
            _INSTALL_ROOT_ENV, None
        ):
            raise ValueError(
                f"An explicit version, {version}, has been specified for "
                "launching System Coupling, while at least one of the "
                f"environment variables {_SC_ROOT_ENV} and {_INSTALL_ROOT_ENV} "
                "is set. To remove the ambiguity, either unset the environment "
                "variable(s) or do not provide the version argument."
            )

    scroot = os.environ.get(_SC_ROOT_ENV, None)

    if not scroot:
        scroot = os.environ.get(_INSTALL_ROOT_ENV, None)
        if scroot is None:
            if version is None:
                scroot = os.environ.get(_INSTALL_ROOT_VER_ENV, None)
            else:
                ver_maj, ver_min = normalize_version(version)
                scroot = os.environ.get(f"{_INSTALL_ROOT_ENV}{ver_maj}{ver_min}", None)
        if scroot:
            scroot = os.path.join(scroot, "SystemCoupling")

    if scroot is None:
        raise RuntimeError("Failed to locate System Coupling from environment.")

    script_path = os.path.join(scroot, "bin", _SCRIPT_NAME)

    if not os.path.isfile(script_path):
        raise RuntimeError(f"System Coupling script does not exist at {script_path}.")

    return script_path


def _kill_process_tree(pid, timeout):  # pragma: no cover
    """Kill a process tree rooted at process ``pid``."""
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    children.append(parent)
    for p in children:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=timeout)

    # On Windows, terminate == kill so this probably won't have much effect.
    for p in alive:
        p.kill()
