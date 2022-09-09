from copy import deepcopy

from ansys.systemcoupling.core.util.yaml_helper import yaml_load_from_string


def get_data() -> list:
    """Returns list of injected command data in the right form to be inserted
    at a convenient point in the current processing.

    Returned data is always a new copy so can be manipulated at will.
    """
    if get_data.data is None:
        data = yaml_load_from_string(_cmd_yaml)
        get_data.data = data
    return deepcopy(get_data.data)


get_data.data = None


# Metadata handling is a bit of a mess at the moment as it relies on blending together
# data from multiple sources into opaque dictionaries. The data here is a further
# source representing locally defined "commands" that are to be injected into the
# generated API so that they are presented as if they are any other command. The YAML
# format here is equivalent to the format of the command data already being obtained
# by blending the result of two queries to System Coupling. This format is therefore
# amendable to simply being merged into that data.
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
"""
