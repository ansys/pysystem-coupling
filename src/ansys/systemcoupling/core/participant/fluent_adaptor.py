from dataclasses import dataclass
import os
from typing import List
import xml.etree.ElementTree

### TEMPORARY IMPLEMENTATION

#  This is consistent with the protocol defined in ../protocol.py but note that
#  we do not have an explicit dependency on it.

#  Eventually PyFluent will provide cleaner exposed API calls (no scheme) and may be the source of
#  an object like this.


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


class SystemCouplingAdaptor2:
    def __init__(self, fluent_session):
        self.__fluent_session = fluent_session

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
        setup_info = dict()

        scp_file_name = "fluent.scp"
        self.setup.models.system_coupling.write_scp_file(file_name=scp_file_name)
        assert os.path.exists(
            scp_file_name
        ), "ERROR: could not create System Coupling .scp file"

        xml_root = xml.etree.ElementTree.parse(scp_file_name)
        cosim_control = xml_root.find("./CosimulationControl")
        setup_info["analysis-type"] = cosim_control.find("AnalysisType").text

        setup_info["variables"] = [
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

        setup_info["regions"] = [
            Region(
                name=region.find("Name").text,
                display_name=region.find("DisplayName").text,
                topology=region.find("Topology").text,
                input_variables=[var.text for var in region.find("InputVariables")],
                output_variables=[var.text for var in region.find("OutputVariables")],
            )
            for region in cosim_control.find("Regions").findall("Region")
        ]

        # remove the generated scp file
        os.remove(scp_file_name)

        return setup_info


class SystemCouplingAdaptor:
    def __init__(self, fluent_session):
        self.__fluent_session = fluent_session

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
        connect_command = f'(%sysc-connect-parallel "{host}" {port} "{name}")'
        self.scheme_eval.exec((connect_command,))

    def solve(self) -> None:
        split_version = self.get_fluent_version().split(".")
        major_version = int(split_version[0])
        minor_version = int(split_version[1])
        if major_version >= 24 or (major_version == 23 and minor_version == 2):
            self.scheme_eval.exec(("(sc-init-solve)",))
        else:
            self.scheme_eval.exec(
                ('(ti-menu-load-string "/solve/initialize/initialize-flow")',)
            )
            self.scheme_eval.exec(("(sc-solve)",))

    def __get_syc_setup(self):
        setup_info = dict()

        scp_file_name = "fluent.scp"
        self.file.export.sc_def_file_settings.write_sc_file(
            file_name=scp_file_name  # , overwrite=False
        )
        assert os.path.exists(
            scp_file_name
        ), "ERROR: could not create System Coupling .scp file"

        xml_root = xml.etree.ElementTree.parse(scp_file_name)
        cosim_control = xml_root.find("./CosimulationControl")
        setup_info["analysis-type"] = cosim_control.find("AnalysisType").text

        setup_info["variables"] = [
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

        setup_info["regions"] = [
            Region(
                name=region.find("Name").text,
                display_name=region.find("DisplayName").text,
                topology=region.find("Topology").text,
                input_variables=[var.text for var in region.find("InputVariables")],
                output_variables=[var.text for var in region.find("OutputVariables")],
            )
            for region in cosim_control.find("Regions").findall("Region")
        ]

        # remove the generated scp file
        os.remove(scp_file_name)

        return setup_info
