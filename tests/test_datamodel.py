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
from io import StringIO

from dm_raw_metadata import cmd_metadata, dm_metadata

IS_FLAT_CLASSES = True
if IS_FLAT_CLASSES:
    import generated_data.setup_root as generated_testing_datamodel
else:
    import generated_data.testing_datamodel as generated_testing_datamodel

import pytest

from ansys.systemcoupling.core.adaptor.impl.root_source import get_root
from ansys.systemcoupling.core.adaptor.impl.static_info import process_cmd_data
from ansys.systemcoupling.core.adaptor.impl.syc_proxy_interface import SycProxyInterface
from state import StateForTesting


def _make_metadata():
    metadata = deepcopy(dm_metadata)
    cmd_meta = deepcopy(process_cmd_data(cmd_metadata, category="setup"))
    metadata["SystemCoupling"]["__commands"] = cmd_meta
    metadata["SystemCoupling"]["category_root"] = "setup_root"
    return metadata


class SycProxy(SycProxyInterface):
    def __init__(self, force_dynamic_datamodel=False):
        self.__force_dynamic_datamodel = force_dynamic_datamodel
        self.__state = StateForTesting()
        self.__metadata = None
        self.clear_last_cmd()

    def clear_last_cmd(self):
        self.last_cmd_path = None
        self.last_cmd_name = None
        self.last_cmd_args = None

    def get_static_info(self, category):
        info = self._get_metadata()
        if not self.__force_dynamic_datamodel:
            return info, "SystemCoupling"

        info = deepcopy(info)
        # info is structured as a single (top-level) element nested dict:
        #    {"root": {...nested data}}
        # We add extra entry to "root"s data to force a difference from the
        # data used to make the generated classes (which will be detected
        # via hash) and thereby force runtime-generated classes to be used.
        info[next(iter(info))]["__dummy__"] = None
        return info, "SystemCoupling"

    def get_version(self):
        return ""

    def set_state(self, path, state):
        self.__state.set_state(path, state)

    def get_state(self, path):
        return self.__state.get_state(path)

    def get_property_state(self, path, name):
        return self.__state.get_parameter(path, name)

    def delete(self, path):
        self.__state.delete_object(path)

    def create_named_object(self, path, name):
        self.__state.create(path, name)

    def get_object_names(self, path):
        state = self.__state.get_state(path)
        return list(state.keys())

    def get_property_options(self, path, name):
        return self.__state.get_parameter_options(path, name)

    def execute_cmd(self, *args, **kwargs):
        self.last_cmd_path = args[0]
        self.last_cmd_name = args[1]
        self.last_cmd_args = dict(**kwargs)
        return None

    def execute_injected_cmd(self, *args, **kwargs):
        return None

    def _get_metadata(self):
        if self.__metadata is None:
            self.__metadata = _make_metadata()
        return self.__metadata

    def set_state_parameter_options(self, path, name, options):
        # Testing support
        self.__state.set_parameter_options(path, name, options)


def _get_dm_and_proxy(force_dynamic: bool):
    proxy = SycProxy(force_dynamic_datamodel=force_dynamic)
    is_actually_dynamic = False

    def report(is_dynamic):
        nonlocal is_actually_dynamic
        is_actually_dynamic = is_dynamic

    root = get_root(
        proxy,
        category="setup",
        generated_module=generated_testing_datamodel,
        report_whether_dynamic_classes_created=report,
    )
    assert is_actually_dynamic == force_dynamic
    return (root, proxy)


@pytest.fixture(name="dm", params=("pre-generated", "dynamically-generated"))
def _dm(request):
    force_dynamic = request.param == "dynamically-generated"
    return _get_dm_and_proxy(force_dynamic)[0]


@pytest.fixture(name="dm_and_proxy", params=("pre-generated", "dynamically-generated"))
def _dm_and_proxy(request):
    force_dynamic = request.param == "dynamically-generated"
    return _get_dm_and_proxy(force_dynamic)


def test_empty(dm):
    assert dm.get_state() == {}


def test_create_library(dm):
    dm.library = {}
    assert dm.get_state() == {"library": {}}


def test_create_empty_expression(dm):
    dm.library.expression["bob"] = {}
    assert dm.get_state() == {"library": {"expression": {"bob": {}}}}


def test_create_empty_properties_expression(dm):
    dm.library.expression["bob"] = {
        "expression_name": None,
        "expression_string": None,
    }
    assert dm.get_state() == {
        "library": {
            "expression": {
                "bob": {
                    "expression_name": None,
                    "expression_string": None,
                }
            }
        }
    }


def test_query_unset_property(dm):
    dm.library.expression["bob"] = {}
    assert dm.library.expression["bob"].expression_name is None


def test_query_unknown_property(dm):
    dm.library.expression["bob"] = {}
    try:
        dm.library.expression["bob"].expression_unknown is None
        assert False, "Expected exception not thrown"
    except AttributeError:
        pass


def test_query_none_rhs_property(dm):
    dm.library.expression["bob"] = {
        "expression_name": None,
        "expression_string": None,
    }
    assert dm.library.expression["bob"].expression_name is None


def test_create_expression(dm):
    dm.library.expression["bob"] = {
        "expression_name": "expr",
        "expression_string": "2 * x",
    }
    assert dm.get_state() == {
        "library": {
            "expression": {
                "bob": {"expression_name": "expr", "expression_string": "2 * x"}
            }
        }
    }
    assert dm.library() == {
        "expression": {"bob": {"expression_name": "expr", "expression_string": "2 * x"}}
    }
    assert dm.library.expression["bob"]() == {
        "expression_name": "expr",
        "expression_string": "2 * x",
    }
    assert dm.library.expression["bob"]() == dm.library.expression["bob"].get_state()


