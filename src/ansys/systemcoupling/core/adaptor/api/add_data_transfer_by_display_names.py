#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .interface_1 import interface
from .side_one_variable_1 import side_one_variable
from .side_two_variable_1 import side_two_variable
from .source_variable_1 import source_variable
from .target_side import target_side
from .target_variable_1 import target_variable
from .value_1 import value
from .value_x_1 import value_x
from .value_y_1 import value_y
from .value_z_1 import value_z


class add_data_transfer_by_display_names(Command):
    """
    Adds data transfer based on arguments that specify the interface, target
    side, and variables to be associated with each side of the interface.
    The command requires that you specify variables using their display names
    (see parameter descriptions for details). Either a variable-based
    or expression-based data transfer may be created with this command based on
    the arguments provided. If a variable-based data transfer argument
    is given, then no expression-based data transfer arguments can be used. If
    an expression-based data transfer argument is given, then no variable-based
    data transfer arguments can be used.

    Cannot be run after participants have been started.

    Returns the name of the Data Transfer created.

    Parameters
    ----------
    interface : str
        String indicating the display name of the interface on which the
        data transfer is to be created.
    target_side : str
        String indicating the side of the interface to receive the data
        transfer variable. Possible values are \"One\" or \"Two\".
    source_variable : str, optional
        String specifying the display name of the variable on the source side of
        the data transfer. Used when creating a variable-based data transfer.
        Must be combined with ``target_variable``.
    target_variable : str, optional
        String specifying the display name of the variable on the target side of
        the data transfer. Must be combined with either ``source_variable`` (when
        creating a variable-based data transfer) or with ``value_{x|y|z}``
        (when creating an expression-based data transfer).
    value : str, optional
        String specifying the expression to use on the source side of the data
        transfer. Used when creating an expression-based data transfer if the
        ``target_variable`` is a scalar. (If the ``target_variable`` is a vector,
        ``value_x``, ``value_y``, ``value_z`` must be used instead.)
    value_x : str, optional
        String specifying the X component of the expression to use on the
        source side of the data transfer. Used when crating an expression-based
        data transfer if the ``target_variable`` is a vector. (If the ``target_variable``
        is scalar, ``value`` must be used instead.) ``value_y`` and ``value_z`` are also
        required if ``value_x`` is used.
    value_y : str, optional
        String specifying the Y component of the expression to use on the
        source side of the data transfer. Used when crating an expression-based
        data transfer if the ``target_variable`` is a vector. (If the ``target_variable``
        is scalar, ``value`` must be used instead.) ``value_x`` and ``value_z`` are also
        required if ``value_y`` is used.
    value_z : str, optional
        String specifying the Z component of the expression to use on the
        source side of the data transfer. Used when crating an expression-based
        data transfer if the ``target_variable`` is a vector. (If the ``target_variable``
        is scalar, ``value`` must be used instead.) ``value_x`` and ``value_y`` are also
        required if ``value_z`` is used.
    side_one_variable : str, optional
        String specifying the display name of the variable associated with side one
        of the interface. Must be combined with ``side_two_variable``. Used only
        when creating variable-based data transfers. Consider using
        ``source_variable``/``target_variable`` parameters instead.
    side_two_variable : str, optional
        String specifying the display name of the variable associated with side two
        of the interface. Must be combined with ``side_two_variable``. Used only
        when creating variable-based data transfers. Consider using
        ``source_variable``/``target_variable`` parameters instead.

    """

    syc_name = "AddDataTransferByDisplayNames"

    argument_names = [
        "interface",
        "target_side",
        "source_variable",
        "target_variable",
        "value",
        "value_x",
        "value_y",
        "value_z",
        "side_one_variable",
        "side_two_variable",
    ]

    interface: interface = interface
    """
    interface argument of add_data_transfer_by_display_names.
    """
    target_side: target_side = target_side
    """
    target_side argument of add_data_transfer_by_display_names.
    """
    source_variable: source_variable = source_variable
    """
    source_variable argument of add_data_transfer_by_display_names.
    """
    target_variable: target_variable = target_variable
    """
    target_variable argument of add_data_transfer_by_display_names.
    """
    value: value = value
    """
    value argument of add_data_transfer_by_display_names.
    """
    value_x: value_x = value_x
    """
    value_x argument of add_data_transfer_by_display_names.
    """
    value_y: value_y = value_y
    """
    value_y argument of add_data_transfer_by_display_names.
    """
    value_z: value_z = value_z
    """
    value_z argument of add_data_transfer_by_display_names.
    """
    side_one_variable: side_one_variable = side_one_variable
    """
    side_one_variable argument of add_data_transfer_by_display_names.
    """
    side_two_variable: side_two_variable = side_two_variable
    """
    side_two_variable argument of add_data_transfer_by_display_names.
    """
