#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class coupling_iteration(Integer):
    """
    Integer specifying the coupling iteration at which the coupled analysis
    is restarted. When used, System Coupling reads the corresponding
    ``Results_iter<#>.h5`` file in the specified directory and restarts the
    analysis at the end of the specified coupling iteration. When this
    argument is used, System Coupling automatically removes the output
    files related to all later coupling iterations. If the files cannot be
    removed, then System Coupling generates an exception message
    instructing you to free up the files and reissue the ``open`` command with
    the ``coupling_iteration`` argument. If the simulation's results files are
    associated with coupling steps, then System Coupling prints an error
    message indicating this.
    """

    syc_name = "CouplingIteration"
