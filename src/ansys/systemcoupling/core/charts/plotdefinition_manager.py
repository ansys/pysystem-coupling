# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dataclasses import dataclass, field
from typing import Optional

from ansys.systemcoupling.core.charts.chart_datatypes import InterfaceInfo, SeriesType


@dataclass
class DataTransferSpec:
    # It's not ideal, but we have to work in terms of display names for transfers,
    # as that is all we have in the data (the CSV data, at least).
    display_name: str
    show_convergence: bool = True
    show_transfer_values: bool = True


@dataclass
class InterfaceSpec:
    name: str
    display_name: str
    transfers: list[DataTransferSpec] = field(default_factory=list)


@dataclass
class PlotSpec:
    interfaces: list[InterfaceSpec] = field(default_factory=list)
    plot_time: bool = False


"""
Convergence subplot:
    title - Data Transfer Convergence for <interface disp name>
    x-axis label - Iteration/Time
    y-axis label - RMS Change in Target Value

    # x-data: []
    y-data: [([], <label=transfer disp name>)]

    # y-data - we actually want an index


Transfer values subplot:
    title - <interface display name> - <transfer display name> (<value type>)
    x-axis label: Iteration/time
    y-axis label: <NOT SET>

    y-data: [([], <label=source|tgt disp name + suffix)]

"""


@dataclass
class SubplotDefinition:
    """Various data - mainly title and label strings - used in the rendering of
    a subplot.

    Attributes
    ----------
    title: str
        The title of the subplot.
    is_log_y: bool
        Whether the y-axis is logarithmic.
    x_axis_label: str
        The label shown on the x-axis.
    y_axis_label: str
        The label shown on the y-axis. This is an empty string for convergence plots.
    index: int = -1
        The index of this subplot within the list of subplots in the current figure.
        (In `matplotlib` terms it also indexes the corresponding ``Axes`` item in
        the figure.)
    series_labels: list[str] = field(default_factory=list)
        Labels for each series of the subplot.
    """

    title: str
    is_log_y: bool
    x_axis_label: str
    y_axis_label: str
    index: int = -1
    series_labels: list[str] = field(default_factory=list)