def test_modify_expression(dm):
    dm.library.expression["bob"] = {
        "expression_name": "expr",
        "expression_string": "2 * x",
    }
    dm.library.expression["bob"].expression_string = "3 * x"
    assert dm.library.expression["bob"]() == {
        "expression_name": "expr",
        "expression_string": "3 * x",
    }
    assert dm.library.expression["bob"].expression_string == "3 * x"


def test_create_expr_direct(dm):
    # dm.library.expression["bob"].expression_name = "myExpr"
    dm.library.expression.create("bob")
    dm.library.expression["bob"].expression_name = "myExpr"
    dm.library.expression["bob"].expression_string = "a + b"
    assert dm.library.expression["bob"].expression_name == "myExpr"
    assert dm.library.expression["bob"].expression_string == "a + b"


def xxxtest_print_state(dm):
    dm.library.expression.create("bob")
    dm.library.expression["bob"].expression_name = "myExpr"
    stream = StringIO()
    dm.library.print_state(out=stream)
    # assert stream.getvalue() == "expression :\n  bob :\n    expression_name : myExpr"
    assert stream.getvalue() == "@"


def test_set_nested_state_get_by_path(dm):
    dm.set_state(
        {
            "library": {
                "expression": {
                    "bob": {"expression_name": "expr", "expression_string": "2 * x"}
                }
            }
        }
    )
    assert dm.library.expression["bob"].expression_string == "2 * x"


def test_syc_path(dm):
    dm.library.expression["bob"] = {}
    assert dm.library.expression["bob"]() == {}
    assert (
        dm.library.expression["bob"].syc_path
        == "/SystemCoupling/Library/Expression:bob"
    )


def test_invoke_solve(dm):
    dm.sycproxy.clear_last_cmd()
    dm.solve()
    assert dm.sycproxy.last_cmd_name == "Solve"
    assert dm.sycproxy.last_cmd_path == "SystemCoupling"
    assert dm.sycproxy.last_cmd_args == {}


def test_invoke_get_parameter_options(dm):
    dm.sycproxy.clear_last_cmd()
    dm.get_parameter_options(name="dummy")
    assert dm.sycproxy.last_cmd_name == "GetParameterOptions"
    assert dm.sycproxy.last_cmd_path == "SystemCoupling"
    assert dm.sycproxy.last_cmd_args == {
        "ObjectPath": "/SystemCoupling",
        "Name": "dummy",
    }


def test_solution_control_state(dm):
    # Not really testing anything new here but sanity
    # check in prep for path-based command
    dm.solution_control.duration_option = "EndTime"
    assert dm.solution_control.duration_option == "EndTime"


def test_invoke_get_parameter_options_on_path(dm):
    # Note that this is really testing mechanism of
    # path-based commands, something that we do not
    # exploit at the moment.
    # Actual property options querying has support in the core
    # so we do not expose this command directly.
    dm.sycproxy.clear_last_cmd()
    dm.solution_control.duration_option = "EndTime"
    dm.solution_control.get_parameter_options(name="duration_option")
    assert dm.sycproxy.last_cmd_name == "GetParameterOptions"
    assert dm.sycproxy.last_cmd_path == "SystemCoupling/SolutionControl"
    # TODO: Name is problematic as we should be transforming this to SyC name!
    assert dm.sycproxy.last_cmd_args == {
        "ObjectPath": "/SystemCoupling/SolutionControl",
        "Name": "duration_option",
    }


def test_get_property_options(dm_and_proxy):
    dm, proxy = dm_and_proxy
    proxy.set_state_parameter_options(
        "/SystemCoupling/SolutionControl",
        "DurationOption",
        ["Time", "Step", "EndTime", "PreviousTimestepSize"],
    )
    dm.solution_control.duration_option = "EndTime"
    options = dm.solution_control.get_property_options("duration_option")
    assert options == ["Time", "Step", "EndTime", "PreviousTimestepSize"]


def test_get_nested_state(dm):
    dm.set_state(
        {
            "library": {
                "expression": {
                    "bob": {"expression_name": "expr", "expression_string": "2 * x"}
                }
            }
        }
    )
    assert dm() == {
        "library": {
            "expression": {
                "bob": {"expression_name": "expr", "expression_string": "2 * x"}
            }
        }
    }


def test_invoke_partition_particpants(dm):
    dm.sycproxy.clear_last_cmd()
    dm.partition_participants(
        machine_list=[{"machine-name": "host1", "core-count": 10}],
        names_and_fractions=[("PART-1", 0.5), ("PART-2", 0.7)],
    )
    assert dm.sycproxy.last_cmd_name == "PartitionParticipants"
    assert dm.sycproxy.last_cmd_path == "SystemCoupling"
    assert dm.sycproxy.last_cmd_args == {
        "MachineList": [{"machine-name": "host1", "core-count": 10}],
        "NamesAndFractions": [("PART-1", 0.5), ("PART-2", 0.7)],
    }


def test_state_order(dm):
    dm.output_control.set_state(
        {
            "results": {
                "option": "ProgramControlled",
                "type": {"option": "EnsightGold"},
                "include_instances": "ProgramControlled",
            },
            "generate_csv_chart_output": False,
            "write_initial_snapshot": True,
            "option": "LastStep",
        }
    )

    str_io = StringIO()
    dm.print_state(out=str_io)
    expected = """
output_control :
  option : LastStep
  generate_csv_chart_output : False
  write_initial_snapshot : True
  results :
    option : ProgramControlled
    include_instances : ProgramControlled
    type :
      option : EnsightGold
"""
    actual = str_io.getvalue()
    assert actual == expected
