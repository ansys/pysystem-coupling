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

# Exclude Bandit check. Subprocess is needed to start the System Coupling.
import subprocess  # nosec B404
import threading
import time

import psutil

from ansys.systemcoupling.core.util.logging import LOG

# NB: Coverage disabled in this file as coverage is obtained in context of
#     GitHub CI where we are restricted to launching SyC in container mode.


class SycProcess:  # pragma: no cover
    def __init__(
        self,
        exe_path: str,
        grpc_args: list[str],
        grpc_args_fallback: list[str],
        working_dir: str,
        **kwargs,
    ):
        # self.__process = _start_system_coupling(
        #    exe_path, grpc_args, working_dir, **kwargs
        # )
        self.__starter = _ProcessStarter(
            exe_path, grpc_args, grpc_args_fallback, working_dir, **kwargs
        )

    def is_running(self) -> bool:
        return self.__starter.get_running_process() is not None

    def end(self):
        if not self.__starter:
            return
        process = self.__starter.get_running_process()
        if process and process.poll() is None:
            pid = process.pid
            try:
                LOG.info("Waiting for process to exit...")
                process.wait(5)
                LOG.info("...process exited.")
            except subprocess.TimeoutExpired:
                LOG.warning(
                    "Process still alive - forcible kill of "
                    "process and children will be attempted."
                )
                _kill_process_tree(pid, timeout=0.5)
        self.__starter = None


class _ProcessStarter:
    def __init__(
        self,
        exe_path: str,
        grpc_args: list[str],
        grpc_args_fallback: list[str],
        working_dir: str,
        **kwargs,
    ):
        self.__default_process: subprocess.Popen | None = None
        self.__fallback_process: subprocess.Popen | None = None

        self.__default_process = _start_system_coupling(
            exe_path, grpc_args, working_dir, **deepcopy(kwargs)
        )

        self.__fallback_thread = None
        if grpc_args_fallback:
            self.__fallback_thread = threading.Thread(
                target=self._fallback_starter,
                args=(exe_path, grpc_args_fallback, working_dir),
                kwargs=deepcopy(kwargs),
            )
            self.__fallback_thread.run()

    def get_running_process(self):
        # We should not normally need to access the process during the
        # period that the fallback thread runs, so the following is likely
        # to execute quickly.
        if self.__fallback_thread and self.__fallback_thread.is_alive():
            self.__fallback_thread.join()

        # Fallback thread is finished so no need for locks
        if self.__default_process.poll() is None:
            return self.__default_process
        if self.__fallback_process and self.__fallback_process.poll() is None:
            return self.__fallback_process

        return None

    def _fallback_starter(
        self,
        exe_path: str,
        grpc_args: list[str],
        working_dir: str,
        **kwargs,
    ):
        try_fallback = False
        for _ in range(10):
            time.sleep(0.1)
            if self.__default_process.poll() is not None:
                # Process has died within the first second or so
                try_fallback = True
                break

        if not try_fallback:
            return

        LOG.warning(
            "System Coupling process exited early. Trying "
            "relaunch with old-style command line arguments"
        )
        # Not accessed until thread joined so no locking needed
        self.__fallback_process = _start_system_coupling(
            exe_path, grpc_args, working_dir, **kwargs
        )


def _start_system_coupling(
    exe_path: str, grpc_args: list[str], working_dir: str, **kwargs
) -> subprocess.Popen:  # pragma: no cover

    env = deepcopy(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    env["SYC_GUI_SILENT_SERVER"] = "1"
    args = [
        exe_path,
        "-m",
        "cosimgui",
    ] + grpc_args

    # Extract arguments that we currently recognize - scope to extend in future
    nprocs = kwargs.pop("nprocs", None)
    if nprocs:
        args += ["--nprocs", str(nprocs)]

    sycnprocs = kwargs.pop("sycnprocs", None)
    if sycnprocs:
        args += ["--sycnprocs", str(sycnprocs)]

    # "extra_args" gives us the option to pass though any arguments that we want to.
    # However, it's user beware.
    args += kwargs.pop("extra_args", [])

    LOG.info(f"Starting System Coupling: {args[0]}")
    # Exclude Bandit check. No untrusted input to arguments.
    return subprocess.Popen(  # nosec B603
        args,
        env=env,
        cwd=working_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


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
