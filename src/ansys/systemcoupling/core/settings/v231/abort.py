#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .reason_msg_1 import reason_msg


class abort(InjectedCommand):
    """
    Aborts a solve in progress.

    See also ``interrupt``. In contrast to an interrupted solve,
    an aborted solve may not be resumed.

    Parameters
    ----------
    reason_msg : str, optional
        Text to describe the reason for the abort.

        This might be used for such purposes as providing
        additional annotation in transcript output.

    """

    syc_name = "abort"

    cmd_name = "abort"

    argument_names = ["reason_msg"]

    reason_msg: reason_msg = reason_msg
    """
    reason_msg argument of abort.
    """
