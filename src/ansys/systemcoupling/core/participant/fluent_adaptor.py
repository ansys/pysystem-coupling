from dataclasses import dataclass
import os
from typing import List
import xml.etree.ElementTree as XmlET

### TEMPORARY IMPLEMENTATION

#  This is consistent with the protocol defined in ../protocol.py but note that
#  we do not have an explicit dependency on it.

#  The plan is for PyFluent to be the source of an object like this.


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


class SystemCouplingAdaptor:
    def __init__(self, fluent_session):
        self.__fluent_session = fluent_session
        self.__setup_info = {}

    def __getattr__(self, attr):
        return getattr(self.__fluent_session, attr)

    @property
    def participant_type(self) -> str:
        return "FLUENT"

    def get_variables(self) -> List[Variable]:
        return self.__get_syc_setup()["variables"]

    def get_regions(self) -> List[Region]:
        return self.__get_syc_setup()["regions"]

    def get_analysis_type(self) -> str:
        return self.__get_syc_setup()["analysis-type"]

    def connect(self, host: str, port: int, name: str) -> None:
        self.setup.models.system_coupling.connect_parallel(
            host=host, port=port, name=name
        )

    def solve(self) -> None:
        self.setup.models.system_coupling.init_and_solve()

    def __get_syc_setup(self):
        scp_xml_content = self.__read_setup_file()

        if self.__setup_info.get("xml", "") == scp_xml_content:
            return self.__setup_info

        # Info is out of date
        self.__setup_info = {}

        xml_root = XmlET.ElementTree(XmlET.fromstring(scp_xml_content))

        cosim_control = xml_root.find("./CosimulationControl")
        self.__setup_info["analysis-type"] = cosim_control.find("AnalysisType").text

        self.__setup_info["variables"] = [
            Variable(
                name=(vname := variable.find("Name").text),
                display_name=variable.find("DisplayName").text,
                tensor_type=(
                    "Vector" if vname in {"force", "lorentz-force"} else "Scalar"
                ),
                is_extensive=(
                    vname in ("force", "lorentz-force", "heatrate", "heatflow")
                ),
                location="Node" if vname in ("displacement",) else "Element",
                quantity_type=variable.find("QuantityType").text,
            )
            for variable in cosim_control.find("Variables").findall("Variable")
        ]

        self.__setup_info["regions"] = [
            Region(
                name=region.find("Name").text,
                display_name=region.find("DisplayName").text,
                topology=region.find("Topology").text,
                input_variables=[var.text for var in region.find("InputVariables")],
                output_variables=[var.text for var in region.find("OutputVariables")],
            )
            for region in cosim_control.find("Regions").findall("Region")
        ]

        self.__setup_info["xml"] = scp_xml_content

        return self.__setup_info

    def __read_setup_file(self) -> str:
        # Ideally, Fluent would provide a query that returns the XML string
        scp_file_name = "fluent.scp"
        self.setup.models.system_coupling.write_scp_file(file_name=scp_file_name)
        assert os.path.exists(
            scp_file_name
        ), "ERROR: could not create System Coupling .scp file"

        with open(scp_file_name, "r") as f:
            xml_string = f.read()

        os.remove(scp_file_name)
        return xml_string
