#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class names_and_fractions(StrFloatPairList):
    """
    List of tuples specifying the fractions of core count applied for
    each participant

    Each tuple must have the ParticipantName as its first item and the
    associated fraction as its second item. If this parameter is omitted,
    then cores will be allocated for all participants set in the
    data model.
    """

    syc_name = "NamesAndFractions"
