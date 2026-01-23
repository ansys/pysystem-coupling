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

import threading
import time
from typing import Callable, TextIO, Union

from ansys.systemcoupling.core.charts.chart_datatypes import SeriesData, TimestepData
from ansys.systemcoupling.core.charts.csv_chartdata import CsvChartDataReader
from ansys.systemcoupling.core.charts.message_dispatcher import Message, MsgType
from ansys.systemcoupling.core.util.logging import LOG


class LiveCsvDataSource:
    def __init__(
        self,
        interface_names: list[str],
        csvfiles: list[Union[str, TextIO]],
        put_msg: Callable[[Message], None],
    ):
        self._csv_readers = [
            CsvChartDataReader(name, csvfile)
            for name, csvfile in zip(interface_names, csvfiles)
        ]
        self._put_msg = put_msg
        self._is_cancelled = threading.Event()
        self._last_data_len: list[list[int]] = [[] for _ in range(len(interface_names))]
        LOG.debug("LiveCsvDataSource initialized for interfaces: %s", interface_names)
        LOG.debug(
            "    _last_data_len initialized with length %s", len(self._last_data_len)
        )

    def cancel(self):
        self._is_cancelled.set()

    def read_data(self):

        metadata_read = [False] * len(self._csv_readers)
        while not self._is_cancelled.is_set():
            for i_series, csv_reader in enumerate(self._csv_readers):
                if not metadata_read[i_series] and csv_reader.read_metadata():
                    LOG.debug("Read metadata for interface index: %s", i_series)
                    self._put_msg(
                        Message(type=MsgType.METADATA, data=csv_reader.metadata)
                    )
                    metadata_read[i_series] = True
            if all(metadata_read):
                break
            time.sleep(0.1)

        last_step_iter = -1
        last_round = False
        while True:
            for i_intf, csv_reader in enumerate(self._csv_readers):
                LOG.debug(
                    "LiveCsvDataSource reading new data for interface index: %s",
                    i_intf,
                )
                csv_reader.read_new_data()
                timestep_data: TimestepData = csv_reader.timestep_data
                if (
                    len(timestep_data.times)
                    and timestep_data.last_iterations[-1] > last_step_iter
                ):
                    # Time data has advanced
                    last_step_iter = timestep_data.last_iterations[-1]
                    self._put_msg(
                        Message(type=MsgType.TIMESTEP_DATA, data=timestep_data)
                    )
                data = csv_reader.data
                if not self._last_data_len[i_intf]:
                    self._last_data_len[i_intf] = [0] * len(data.series)
                for i_series, line_series in enumerate(data.series):
                    start_index = self._last_data_len[i_intf][i_series]
                    new_data_len = len(line_series.data)

                    if new_data_len - start_index == 0:
                        continue

                    LOG.debug(
                        "  interface %s series %s: sending data from index %s to %s",
                        i_intf,
                        i_series,
                        start_index,
                        new_data_len,
                    )

                    line_series_incr = SeriesData(
                        interface_name=line_series.interface_name,
                        transfer_index=line_series.transfer_index,
                        start_index=start_index,
                        data=line_series.data[start_index:],
                    )
                    self._put_msg(
                        Message(type=MsgType.SERIES_DATA, data=line_series_incr)
                    )
                    self._last_data_len[i_intf][i_series] = new_data_len

            if last_round:
                self._put_msg(Message(type=MsgType.END_OF_DATA))
                break
            elif self._is_cancelled.is_set():
                LOG.debug("LiveCsvDataSource cancellation detected")
                # Allow opportunity for any trailing updates to file
                last_round = True

            time.sleep(0.5 / len(self._csv_readers))
