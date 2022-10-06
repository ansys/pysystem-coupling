#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class get_errors(InjectedCommand):
    """
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
       to interpret. Nevertheless ``get_errors`` should be regarded as "beta"
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
    """

    syc_name = "GetErrors"

    cmd_name = "get_errors"
