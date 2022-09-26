#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


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

    class interface(String):
        """
        String indicating the display name of the interface on which the
        data transfer is to be created.
        """

        syc_name = "Interface"

    class target_side(String):
        """
        String indicating the side of the interface to receive the data
        transfer variable. Possible values are \"One\" or \"Two\".
        """

        syc_name = "TargetSide"

    class source_variable(String):
        """
        String specifying the display name of the variable on the source side of
        the data transfer. Used when creating a variable-based data transfer.
        Must be combined with ``target_variable``.
        """

        syc_name = "SourceVariable"

    class target_variable(String):
        """
        String specifying the display name of the variable on the target side of
        the data transfer. Must be combined with either ``source_variable`` (when
        creating a variable-based data transfer) or with ``value_{x|y|z}``
        (when creating an expression-based data transfer).
        """

        syc_name = "TargetVariable"

    class value(String):
        """
        String specifying the expression to use on the source side of the data
        transfer. Used when creating an expression-based data transfer if the
        ``target_variable`` is a scalar. (If the ``target_variable`` is a vector,
        ``value_x``, ``value_y``, ``value_z`` must be used instead.)
        """

        syc_name = "Value"

    class value_x(String):
        """
        String specifying the X component of the expression to use on the
        source side of the data transfer. Used when crating an expression-based
        data transfer if the ``target_variable`` is a vector. (If the ``target_variable``
        is scalar, ``value`` must be used instead.) ``value_y`` and ``value_z`` are also
        required if ``value_x`` is used.
        """

        syc_name = "ValueX"

    class value_y(String):
        """
        String specifying the Y component of the expression to use on the
        source side of the data transfer. Used when crating an expression-based
        data transfer if the ``target_variable`` is a vector. (If the ``target_variable``
        is scalar, ``value`` must be used instead.) ``value_x`` and ``value_z`` are also
        required if ``value_y`` is used.
        """

        syc_name = "ValueY"

    class value_z(String):
        """
        String specifying the Z component of the expression to use on the
        source side of the data transfer. Used when crating an expression-based
        data transfer if the ``target_variable`` is a vector. (If the ``target_variable``
        is scalar, ``value`` must be used instead.) ``value_x`` and ``value_y`` are also
        required if ``value_z`` is used.
        """

        syc_name = "ValueZ"

    class side_one_variable(String):
        """
        String specifying the display name of the variable associated with side one
        of the interface. Must be combined with ``side_two_variable``. Used only
        when creating variable-based data transfers. Consider using
        ``source_variable``/``target_variable`` parameters instead.
        """

        syc_name = "SideOneVariable"

    class side_two_variable(String):
        """
        String specifying the display name of the variable associated with side two
        of the interface. Must be combined with ``side_two_variable``. Used only
        when creating variable-based data transfers. Consider using
        ``source_variable``/``target_variable`` parameters instead.
        """

        syc_name = "SideTwoVariable"
