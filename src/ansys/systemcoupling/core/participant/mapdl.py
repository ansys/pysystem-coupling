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

from dataclasses import dataclass
from typing import List


class MapdlSystemCouplingInterface(object):
    @dataclass
    class Variable:
        name: str
        display_name: str
        tensor_type: str
        is_extensive: bool
        location: str
        quantity_type: str

    @dataclass
    class Region:
        name: str
        display_name: str
        topology: str
        input_variables: List[str]
        output_variables: List[str]

    def __init__(self, solver):
        self._solver = solver
        self.__clear()
        if self._solver.version < 24.2:
            msg = "PySystemCoupling integration requires MAPDL version 24.2 or later."
            msg += f" Current version is {self._solver.version}"
            raise RuntimeError(msg)

    @property
    def participant_type(self) -> str:
        return "MAPDL"

    def get_variables(self):
        self._parse_setup()
        return self.__variables

    def get_regions(self):
        self._parse_setup()
        return self.__regions

    def get_analysis_type(self) -> str:
        analysis_type = int(self._solver.get(entity="ACTIVE", item1="ANTY"))
        if analysis_type == 0:
            return "Steady"
        elif analysis_type == 4:
            return "Transient"
        else:
            raise MapdlRuntimeError(f"Unsupported analysis type: {analysis_type}")

    def connect(self, host, port, name):
        self._solver.run(f"scconnect,{host},{port},{name}")

    def solve(self):
        self._solver.solve()

    def __clear(self):
        self.__regions = list()
        self.__variables = list()
        self.__structural = False
        self.__thermal = False

    def _parse_setup(self):
        self.__clear()
        # TODO: need to actually check element types connected to the FSI region
        et_index = self._solver.get(entity="ACTIVE", item1="TYPE")
        element_type = int(
            self._solver.get(
                entity="ETYP", entnum=et_index, item1="ATTR", it1num="ENAM"
            )
        )
        # TODO: the elements list may not be complete
        if element_type in {181, 185, 186, 187, 190, 225, 226, 227, 281, 285}:
            self._activate_structural()
        if element_type in {131, 132, 225, 226, 227, 278, 279, 291}:
            self._activate_thermal()

        num_comp = int(self._solver.get(entity="COMP", item1="NCOMP"))
        for curr_comp in range(1, num_comp + 1):
            region_name = self._solver.get(
                entity="COMP", entnum=curr_comp, item1="NAME"
            )
            comp_type = int(
                self._solver.get(entity="COMP", entnum=region_name, item1="TYPE")
            )
            # if type of component is "Nodes" (1), check for SF FSIN
            if comp_type == 1:
                res = self._solver.sflist(node=region_name, lab="FSIN")
                if "There are no nodal fluid solid interfaces" not in str(res):
                    self._add_surface_region(region_name)
            # if type of component is "Elements" (2), check for BFE FVIN
            elif comp_type == 2:
                res = self._solver.bfelist(node=region_name, lab="FVIN")
                if "There are no" not in str(res):
                    self._add_volume_region(region_name)

    def _add_surface_region(self, region_name):
        region = MapdlSystemCouplingInterface.Region(
            name=region_name,
            display_name=f"System Coupling (Surface) Region {len(self.__regions)}",
            topology="Surface",
            input_variables=list(),
            output_variables=list(),
        )
        if self.__structural:
            region.input_variables.append("FORC")
            region.input_variables.append("FDNS")
            region.output_variables.append("INCD")
        if self.__thermal:
            region.input_variables.append("TEMP")
            region.input_variables.append("TBULK")
            region.input_variables.append("HCOEF")
            region.input_variables.append("HFLW")
            region.output_variables.append("TEMP")
            region.output_variables.append("TBULK")
            region.output_variables.append("HCOEF")
            region.output_variables.append("HFLW")
        self.__regions.append(region)

    def _add_volume_region(self, region_name):
        region = MapdlSystemCouplingInterface.Region(
            name=region_name,
            display_name=f"System Coupling (Volume) Region {len(self.__regions)}",
            topology="Volume",
            input_variables=list(),
            output_variables=list(),
        )
        if self.__thermal:
            region.input_variables.append("HGEN")
            region.input_variables.append("TPLD")
            region.output_variables.append("TEMP")
        self.__regions.append(region)

    def _activate_structural(self):
        if not self.__structural:
            self.__structural = True
            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="FORC",
                    display_name="Force",
                    tensor_type="Vector",
                    is_extensive=True,
                    location="Node",
                    quantity_type="Force",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="FDNS",
                    display_name="Force Density",
                    tensor_type="Vector",
                    is_extensive=False,
                    location="Element",
                    quantity_type="Force",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="INCD",
                    display_name="Incremental Displacement",
                    tensor_type="Vector",
                    is_extensive=False,
                    location="Node",
                    quantity_type="Incremental Displacement",
                )
            )

            for region in self.__regions:
                if region.topology == "Surface":
                    region.input_variables.append("FORC")
                    region.input_variables.append("FDNS")
                    region.output_variables.append("INCD")

    def _activate_thermal(self):
        if not self.__thermal:
            self.__thermal = True
            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="TEMP",
                    display_name="Temperature",
                    tensor_type="Scalar",
                    is_extensive=False,
                    location="Node",
                    quantity_type="Temperature",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="TBULK",
                    display_name="Bulk Temperature",
                    tensor_type="Scalar",
                    is_extensive=False,
                    location="Node",
                    quantity_type="Convection Reference Temperature",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="HCOEF",
                    display_name="Heat Transfer Coefficient",
                    tensor_type="Scalar",
                    is_extensive=False,
                    location="Node",
                    quantity_type="Heat Transfer Coefficient",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="HFLW",
                    display_name="Heat Flow",
                    tensor_type="Scalar",
                    is_extensive=True,
                    location="Node",
                    quantity_type="Heat Rate",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="HGEN",
                    display_name="Heat Generation",
                    tensor_type="Scalar",
                    is_extensive=False,
                    location="Node",
                    quantity_type="Heat Rate",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="TPLD",
                    display_name="Temperature Load",
                    tensor_type="Scalar",
                    is_extensive=False,
                    location="Node",
                    quantity_type="Temperature",
                )
            )

            self.__variables.append(
                MapdlSystemCouplingInterface.Variable(
                    name="TEMP",
                    display_name="Temperature",
                    tensor_type="Scalar",
                    is_extensive=False,
                    location="Node",
                    quantity_type="Temperature",
                )
            )

            for region in self.__regions:
                if region.topology == "Surface":
                    region.input_variables.append("TEMP")
                    region.input_variables.append("TBULK")
                    region.input_variables.append("HCOEF")
                    region.input_variables.append("HFLW")
                    region.output_variables.append("TEMP")
                    region.output_variables.append("TBULK")
                    region.output_variables.append("HCOEF")
                    region.output_variables.append("HFLW")
                elif region.topology == "Volume":
                    region.input_variables.append("HGEN")
                    region.input_variables.append("TPLD")
                    region.output_variables.append("TEMP")

    def _set_steady(self):
        self.__analysis_type = "Steady"

    def _set_transient(self):
        self.__analysis_type = "Transient"
