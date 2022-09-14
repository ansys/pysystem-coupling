#
# Copyright 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#

from copy import deepcopy
import os
import platform
import subprocess

import psutil

from ansys.systemcoupling.core.util.logging import LOG

_isWindows = any(platform.win32_ver())

_CURR_VER = "231"
_INSTALL_ROOT_ENV = "AWP_ROOT"
_INSTALL_ROOT_VER_ENV = _INSTALL_ROOT_ENV + _CURR_VER
_SC_ROOT_ENV = "SYSC_ROOT"

_SCRIPT_EXT = ".bat" if _isWindows else ""
_SCRIPT_NAME = "systemcoupling" + _SCRIPT_EXT


class SycProcess:
    def __init__(self, host, port, working_dir, log_level=1):
        self.__process = _start_system_coupling(host, port, working_dir, log_level)

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


def _start_system_coupling(host, port, working_dir, log_level):
    env = deepcopy(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    env["SYC_GUI_SILENT_SERVER"] = "1"
    args = [_path_to_system_coupling(), "-m", "cosimgui", f"--grpcport={host}:{port}"]
    if log_level:
        args += ["-l", str(log_level)]
    LOG.info(f"Starting System Coupling: {args[0]}")
    return subprocess.Popen(
        args,
        env=env,
        cwd=working_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


def _path_to_system_coupling():
    scroot = os.environ.get(_SC_ROOT_ENV, None)

    if not scroot:
        scroot = os.environ.get(_INSTALL_ROOT_ENV, None)
        if scroot is None:
            scroot = os.environ.get(_INSTALL_ROOT_VER_ENV, None)
        if scroot:
            scroot = os.path.join(scroot, "SystemCoupling")

    if scroot is None:
        raise RuntimeError("Failed to locate SystemCoupling from environment.")

    script_path = os.path.join(scroot, "bin", _SCRIPT_NAME)

    if not os.path.isfile(script_path):
        raise RuntimeError(f"System coupling script does not exist at {script_path}")

    return script_path


def _kill_process_tree(pid, timeout):
    """Kill a process tree rooted at process `pid`."""
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
