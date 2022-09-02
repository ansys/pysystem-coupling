#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class participant_type(String):
    """
    Participant type. Currently supported types are:

    - \"DEFAULT\"
    - \"CFX\"
    - \"FLUENT\"
    - \"MAPDL\"
    - \"AEDT\"
    - \"FMU\"
    - \"FORTE\"
    - \"DEFAULT-SRV\"
    - \"MECH-SRV\"
    - \"CFD-SRV\"

    If unspecified, ``add_participant`` will attempt to deduce
    the type from ``input_file``.
    """

    syc_name = "ParticipantType"
