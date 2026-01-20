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

from ansys.systemcoupling.core.charts.chart_datatypes import SeriesData
from ansys.systemcoupling.core.charts.csv_chartdata import CsvChartDataReader
from ansys.systemcoupling.core.charts.message_dispatcher import Message, MsgType


class LiveCsvDataSource:
    def __init__(
        self,
        interface_name: str,
        csvfile: Union[str, TextIO],
        put_msg: Callable[[Message], None],
    ):
        self._csv_reader = CsvChartDataReader(interface_name, csvfile)
        self._put_msg = put_msg
        self._is_cancelled = threading.Event()
        self._last_data_len = []

    def cancel(self):
        self._is_cancelled.set()

    def read_data(self):

        while not self._is_cancelled.is_set():
            if not self._csv_reader.read_metadata():
                time.sleep(0.5)
            else:
                self._put_msg(
                    Message(type=MsgType.METADATA, data=self._csv_reader.metadata)
                )
                break

        last_round = False
        while True:
            self._csv_reader.read_new_data()
            data = self._csv_reader.data
            if not self._last_data_len:
                self._last_data_len = [0] * len(data.series)
            for i, line_series in enumerate(data.series):
                start_index = self._last_data_len[i]
                new_data_len = len(line_series.data)

                if new_data_len - start_index == 0:
                    continue

                line_series_incr = SeriesData(
                    line_series.transfer_index,
                    line_series.component_index,
                    start_index=start_index,
                    data=line_series.data[start_index:],
                )
                self._put_msg(Message(type=MsgType.SERIES_DATA, data=line_series_incr))
                self._last_data_len[i] = new_data_len

            if last_round:
                self._put_msg(Message(type=MsgType.END_OF_DATA))
                break
            elif self._is_cancelled.is_set():
                # Allow opportunity for any trailing updates to file
                last_round = True

            time.sleep(0.5)
