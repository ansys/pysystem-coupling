#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class write_csv_chart_files(Command):
    """
    For each coupling interface, exports a CSV file containing chart data
    (convergence and source/target quantity transfer values) for
    that interface.

    Each file is named according to the convention ``<interface>.csv``, where
    ``<interface>`` is the object name of the corresponding coupling interface.

    This command will overwrite any CSV charting files that already exist,
    including any that were written during the solution.
    """

    syc_name = "WriteCsvChartFiles"
