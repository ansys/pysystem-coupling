#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class interrupt(InjectedCommand):
    """
    Interrupts a solve in progress.

    See also ``abort``. The difference between an interrupted and
    aborted solve is that an interrupted solve may be resumed.

    Parameters
    ----------
    reason_msg : str, optional
        Text to describe the reason for the interrupt.

        This might be used for such purposes as providing
        additional annotation in transcript output.

    """

    syc_name = "interrupt"

    cmd_name = "interrupt"

    argument_names = ["reason_msg"]

    class reason_msg(String):
        """
        Text to describe the reason for the interrupt.

        This might be used for such purposes as providing
        additional annotation in transcript output.
        """

        syc_name = "reason_msg"
