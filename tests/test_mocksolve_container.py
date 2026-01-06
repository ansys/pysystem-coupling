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

        solution = syc.solution
        solution.solve()
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
