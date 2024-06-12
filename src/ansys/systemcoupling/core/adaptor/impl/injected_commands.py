# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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
from typing import Callable, Dict, Protocol

from ansys.systemcoupling.core.native_api import NativeApi
from ansys.systemcoupling.core.participant.manager import ParticipantManager
from ansys.systemcoupling.core.participant.mapdl import MapdlSystemCouplingInterface
from ansys.systemcoupling.core.util.yaml_helper import yaml_load_from_string

from .get_status_messages import get_status_messages
from .types import Container


# We cannot import Session directly, so define a protocol for typing
# We mainly use it as a means of accessing the "API roots".
class SessionProtocol(Protocol):
    case: Container
    setup: Container
    solution: Container
    _native_api: NativeApi

    def download_file(
        self, file_name: str, local_file_dir: str = ".", overwrite: bool = False
    ) -> None: ...


def get_injected_cmd_map(
    category: str,
    session: SessionProtocol,
    part_mgr: ParticipantManager,
    rpc,
) -> Dict[str, Callable]:
    """Get a dictionary mapping names to functions that implement injected commands
    for the specified API category.

    Whereas the set of commands that exists by default on the API represents a relatively
    mechanical exposure of native System Coupling commands to PySystemCoupling, the
    "injected commands" that are returned from here are either *additional* commands
    that have no counterpart in System Coupling, or are *overrides* to existing commands
    that provide modified or extended behavior.

    """
    ret = {}

    if category == "setup":
        # ``get_injected_cmd_map`` needs to be called during initialisation, where
        # the session API roots are not necessarily available yet. We therefore
        # defer their access via the lambda.
        get_setup_root_object = lambda: session.setup
        ret = {
            "get_setup_summary": lambda **kwargs: rpc.GetSetupSummary(**kwargs),
            "get_status_messages": lambda **kwargs: get_status_messages(
                rpc, get_setup_root_object(), **kwargs
            ),
            "add_participant": lambda **kwargs: _wrap_add_participant(
                get_setup_root_object(), part_mgr, **kwargs
            ),
        }

    if category == "solution":
        get_solution_root_object = lambda: session.solution
        get_setup_root_object = lambda: session.setup
        ret = {
            "solve": lambda **kwargs: _wrap_solve(
                get_solution_root_object(), part_mgr, **kwargs
            ),
            "interrupt": lambda **kwargs: rpc.interrupt(**kwargs),
            "abort": lambda **kwargs: rpc.abort(**kwargs),
        }

    if category == "case":
        get_case_root_object = lambda: session.case
        ret = {
            "clear_state": lambda **kwargs: _wrap_clear_state(
                get_case_root_object(), part_mgr, **kwargs
            )
        }

    return ret


def _wrap_add_participant(
    setup: Container, part_mgr: ParticipantManager, **kwargs
) -> str:
    if session := kwargs.get("participant_session", None):
        if len(kwargs) != 1:
            raise RuntimeError(
                "If a 'participant_session' argument is passed to "
                "'add_participant', it must be the only argument."
            )
        if part_mgr is None:
            raise RuntimeError("Internal error: participant manager is not available.")

        # special handling for mapdl session
        if "ansys.mapdl.core.mapdl_grpc.MapdlGrpc" in str(type(session)):
            return part_mgr.add_participant(
                participant_session=MapdlSystemCouplingInterface(session)
            )

        if not hasattr(session, "system_coupling"):
            raise RuntimeError(
                "The 'participant_session' parameter does not provide a "
                "'system_coupling' attribute and therefore cannot support this "
                "form of 'add_participant'."
            )
        return part_mgr.add_participant(participant_session=session.system_coupling)

    if input_file := kwargs.get("input_file", None):
        part_mgr.upload_file(input_file)

    return setup._add_participant(**kwargs)


def _wrap_clear_state(case: Container, part_mgr: ParticipantManager, **kwargs) -> None:
    part_mgr.clear()
    case._clear_state(**kwargs)


def _wrap_solve(solution: Container, part_mgr: ParticipantManager) -> None:
    if part_mgr is None:
        solution._solve()
    else:
        part_mgr.solve()


def get_injected_cmd_data() -> list:
    """Gets a list of injected command data in the right form to insert
    at a convenient point in the current processing.

    Because the data returned data is always a new copy, it can be manipulated at will.
    """
    if get_injected_cmd_data.data is None:
        data = yaml_load_from_string(_cmd_yaml)
        get_injected_cmd_data.data = data
    return deepcopy(get_injected_cmd_data.data)


get_injected_cmd_data.data = None


# Metadata handling is a bit of a mess at the moment as it relies on blending together
# data from multiple sources into opaque dictionaries. The data here is a further
# source that represents locally defined *commands* that are to be injected into the
# generated API so that they are presented in a uniform manner (the same as generated).
#
# The YAML format here is equivalent to the format of the command data already being
# obtained by blending the result of two queries to System Coupling. This format is
# therefore amenable to simply being merged into that data.
# (TODO: investigate rationalization of raw queried data and look at introduction of
# dataclasses and more on this side.)

