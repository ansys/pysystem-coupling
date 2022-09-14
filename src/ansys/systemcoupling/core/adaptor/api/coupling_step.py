#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class coupling_step(Integer):
    """
    Integer specifying the coupling step at which the coupled analysis is
    restarted. When used, System Coupling reads the corresponding
    ``Results_step<#>.h5`` file in the specified directory and restarts the
    analysis at the end of the specified coupling step. When this argument
    is used, System Coupling automatically removes the output files related
    to all later coupling steps. If the files cannot be removed, then
    System Coupling generates an exception message instructing you to free
    up the files and reissue the ``open`` command with the ``coupling_step``
    argument. If the simulation's results files are associated with
    coupling iterations, then System Coupling prints an error message
    indicating this.
    """

    syc_name = "CouplingStep"