class PlotDefinitionManager:
    def __init__(self, spec: PlotSpec):
        self._plot_spec = spec
        self._data_index_map: dict[str, dict[int, tuple[SubplotDefinition, int]]] = {}
        self._conv_subplots: dict[str, SubplotDefinition] = {}
        self._transfer_subplots: dict[tuple[str, str, int], SubplotDefinition] = {}
        self._subplots: list[SubplotDefinition] = []
        self._allocate_subplots()

    @property
    def subplots(self) -> list[SubplotDefinition]:
        return self._subplots

    def subplot_for_data_index(
        self, interface_name: str, data_index: int
    ) -> tuple[Optional[SubplotDefinition], int]:
        """Return the subplot definition, and the line index within the
        subplot, corresponding to a given ``data_index``.

        The ``data_index`` is a "global" line index for the interface.

        If there is no subplot corresponding to the provided index,
        return a tuple ``(None, -1)``
        """
        try:
            return self._data_index_map[interface_name][data_index]
        except KeyError:
            return (None, -1)

    def get_layout(self) -> tuple[int, int]:
        nsubplot = len(self._subplots)

        if nsubplot == 1:
            ncol = 1
        elif nsubplot < 6:
            ncol = 2
        elif nsubplot < 12:
            ncol = 3
        elif nsubplot < 18:
            ncol = 4
        elif nsubplot < 26:
            ncol = 5
        else:
            raise ValueError(f"Too many subplots requested: {nsubplot}")
        nrow = nsubplot // ncol
        if nsubplot % ncol != 0:
            nrow += 1

        return (nrow, ncol)

    def _allocate_subplots(self):
        is_time = self._plot_spec.plot_time
        conv_subplots = {}
        transfer_subplots = {}
        subplots = []
        for interface in self._plot_spec.interfaces:
            conv = SubplotDefinition(
                title=f"Data transfer convergence on {interface.display_name}",
                is_log_y=True,
                x_axis_label="Time" if is_time else "Iteration",
                y_axis_label="RMS Change in target value",
            )
            # Add this now so that it is before transfer values plots but we may end
            # up removing it if none of the transfers add a convergence line to it
            conv_index = len(subplots)
            subplots.append(conv)
            keep_conv = False
            transfer_disambig: dict[str, int] = {}
            for transfer in interface.transfers:
                if transfer.display_name in transfer_disambig:
                    transfer_disambig[transfer.display_name] += 1
                else:
                    transfer_disambig[transfer.display_name] = 0
                if transfer.show_convergence:
                    keep_conv = True
                if transfer.show_transfer_values:
                    transfer_value = SubplotDefinition(
                        # NB: <VALUETYPE> is a placeholder - substitute later from metadata info
                        title=f"{interface.display_name} - {transfer.display_name} (<VALUETYPE>)",
                        is_log_y=False,
                        x_axis_label="Time" if is_time else "Iteration",
                        y_axis_label="",
                    )
                    transfer_subplots[
                        (
                            interface.name,
                            transfer.display_name,
                            transfer_disambig[transfer.display_name],
                        )
                    ] = transfer_value
                    subplots.append(transfer_value)
            if keep_conv:
                conv_subplots[interface.name] = conv
            else:
                subplots[conv_index] = None
        # Clean out inactive convergence plots
        self._subplots = [subplot for subplot in subplots if subplot is not None]
        for i, subplot in enumerate(self._subplots):
            subplot.index = i
        self._conv_subplots: dict[str, SubplotDefinition] = conv_subplots
        self._transfer_subplots: dict[tuple[str, str, int], SubplotDefinition] = (
            transfer_subplots
        )

    def set_metadata(self, metadata: InterfaceInfo):
        """Reconcile the metadata for a single interface with the pre-allocated
        sub-plots and set up any necessary data routing.

        Typically, this data only starts to be provided once the raw plot data starts
        being generated.
        """

        # If a subset of transfers was specified in the plot spec, this is already
        # implicitly accounted for in self._tranfer_subplots, which will contain only
        # the active ones. However, some additional work has to be done to filter the
        # transfers shown on the convergence subplot and we have to go back to the plot
        # spec to get a list of active transfers.
        active_transfers = []
        for intf in self._plot_spec.interfaces:
            if intf.name == metadata.name:
                active_transfers = [trans.display_name for trans in intf.transfers]
                break
        if not active_transfers:
            # TODO: should this be an exception?
            return

        # map from source data index to corresponding (subplot, line index within subplot)
        data_index_map: dict[int, tuple[SubplotDefinition, int]] = {}
        interface_name = metadata.name
        iconv = 0

        # Keep a running count of the transfer value lines associated with a given
        # transfer. There will be multiple if the transfer variable has vector
        # and or real/imag components. Note that a transfer is uniquely identified by a
        # pair (transfer_name, int) because transfer names are not guaranteed to be unique.
        # The integer is the "disambiguation_index" the transfer's TransferSeriesInfo.
        transfer_value_line_count: dict[tuple[str, int], int] = {}

        for transfer in metadata.transfer_info:
            transfer_key = (
                transfer.transfer_display_name,
                transfer.disambiguation_index,
            )
            if transfer.series_type == SeriesType.CONVERGENCE:
                if transfer.transfer_display_name not in active_transfers:
                    # We don't want this transfer on the convergence plot
                    continue
                # Clear the entry in case transfer names are not unique. (If another transfer
                # with the same name needs plotting, then it should appear as a second entry
                # in active_transfers.)
                active_transfers[
                    active_transfers.index(transfer.transfer_display_name)
                ] = ""

                if conv_subplot := self._conv_subplots.get(interface_name):
                    data_index_map[transfer.data_index] = (conv_subplot, iconv)
                    # Add a new series list to y_data, and label to series_labels
                    # Both will be at position iconv of respective lists
                    # conv_subplot.y_data.append([])
                    conv_subplot.series_labels.append(transfer.transfer_display_name)
                    iconv += 1
            else:
                transfer_value_subplot = self._transfer_subplots.get(
                    (interface_name, transfer_key[0], transfer_key[1])
                )
                if transfer_value_subplot:
                    value_type = (
                        "Sum"
                        if transfer.series_type == SeriesType.SUM
                        else "Weighted Average"
                    )
                    transfer_value_subplot.title = transfer_value_subplot.title.replace(
                        "<VALUETYPE>", value_type
                    )
                    itransval = transfer_value_line_count.get(transfer_key, 0)
                    if not transfer.line_suffixes:
                        data_index_map[transfer.data_index] = (
                            transfer_value_subplot,
                            itransval,
                        )
                        transfer_value_subplot.series_labels.append(
                            transfer.participant_display_name
                        )
                        itransval += 1
                        transfer_value_line_count[transfer_key] = itransval
                    else:
                        for i, suffix in enumerate(transfer.line_suffixes):
                            data_index_map[transfer.data_index + i] = (
                                transfer_value_subplot,
                                itransval + i,
                            )
                            transfer_value_subplot.series_labels.append(
                                transfer.participant_display_name + suffix
                            )
                        transfer_value_line_count[transfer_key] = itransval + len(
                            transfer.line_suffixes
                        )

        # This will be what allows us to update subplot data as new data received
        self._data_index_map[interface_name] = data_index_map