_cmd_yaml = """
-   name: Solve
    pyname: solve
    isInjected: true
    pysyc_internal_name: _solve
-   name: AddParticipant
    pyname: add_participant
    isInjected: true
    pysyc_internal_name: _add_participant
    doc_prefix: |-
        This command operates in one of two modes, depending on how it is called.
        *Either* a single argument, ``participant_session``, should be provided, *or* some
        combination of the other optional arguments not including ``participant_session``
        should be provided.

        In the ``participant_session`` mode, the session object is queried to
        extract the information needed to define a new ``coupling_participant``
        object in the setup datamodel. A reference to the session is also retained,
        and this will play a further role if ``solve`` is called later. In that case,
        the participant solver will be driven from the Python environment in which the
        participant and PySystemCoupling sessions are active and System Coupling will
        regard the participant solver as "externally managed" (see the `execution_control`
        settings in `coupling_participant` for details of this mode).

        .. note::
            The ``participant_session`` mode currently has limited support in the
            broader Ansys Python ecosystem - at present, only PyFluent supports
            the API required of the session object and product versions of Fluent and
            System Coupling need to be at least 24.1. This capability should be
            regarded as *Beta* as it may be subject to revision when extended to other
            products.

        The remainder of the documentation describes the more usual non-session mode.


    essentialArgNames_extra: []
    optionalArgNames_extra:
    - participant_session
    args_extra:
    - #!!python/tuple
        - participant_session
        -   pyname: participant_session
            Type: <class 'object'>
            type: ParticipantSession
            doc: |-
                Participant session object conforming to the ``ParticipantProtocol`` protocol class.
-   name: interrupt
    pyname: interrupt
    exposure: solution
    isInjected: true
    isQuery: false
    isInternal: false
    retType: <class 'NoneType'>
    doc: |-
        Interrupts a solve in progress.

        See also ``abort``. The difference between an interrupted and
        aborted solve is that an interrupted solve can be resumed.
    essentialArgNames: []
    optionalArgNames:
    - reason_msg
    defaults:
    - ""
    args:
    - #!!python/tuple
        - reason_msg
        -   pyname: reason_msg
            Type: <class 'str'>
            type: String
            doc:  |-
               Text to describe the reason for the interrupt.

               This might be used for such purposes as providing
               additional annotation in transcript output.
-   name: abort
    pyname: abort
    exposure: solution
    isInjected: true
    isQuery: false
    isInternal: false
    retType: <class 'NoneType'>
    doc: |-
        Aborts a solve in progress.

        See also ``interrupt``. In contrast to an interrupted solve,
        an aborted solve cannot be resumed.
    essentialArgNames: []
    optionalArgNames:
    - reason_msg
    defaults:
    - ""
    args:
    - #!!python/tuple
        - reason_msg
        -   pyname: reason_msg
            Type: <class 'str'>
            type: String
            doc:  |-
               Text to describe the reason for the abort.

               This might be used for such purposes as providing
               additional annotation in transcript output.
-   name: GetSetupSummary
    pyname: get_setup_summary
    exposure: setup
    isInjected: true
    isQuery: true
    isInternal: true
    retType: <class 'str'>
    doc: |-
        Returns a string containing a formatted summary of the
        coupled analysis setup.

        This summary is printed in the System Coupling transcript
        output at the beginning of a solve. However, it is sometimes
        useful to see the summary before starting the solve.

        The summary output is generated by System Coupling and is not
        modified for PySystemCoupling purposes. Any ``datamodel`` type names
        that are referenced in the summary therefore might not
        be fully consistent with PySystemCoupling conventions.
    essentialArgNames: []
    optionalArgNames: []
    args: []
-   name: GetErrors
    pyname: get_status_messages
    exposure: setup
    isInjected: true
    isQuery: true
    retType: <class 'list'>
    doc: |-
        Provides information relating to the current state of the analysis setup.

        The return value is a list of dictionaries. Each dictionary holds a
        single message about the setup status, along with some associated information.
        The dictionary has string-valued fields: ``"message"``, ``"level"``,
        and ``"path"``.

        The ``"message"`` field is the actual text of the message.

        .. note::
           In the current release, generated messages have not been adapted to
           the PySystemCoupling environment and may use naming and terminology that
           is native to the System Coupling application and its own command line
           interface.

           Because there is generally a straightforward mapping to the PySystemCoupling
           exposure of settings and so on, the messages should not be difficult
           to interpret. Nevertheless, the ``get_status_messages`` method should
           be regarded as *beta* functionality in the current release.

        The ``"level"`` field provides information about the severity or nature of the
        message. Possible values are ``"Error"``, ``"Warning"``, ``"Information"``,
        ``"Alpha"``, and ``"Beta"``. ``"Alpha"`` and ``"Beta"`` indicate settings related
        to activated alpha or beta features.

        It is not possible to solve an analysis that has any issues at the ``"Error"``
        severity level. An attempt to invoke the ``solve`` command while there are
        any errors results in an immediate failure.

        If the ``"path"`` field is set, it contains a string representation of the path
        to the setting to which the message pertains. This is given in the form of
        chained Python attribute accesses starting from the ``setup`` attribute.

        Thus, if an issue were detected that is specific to the ``absolute_gap_tolerance``
        setting in a particular coupling interface, a ``"path"`` such as the following would
        be provided:

        ``'coupling_interface["Interface-1"].mapping_control.absolute_gap_tolerance'``


    essentialArgNames: []
    optionalArgNames: []
    args: []
-   name: ClearState
    pyname: clear_state
    isInjected: true
    pysyc_internal_name: _clear_state
"""
