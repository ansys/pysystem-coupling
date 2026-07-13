# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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
import subprocess  # nosec B404
import time

import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core.charts.plotter import Plotter
from ansys.systemcoupling.core.syc_version import compare_versions


def test_partlib_cosim_volume_simple(image_tag_env) -> None:
    """Equivalent of SyC test partlib-cosim-volume-simple.

    One of the simplest examples using a mock solver.
    """

    with pysystemcoupling.launch_container() as syc:
        assert syc.ping()

        setup = syc.setup

        if compare_versions(syc.version, "24.2") > 0:
            p1 = setup.add_participant(
                python_script=_get_mocksolve_executable(get_python_script=True),
                additional_arguments="--p1",
            )
            p2 = setup.add_participant(
                python_script=_get_mocksolve_executable(get_python_script=True),
                additional_arguments="--p2",
            )
        else:
            p1 = setup.add_participant(
                executable=_get_mocksolve_executable(), additional_arguments="--p1"
            )
            p2 = setup.add_participant(
                executable=_get_mocksolve_executable(), additional_arguments="--p2"
            )

        interface = setup.add_interface(
            side_one_participant=p1,
            side_one_regions=["volume"],
            side_two_participant=p2,
            side_two_regions=["volume"],
        )

        # As of 24.1 there are some expected warnings, so filter
        # to Errors only
        messages = [
            msg for msg in setup.get_status_messages() if msg["level"] == "Error"
        ]

        assert len(messages) == 1, print(messages)
        assert messages[0]["path"] == 'coupling_interface["Interface-1"]'
        assert messages[0]["message"].startswith(
            "No data transfers exist on Interface-1"
        )

        dt1 = setup.add_data_transfer(
            interface=interface,
            target_side="Two",
            side_one_variable="p1_to_p2",
            side_two_variable="p1_to_p2",
        )

        messages = [
            msg for msg in setup.get_status_messages() if msg["level"] == "Error"
        ]
        assert len(messages) == 0

        # At 24.1 there is a new Warning about unused input variables that we don't worry about here
        messages = [
            msg for msg in setup.get_status_messages() if msg["level"] == "Information"
        ]
        if compare_versions(syc.version, "25.1") > 0:
            assert len(messages) == 3
        else:
            assert len(messages) == 1
        assert messages[0]["path"] == "analysis_control"
        assert messages[0]["message"].startswith(
            "The data transfers define an optimized one-way workflow."
        )

        dt2 = setup.add_data_transfer(
            interface=interface,
            target_side="One",
            side_one_variable="p2_to_p1",
            side_two_variable="p2_to_p1",
        )

        setup.output_control.generate_csv_chart_output = True

        output_handler = _OutputHandler()
        syc.start_output(handle_output=output_handler.on_line)

        _run_license_network_diagnostics()

        # assert False, "Force failure to capture output for debugging"
        solution = syc.solution
        try:
            solution.solve()
        except Exception as e:
            print(f"An error occurred during solution: {e}")
            print("\n\n**OUTPUT LINES** captured during the solution:")
            time.sleep(3)  # Give time for any remaining output to be captured
            for line in output_handler.lines:
                print(line)
            print("<< End of captured output >>")
            raise
        plotter: Plotter = solution.show_plot()
        time.sleep(5)
        plotter.close()

        syc._native_api.PrintState(ObjectPath="/SystemCoupling/OutputControl")
        syc.end_output()

        assert any(
            "        Shut Down         " in line for line in output_handler.lines
        )


def _get_mocksolve_executable(get_python_script: bool = False):
    # System Coupling is packaged under /syc in the image

    # Note that we don't use os.path.join here because it
    # would give us a Windows path on Windows and we always
    # want a unix-style path.

    suffix = "py" if get_python_script else "sh"

    return "/" + "/".join(
        (
            "syc",
            "SystemCoupling",
            "Tests",
            "SystemCouplingParticipant",
            "TestSolvers",
            "Python",
            f"VolumeCosimTester.{suffix}",
        )
    )


class _OutputHandler:
    def __init__(self):
        self.lines = []

    def on_line(self, line):
        self.lines.append(line)


def _run_license_network_diagnostics() -> None:
    print("Running pre-solve license network diagnostics...")

    license_spec = os.getenv("ANSYSLMD_LICENSE_FILE", "")
    if "@" not in license_spec:
        print(
            "Skipping diagnostics: ANSYSLMD_LICENSE_FILE is missing or "
            "not in '<port>@<server>' format."
        )
        return

    license_server = license_spec.split("@", 1)[1].split(",", 1)[0].strip()
    if not license_server:
        print("Skipping diagnostics: extracted license server name is empty.")
        return

    container_id = _find_syc_container_id()
    if not container_id:
        print(
            "Skipping diagnostics: could not locate running System Coupling container."
        )
        return

    print(f"Using System Coupling container: {container_id}")
    print(f"Using license server: {license_server}")

    install_nc_cmd = ["docker", "exec", container_id, "yum", "install", "-y", "nc"]
    install_nc_result = _run_and_log_command(install_nc_cmd)
    if install_nc_result.returncode != 0:
        print("Initial nc installation failed. Trying nmap-ncat package...")
        install_nmap_ncat_cmd = [
            "docker",
            "exec",
            container_id,
            "yum",
            "install",
            "-y",
            "nmap-ncat",
        ]
        _run_and_log_command(install_nmap_ncat_cmd)

    for port in (34583, 1055):
        nc_cmd = [
            "docker",
            "exec",
            container_id,
            "nc",
            "-zv",
            license_server,
            str(port),
        ]
        _run_and_log_command(nc_cmd)


def _find_syc_container_id() -> str | None:
    image_tag = os.getenv("SYC_IMAGE_TAG", "latest")
    image_name = f"ghcr.io/ansys/pysystem-coupling:{image_tag}"
    cmd = [
        "docker",
        "ps",
        "--filter",
        f"ancestor={image_name}",
        "--format",
        "{{.ID}}",
    ]
    result = _run_and_log_command(cmd)
    if result.returncode != 0:
        return None

    ids = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not ids:
        return None
    if len(ids) > 1:
        print(f"Multiple matching containers found. Using first: {ids[0]}")
    return ids[0]


def _run_and_log_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)  # nosec B603
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())
    print(f"[returncode={result.returncode}]")
    return result
