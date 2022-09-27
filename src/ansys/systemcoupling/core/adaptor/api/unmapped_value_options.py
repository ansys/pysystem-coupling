#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class unmapped_value_options(Container):
    """
    Unmapped value settings.
    """

    syc_name = "UnmappedValueOptions"

    property_names_types = [
        ("matrix_verbosity", "MatrixVerbosity", "int"),
        ("solver_verbosity", "SolverVerbosity", "int"),
        ("solver", "Solver", "str"),
        ("solver_relative_tolerance", "SolverRelativeTolerance", "RealType"),
        ("solver_max_iterations", "SolverMaxIterations", "int"),
        ("solver_max_search_directions", "SolverMaxSearchDirections", "int"),
        ("preconditioner", "Preconditioner", "str"),
        ("ilut_tau", "IlutTau", "RealType"),
        ("ilut_max_fill", "IlutMaxFill", "int"),
        ("ilut_pivot_tol", "IlutPivotTol", "RealType"),
        ("face_filter_tolerance", "FaceFilterTolerance", "RealType"),
        ("rbf_shape_parameter", "RbfShapeParameter", "RealType"),
        ("rbf_linear_correction", "RbfLinearCorrection", "bool"),
        ("rbf_colinearity_tolerance", "RbfColinearityTolerance", "RealType"),
    ]

    @property
    def matrix_verbosity(self) -> int:
        """Matrix verbosity."""
        return self.get_property_state("matrix_verbosity")

    @matrix_verbosity.setter
    def matrix_verbosity(self, value: int):
        self.set_property_state("matrix_verbosity", value)

    @property
    def solver_verbosity(self) -> int:
        """Solver verbosity."""
        return self.get_property_state("solver_verbosity")

    @solver_verbosity.setter
    def solver_verbosity(self, value: int):
        self.set_property_state("solver_verbosity", value)

    @property
    def solver(self) -> str:
        """Solver (\"GMRES\" or \"FGMRES\")."""
        return self.get_property_state("solver")

    @solver.setter
    def solver(self, value: str):
        self.set_property_state("solver", value)

    @property
    def solver_relative_tolerance(self) -> RealType:
        """Solver relative tolerance"""
        return self.get_property_state("solver_relative_tolerance")

    @solver_relative_tolerance.setter
    def solver_relative_tolerance(self, value: RealType):
        self.set_property_state("solver_relative_tolerance", value)

    @property
    def solver_max_iterations(self) -> int:
        """Solver maximum iterations."""
        return self.get_property_state("solver_max_iterations")

    @solver_max_iterations.setter
    def solver_max_iterations(self, value: int):
        self.set_property_state("solver_max_iterations", value)

    @property
    def solver_max_search_directions(self) -> int:
        """Solver maximum search directions."""
        return self.get_property_state("solver_max_search_directions")

    @solver_max_search_directions.setter
    def solver_max_search_directions(self, value: int):
        self.set_property_state("solver_max_search_directions", value)

    @property
    def preconditioner(self) -> str:
        """Preconditioner type (\"None\" or \"ILUT\")."""
        return self.get_property_state("preconditioner")

    @preconditioner.setter
    def preconditioner(self, value: str):
        self.set_property_state("preconditioner", value)

    @property
    def ilut_tau(self) -> RealType:
        """Tolerance for ILUT."""
        return self.get_property_state("ilut_tau")

    @ilut_tau.setter
    def ilut_tau(self, value: RealType):
        self.set_property_state("ilut_tau", value)

    @property
    def ilut_max_fill(self) -> int:
        """Maximum fill level for ILUT."""
        return self.get_property_state("ilut_max_fill")

    @ilut_max_fill.setter
    def ilut_max_fill(self, value: int):
        self.set_property_state("ilut_max_fill", value)

    @property
    def ilut_pivot_tol(self) -> RealType:
        """Pivot tolerance for ILUT."""
        return self.get_property_state("ilut_pivot_tol")

    @ilut_pivot_tol.setter
    def ilut_pivot_tol(self, value: RealType):
        self.set_property_state("ilut_pivot_tol", value)

    @property
    def face_filter_tolerance(self) -> RealType:
        """Tolerance (angle, in degrees) for which to consider nearby faces to be sufficiently
        aligned to be included in the algorithm."""
        return self.get_property_state("face_filter_tolerance")

    @face_filter_tolerance.setter
    def face_filter_tolerance(self, value: RealType):
        self.set_property_state("face_filter_tolerance", value)

    @property
    def rbf_shape_parameter(self) -> RealType:
        """Radial basis function shape parameter for Gaussian shape function."""
        return self.get_property_state("rbf_shape_parameter")

    @rbf_shape_parameter.setter
    def rbf_shape_parameter(self, value: RealType):
        self.set_property_state("rbf_shape_parameter", value)

    @property
    def rbf_linear_correction(self) -> bool:
        """Control whether the radial basis function linear correction is active."""
        return self.get_property_state("rbf_linear_correction")

    @rbf_linear_correction.setter
    def rbf_linear_correction(self, value: bool):
        self.set_property_state("rbf_linear_correction", value)

    @property
    def rbf_colinearity_tolerance(self) -> RealType:
        """Tolerance to use for checking colinearity of nearby data when using the radial
        basis functions for non-overlap extrapolation."""
        return self.get_property_state("rbf_colinearity_tolerance")

    @rbf_colinearity_tolerance.setter
    def rbf_colinearity_tolerance(self, value: RealType):
        self.set_property_state("rbf_colinearity_tolerance", value)
