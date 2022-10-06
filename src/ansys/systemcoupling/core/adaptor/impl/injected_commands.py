from copy import deepcopy
from typing import Callable, Dict

from ansys.systemcoupling.core.util.yaml_helper import yaml_load_from_string

from .get_status_messages import get_status_messages
from .types import Container


def get_injected_cmd_map(
    category: str, root_object: Container, rpc
) -> Dict[str, Callable]:
    """Returns a dictionary that maps names to functions that implement injected command.

    The map returned pertains to the commands in the specified category.
    """
    if category == "setup":
        return {
            "get_status_messages": lambda **kwargs: get_status_messages(
                rpc, root_object, **kwargs
            )
        }
    if category == "solution":
        return {
            "solve": lambda **kwargs: rpc.solve(),
            "interrupt": lambda **kwargs: rpc.interrupt(**kwargs),
            "abort": lambda **kwargs: rpc.abort(**kwargs),
        }
    return {}


def get_injected_cmd_data() -> list:
    """Returns list of injected command data in the right form to be inserted
    at a convenient point in the current processing.

    Returned data is always a new copy so can be manipulated at will.
    """
    if get_injected_cmd_data.data is None:
        data = yaml_load_from_string(_cmd_yaml)
        get_injected_cmd_data.data = data
    return deepcopy(get_injected_cmd_data.data)


get_injected_cmd_data.data = None


# Metadata handling is a bit of a mess at the moment as it relies on blending together
# data from multiple sources into opaque dictionaries. The data here is a further
# source that represents locally defined "commands" that are to be injected into the
# generated API so that they are presented in a uniform manner (i.e. same as generated).
#
# The YAML format here is equivalent to the format of the command data already being
# obtained by blending the result of two queries to System Coupling. This format is
# therefore amenable to simply being merged into that data.
# (TODO: investigate rationalisation of raw queried data and look at introduction of
# dataclasses etc on this side.)

_cmd_yaml = """
-   name: Solve
    pyname: solve
    isInjected: true
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
        aborted solve is that an interrupted solve may be resumed.
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
        an aborted solve may not be resumed.
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
        The dictionary has string-valued fields "message", "level" and "path".

        The "message" field is the actual text of the message.

        .. note::
           In the current release, generated messages have not been adapted to
           the PySystemCoupling environment and may use naming and terminology that
           is native to the System Coupling application and its own command line
           interface.

           Generally, there is a straightforward mapping to the PySystemCoupling
           exposure of settings and so on, so the messages should not be difficult
           to interpret. Nevertheless ``get_status_messages`` should be regarded as "beta"
           functionality in the current release.

        The "level" field provides information about the severity or nature of the
        message. Possible values are "Error", "Warning", "Information", "Alpha" and
        "Beta". "Alpha" and "Beta" are used to inform the user of settings related
        to activated alpha or beta features.

        It is not possible to solve an analysis that has any issues at "Error"
        severity level. An attempt to invoke the ``solve`` command while there are
        any errors will result in an immediate failure.

        If the "path" field is set, it contains a string representation of the path
        to the setting to which the message pertains. This is given in the form of
        chained Python attribute accesses starting from ``setup``.

        Thus, if an issue were detected that is specific to the ``absolute_gap_tolerance``
        setting in a particular coupling interface, a "path" such as the following would
        be provided:

        ``'coupling_interface["Interface-1"].mapping_control.absolute_gap_tolerance'``


    essentialArgNames: []
    optionalArgNames: []
    args: []
"""
