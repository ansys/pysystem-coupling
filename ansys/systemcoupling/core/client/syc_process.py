#
# Copyright 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#

import os
import platform
import subprocess
import time

_isWindows = any(platform.win32_ver())

_INSTALL_ROOT = "AWP_ROOT222"
_SC_ROOT_ENV = "SYSC_ROOT"

_SCRIPT_EXT = '.bat' if _isWindows else ''
_SCRIPT_NAME = 'systemcoupling' + _SCRIPT_EXT

class SycProcess:
    def __init__(self, host, port, working_dir, log_level=1):
        self.__process = _start_system_coupling(
            host, port, working_dir, log_level
        )

    def end(self):
        if self.__process and self.__process.poll() is None:
            try:
                print("wait for process to exit...")
                self.__process.wait(5)
                print("...done")
            except subprocess.TimeoutExpired:
                print("process still alive - killing it...")
                self.__process.kill()
                time.sleep(0.5)
                ret_code = self.__process.poll()
                print("process exit code: ",
                      "Unknown - still alive?" if ret_code is None
                      else ret_code)
            self.__process = None


def _start_system_coupling(host, port, working_dir, log_level):
    from copy import deepcopy
    env = deepcopy(os.environ)
    env['PYTHONUNBUFFERED'] = '1'
    env['SYC_GUI_SILENT_SERVER'] = '1'
    args = [_path_to_system_coupling(), '-m', 'cosimtest', f'--grpcport={host}:{port}']
    if log_level:
        args += ['-l', str(log_level)]
    print("Starting System Coupling: ", args[0])
    return subprocess.Popen(args,
                            env=env,
                            cwd=working_dir,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT
                            )


def _path_to_system_coupling():
    scroot = os.environ.get(_SC_ROOT_ENV, None)

    if not scroot:
        scroot = os.environ.get(_INSTALL_ROOT, None)
        if scroot:
            scroot = os.path.join(scroot, 'SystemCoupling')

    if scroot is None:
        raise RuntimeError("Failed to locate SystemCoupling from environment.")

    script_path = os.path.join(scroot, 'bin', _SCRIPT_NAME)

    if not os.path.isfile(script_path):
        raise RuntimeError(f"System coupling script does not exist at {script_path}")

    return script_path

