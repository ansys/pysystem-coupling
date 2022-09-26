#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class clear_state(Command):
    """
    Clears the state of the entire System Coupling service, removing all
    data model items, parameter values, and calculated values.

    Cannot be run after participants have been started.
    """

    syc_name = "ClearState"
