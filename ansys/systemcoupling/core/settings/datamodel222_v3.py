"""This is an auto-generated file.  DO NOT EDIT!"""

from ansys.systemcoupling.core.settings.datamodel import *

SHASH = "6dcf89b85d9d37b8ed874803294c14bbb740ec3c55f180530e94ed73d2550793"


class system_coupling(Group):
    """
    root object
    """

    syc_name = "SystemCoupling"
    child_names = [
        "activate_hidden",
        "library",
        "coupling_participant",
        "analysis_control",
        "coupling_interface",
        "solution_control",
        "output_control",
    ]

    class activate_hidden(Group):
        """
        'activate_hidden' child of 'system_coupling' object
        """

        syc_name = "ActivateHidden"
        property_names_types = [
            ("beta_features", "BetaFeatures", "Boolean"),
            ("alpha_features", "AlphaFeatures", "Boolean"),
            ("lenient_validation", "LenientValidation", "Boolean"),
        ]

        @property
        def beta_features(self) -> Boolean:
            """'beta_features' property of 'system_coupling' object"""
            return self.get_property_state("beta_features")

        @beta_features.setter
        def beta_features(self, value: Boolean):
            self.set_property_state("beta_features", value)

        @property
        def alpha_features(self) -> Boolean:
            """'alpha_features' property of 'system_coupling' object"""
            return self.get_property_state("alpha_features")

        @alpha_features.setter
        def alpha_features(self, value: Boolean):
            self.set_property_state("alpha_features", value)

        @property
        def lenient_validation(self) -> Boolean:
            """'lenient_validation' property of 'system_coupling' object"""
            return self.get_property_state("lenient_validation")

        @lenient_validation.setter
        def lenient_validation(self, value: Boolean):
            self.set_property_state("lenient_validation", value)

    class library(Group):
        """
        'library' child of 'system_coupling' object
        """

        syc_name = "Library"
        child_names = [
            "expression",
            "expression_function",
            "reference_frame",
            "instancing",
        ]

        class expression(NamedObject):
            """
            'expression' child of 'library' object
            """

            syc_name = "Expression"

            class child_object_type(Group):
                """
                'child_object_type' child of 'expression' object
                """

                syc_name = "child_object_type"
                property_names_types = [
                    ("expression_name", "ExpressionName", "String"),
                    ("expression_string", "ExpressionString", "String"),
                ]

                @property
                def expression_name(self) -> String:
                    """'expression_name' property of 'expression' object"""
                    return self.get_property_state("expression_name")

                @expression_name.setter
                def expression_name(self, value: String):
                    self.set_property_state("expression_name", value)

                @property
                def expression_string(self) -> String:
                    """'expression_string' property of 'expression' object"""
                    return self.get_property_state("expression_string")

                @expression_string.setter
                def expression_string(self, value: String):
                    self.set_property_state("expression_string", value)

        class expression_function(NamedObject):
            """
            'expression_function' child of 'library' object
            """

            syc_name = "ExpressionFunction"

            class child_object_type(Group):
                """
                'child_object_type' child of 'expression_function' object
                """

                syc_name = "child_object_type"
                property_names_types = [
                    ("module", "Module", "String"),
                    ("function", "Function", "String"),
                    ("function_name", "FunctionName", "String"),
                ]

                @property
                def module(self) -> String:
                    """'module' property of 'expression_function' object"""
                    return self.get_property_state("module")

                @module.setter
                def module(self, value: String):
                    self.set_property_state("module", value)

                @property
                def function(self) -> String:
                    """'function' property of 'expression_function' object"""
                    return self.get_property_state("function")

                @function.setter
                def function(self, value: String):
                    self.set_property_state("function", value)

                @property
                def function_name(self) -> String:
                    """'function_name' property of 'expression_function' object"""
                    return self.get_property_state("function_name")

                @function_name.setter
                def function_name(self, value: String):
                    self.set_property_state("function_name", value)

        class reference_frame(NamedObject):
            """
            'reference_frame' child of 'library' object
            """

            syc_name = "ReferenceFrame"

            class child_object_type(Group):
                """
                'child_object_type' child of 'reference_frame' object
                """

                syc_name = "child_object_type"
                child_names = ["transformation"]

                class transformation(NamedObject):
                    """
                    'transformation' child of 'child_object_type' object
                    """

                    syc_name = "Transformation"

                    class child_object_type(Group):
                        """
                        'child_object_type' child of 'transformation' object
                        """

                        syc_name = "child_object_type"
                        property_names_types = [
                            ("option", "Option", "String"),
                            ("angle", "Angle", "Real"),
                            ("axis", "Axis", "String"),
                            ("vector", "Vector", "RealList"),
                        ]

                        @property
                        def option(self) -> String:
                            """'option' property of 'transformation' object"""
                            return self.get_property_state("option")

                        @option.setter
                        def option(self, value: String):
                            self.set_property_state("option", value)

                        @property
                        def angle(self) -> Real:
                            """'angle' property of 'transformation' object"""
                            return self.get_property_state("angle")

                        @angle.setter
                        def angle(self, value: Real):
                            self.set_property_state("angle", value)

                        @property
                        def axis(self) -> String:
                            """'axis' property of 'transformation' object"""
                            return self.get_property_state("axis")

                        @axis.setter
                        def axis(self, value: String):
                            self.set_property_state("axis", value)

                        @property
                        def vector(self) -> RealList:
                            """'vector' property of 'transformation' object"""
                            return self.get_property_state("vector")

                        @vector.setter
                        def vector(self, value: RealList):
                            self.set_property_state("vector", value)

                property_names_types = [
                    ("option", "Option", "String"),
                    ("parent_reference_frame", "ParentReferenceFrame", "String"),
                    ("transformation_order", "TransformationOrder", "StringList"),
                    ("transformation_matrix", "TransformationMatrix", "RealList"),
                ]

                @property
                def option(self) -> String:
                    """'option' property of 'reference_frame' object"""
                    return self.get_property_state("option")

                @option.setter
                def option(self, value: String):
                    self.set_property_state("option", value)

                @property
                def parent_reference_frame(self) -> String:
                    """'parent_reference_frame' property of 'reference_frame' object"""
                    return self.get_property_state("parent_reference_frame")

                @parent_reference_frame.setter
                def parent_reference_frame(self, value: String):
                    self.set_property_state("parent_reference_frame", value)

                @property
                def transformation_order(self) -> StringList:
                    """'transformation_order' property of 'reference_frame' object"""
                    return self.get_property_state("transformation_order")

                @transformation_order.setter
                def transformation_order(self, value: StringList):
                    self.set_property_state("transformation_order", value)

                @property
                def transformation_matrix(self) -> RealList:
                    """'transformation_matrix' property of 'reference_frame' object"""
                    return self.get_property_state("transformation_matrix")

                @transformation_matrix.setter
                def transformation_matrix(self, value: RealList):
                    self.set_property_state("transformation_matrix", value)

        class instancing(NamedObject):
            """
            'instancing' child of 'library' object
            """

            syc_name = "Instancing"

            class child_object_type(Group):
                """
                'child_object_type' child of 'instancing' object
                """

                syc_name = "child_object_type"
                property_names_types = [
                    ("reference_frame", "ReferenceFrame", "String"),
                    ("instances_in_full_circle", "InstancesInFullCircle", "Integer"),
                    ("instances_for_mapping", "InstancesForMapping", "Integer"),
                ]

                @property
                def reference_frame(self) -> String:
                    """'reference_frame' property of 'instancing' object"""
                    return self.get_property_state("reference_frame")

                @reference_frame.setter
                def reference_frame(self, value: String):
                    self.set_property_state("reference_frame", value)

                @property
                def instances_in_full_circle(self) -> Integer:
                    """'instances_in_full_circle' property of 'instancing' object"""
                    return self.get_property_state("instances_in_full_circle")

                @instances_in_full_circle.setter
                def instances_in_full_circle(self, value: Integer):
                    self.set_property_state("instances_in_full_circle", value)

                @property
                def instances_for_mapping(self) -> Integer:
                    """'instances_for_mapping' property of 'instancing' object"""
                    return self.get_property_state("instances_for_mapping")

                @instances_for_mapping.setter
                def instances_for_mapping(self, value: Integer):
                    self.set_property_state("instances_for_mapping", value)

    class coupling_participant(NamedObject):
        """
        'coupling_participant' child of 'system_coupling' object
        """

        syc_name = "CouplingParticipant"

        class child_object_type(Group):
            """
            'child_object_type' child of 'coupling_participant' object
            """

            syc_name = "child_object_type"
            child_names = [
                "variable",
                "region",
                "update_control",
                "fmu_parameter",
                "execution_control",
                "external_data_file",
            ]

            class variable(NamedObject):
                """
                'variable' child of 'child_object_type' object
                """

                syc_name = "Variable"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'variable' object
                    """

                    syc_name = "child_object_type"
                    child_names = ["attribute"]

                    class attribute(NamedObject):
                        """
                        'attribute' child of 'child_object_type' object
                        """

                        syc_name = "Attribute"

                        class child_object_type(Group):
                            """
                            'child_object_type' child of 'attribute' object
                            """

                            syc_name = "child_object_type"
                            child_names = ["dimensionality"]

                            class dimensionality(Group):
                                """
                                'dimensionality' child of 'child_object_type' object
                                """

                                syc_name = "Dimensionality"
                                property_names_types = [
                                    ("length", "Length", "Real"),
                                    ("time", "Time", "Real"),
                                    ("mass", "Mass", "Real"),
                                    ("temperature", "Temperature", "Real"),
                                    (
                                        "amount_of_substance",
                                        "AmountOfSubstance",
                                        "Real",
                                    ),
                                    ("current", "Current", "Real"),
                                    ("luminous_intensity", "LuminousIntensity", "Real"),
                                    ("angle", "Angle", "Real"),
                                ]

                                @property
                                def length(self) -> Real:
                                    """'length' property of 'child_object_type' object"""
                                    return self.get_property_state("length")

                                @length.setter
                                def length(self, value: Real):
                                    self.set_property_state("length", value)

                                @property
                                def time(self) -> Real:
                                    """'time' property of 'child_object_type' object"""
                                    return self.get_property_state("time")

                                @time.setter
                                def time(self, value: Real):
                                    self.set_property_state("time", value)

                                @property
                                def mass(self) -> Real:
                                    """'mass' property of 'child_object_type' object"""
                                    return self.get_property_state("mass")

                                @mass.setter
                                def mass(self, value: Real):
                                    self.set_property_state("mass", value)

                                @property
                                def temperature(self) -> Real:
                                    """'temperature' property of 'child_object_type' object"""
                                    return self.get_property_state("temperature")

                                @temperature.setter
                                def temperature(self, value: Real):
                                    self.set_property_state("temperature", value)

                                @property
                                def amount_of_substance(self) -> Real:
                                    """'amount_of_substance' property of 'child_object_type' object"""
                                    return self.get_property_state(
                                        "amount_of_substance"
                                    )

                                @amount_of_substance.setter
                                def amount_of_substance(self, value: Real):
                                    self.set_property_state(
                                        "amount_of_substance", value
                                    )

                                @property
                                def current(self) -> Real:
                                    """'current' property of 'child_object_type' object"""
                                    return self.get_property_state("current")

                                @current.setter
                                def current(self, value: Real):
                                    self.set_property_state("current", value)

                                @property
                                def luminous_intensity(self) -> Real:
                                    """'luminous_intensity' property of 'child_object_type' object"""
                                    return self.get_property_state("luminous_intensity")

                                @luminous_intensity.setter
                                def luminous_intensity(self, value: Real):
                                    self.set_property_state("luminous_intensity", value)

                                @property
                                def angle(self) -> Real:
                                    """'angle' property of 'child_object_type' object"""
                                    return self.get_property_state("angle")

                                @angle.setter
                                def angle(self, value: Real):
                                    self.set_property_state("angle", value)

                            property_names_types = [
                                ("attribute_type", "AttributeType", "String"),
                                ("real_value", "RealValue", "Real"),
                                ("integer_value", "IntegerValue", "Integer"),
                            ]

                            @property
                            def attribute_type(self) -> String:
                                """'attribute_type' property of 'attribute' object"""
                                return self.get_property_state("attribute_type")

                            @attribute_type.setter
                            def attribute_type(self, value: String):
                                self.set_property_state("attribute_type", value)

                            @property
                            def real_value(self) -> Real:
                                """'real_value' property of 'attribute' object"""
                                return self.get_property_state("real_value")

                            @real_value.setter
                            def real_value(self, value: Real):
                                self.set_property_state("real_value", value)

                            @property
                            def integer_value(self) -> Integer:
                                """'integer_value' property of 'attribute' object"""
                                return self.get_property_state("integer_value")

                            @integer_value.setter
                            def integer_value(self, value: Integer):
                                self.set_property_state("integer_value", value)

                    property_names_types = [
                        ("quantity_type", "QuantityType", "String"),
                        ("location", "Location", "String"),
                        (
                            "participant_display_name",
                            "ParticipantDisplayName",
                            "String",
                        ),
                        ("display_name", "DisplayName", "String"),
                        ("data_type", "DataType", "String"),
                        ("real_initial_value", "RealInitialValue", "Real"),
                        ("integer_initial_value", "IntegerInitialValue", "Integer"),
                        ("logical_initial_value", "LogicalInitialValue", "Boolean"),
                        ("string_initial_value", "StringInitialValue", "String"),
                        ("real_min", "RealMin", "Real"),
                        ("real_max", "RealMax", "Real"),
                        ("integer_min", "IntegerMin", "Integer"),
                        ("integer_max", "IntegerMax", "Integer"),
                        ("tensor_type", "TensorType", "String"),
                        ("is_extensive", "IsExtensive", "Boolean"),
                    ]

                    @property
                    def quantity_type(self) -> String:
                        """'quantity_type' property of 'variable' object"""
                        return self.get_property_state("quantity_type")

                    @quantity_type.setter
                    def quantity_type(self, value: String):
                        self.set_property_state("quantity_type", value)

                    @property
                    def location(self) -> String:
                        """'location' property of 'variable' object"""
                        return self.get_property_state("location")

                    @location.setter
                    def location(self, value: String):
                        self.set_property_state("location", value)

                    @property
                    def participant_display_name(self) -> String:
                        """'participant_display_name' property of 'variable' object"""
                        return self.get_property_state("participant_display_name")

                    @participant_display_name.setter
                    def participant_display_name(self, value: String):
                        self.set_property_state("participant_display_name", value)

                    @property
                    def display_name(self) -> String:
                        """'display_name' property of 'variable' object"""
                        return self.get_property_state("display_name")

                    @display_name.setter
                    def display_name(self, value: String):
                        self.set_property_state("display_name", value)

                    @property
                    def data_type(self) -> String:
                        """'data_type' property of 'variable' object"""
                        return self.get_property_state("data_type")

                    @data_type.setter
                    def data_type(self, value: String):
                        self.set_property_state("data_type", value)

                    @property
                    def real_initial_value(self) -> Real:
                        """'real_initial_value' property of 'variable' object"""
                        return self.get_property_state("real_initial_value")

                    @real_initial_value.setter
                    def real_initial_value(self, value: Real):
                        self.set_property_state("real_initial_value", value)

                    @property
                    def integer_initial_value(self) -> Integer:
                        """'integer_initial_value' property of 'variable' object"""
                        return self.get_property_state("integer_initial_value")

                    @integer_initial_value.setter
                    def integer_initial_value(self, value: Integer):
                        self.set_property_state("integer_initial_value", value)

                    @property
                    def logical_initial_value(self) -> Boolean:
                        """'logical_initial_value' property of 'variable' object"""
                        return self.get_property_state("logical_initial_value")

                    @logical_initial_value.setter
                    def logical_initial_value(self, value: Boolean):
                        self.set_property_state("logical_initial_value", value)

                    @property
                    def string_initial_value(self) -> String:
                        """'string_initial_value' property of 'variable' object"""
                        return self.get_property_state("string_initial_value")

                    @string_initial_value.setter
                    def string_initial_value(self, value: String):
                        self.set_property_state("string_initial_value", value)

                    @property
                    def real_min(self) -> Real:
                        """'real_min' property of 'variable' object"""
                        return self.get_property_state("real_min")

                    @real_min.setter
                    def real_min(self, value: Real):
                        self.set_property_state("real_min", value)

                    @property
                    def real_max(self) -> Real:
                        """'real_max' property of 'variable' object"""
                        return self.get_property_state("real_max")

                    @real_max.setter
                    def real_max(self, value: Real):
                        self.set_property_state("real_max", value)

                    @property
                    def integer_min(self) -> Integer:
                        """'integer_min' property of 'variable' object"""
                        return self.get_property_state("integer_min")

                    @integer_min.setter
                    def integer_min(self, value: Integer):
                        self.set_property_state("integer_min", value)

                    @property
                    def integer_max(self) -> Integer:
                        """'integer_max' property of 'variable' object"""
                        return self.get_property_state("integer_max")

                    @integer_max.setter
                    def integer_max(self, value: Integer):
                        self.set_property_state("integer_max", value)

                    @property
                    def tensor_type(self) -> String:
                        """'tensor_type' property of 'variable' object"""
                        return self.get_property_state("tensor_type")

                    @tensor_type.setter
                    def tensor_type(self, value: String):
                        self.set_property_state("tensor_type", value)

                    @property
                    def is_extensive(self) -> Boolean:
                        """'is_extensive' property of 'variable' object"""
                        return self.get_property_state("is_extensive")

                    @is_extensive.setter
                    def is_extensive(self, value: Boolean):
                        self.set_property_state("is_extensive", value)

            class region(NamedObject):
                """
                'region' child of 'child_object_type' object
                """

                syc_name = "Region"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'region' object
                    """

                    syc_name = "child_object_type"
                    property_names_types = [
                        ("topology", "Topology", "String"),
                        ("input_variables", "InputVariables", "StringList"),
                        ("output_variables", "OutputVariables", "StringList"),
                        ("display_name", "DisplayName", "String"),
                    ]

                    @property
                    def topology(self) -> String:
                        """'topology' property of 'region' object"""
                        return self.get_property_state("topology")

                    @topology.setter
                    def topology(self, value: String):
                        self.set_property_state("topology", value)

                    @property
                    def input_variables(self) -> StringList:
                        """'input_variables' property of 'region' object"""
                        return self.get_property_state("input_variables")

                    @input_variables.setter
                    def input_variables(self, value: StringList):
                        self.set_property_state("input_variables", value)

                    @property
                    def output_variables(self) -> StringList:
                        """'output_variables' property of 'region' object"""
                        return self.get_property_state("output_variables")

                    @output_variables.setter
                    def output_variables(self, value: StringList):
                        self.set_property_state("output_variables", value)

                    @property
                    def display_name(self) -> String:
                        """'display_name' property of 'region' object"""
                        return self.get_property_state("display_name")

                    @display_name.setter
                    def display_name(self, value: String):
                        self.set_property_state("display_name", value)

            class update_control(Group):
                """
                'update_control' child of 'child_object_type' object
                """

                syc_name = "UpdateControl"
                property_names_types = [
                    ("option", "Option", "String"),
                    ("update_frequency", "UpdateFrequency", "Integer"),
                ]

                @property
                def option(self) -> String:
                    """'option' property of 'child_object_type' object"""
                    return self.get_property_state("option")

                @option.setter
                def option(self, value: String):
                    self.set_property_state("option", value)

                @property
                def update_frequency(self) -> Integer:
                    """'update_frequency' property of 'child_object_type' object"""
                    return self.get_property_state("update_frequency")

                @update_frequency.setter
                def update_frequency(self, value: Integer):
                    self.set_property_state("update_frequency", value)

            class fmu_parameter(NamedObject):
                """
                'fmu_parameter' child of 'child_object_type' object
                """

                syc_name = "FMUParameter"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'fmu_parameter' object
                    """

                    syc_name = "child_object_type"
                    property_names_types = [
                        ("data_type", "DataType", "String"),
                        (
                            "participant_display_name",
                            "ParticipantDisplayName",
                            "String",
                        ),
                        ("display_name", "DisplayName", "String"),
                        ("real_value", "RealValue", "Real"),
                        ("real_min", "RealMin", "Real"),
                        ("real_max", "RealMax", "Real"),
                        ("integer_value", "IntegerValue", "Integer"),
                        ("integer_min", "IntegerMin", "Integer"),
                        ("integer_max", "IntegerMax", "Integer"),
                        ("logical_value", "LogicalValue", "Boolean"),
                        ("string_value", "StringValue", "String"),
                    ]

                    @property
                    def data_type(self) -> String:
                        """'data_type' property of 'fmu_parameter' object"""
                        return self.get_property_state("data_type")

                    @data_type.setter
                    def data_type(self, value: String):
                        self.set_property_state("data_type", value)

                    @property
                    def participant_display_name(self) -> String:
                        """'participant_display_name' property of 'fmu_parameter' object"""
                        return self.get_property_state("participant_display_name")

                    @participant_display_name.setter
                    def participant_display_name(self, value: String):
                        self.set_property_state("participant_display_name", value)

                    @property
                    def display_name(self) -> String:
                        """'display_name' property of 'fmu_parameter' object"""
                        return self.get_property_state("display_name")

                    @display_name.setter
                    def display_name(self, value: String):
                        self.set_property_state("display_name", value)

                    @property
                    def real_value(self) -> Real:
                        """'real_value' property of 'fmu_parameter' object"""
                        return self.get_property_state("real_value")

                    @real_value.setter
                    def real_value(self, value: Real):
                        self.set_property_state("real_value", value)

                    @property
                    def real_min(self) -> Real:
                        """'real_min' property of 'fmu_parameter' object"""
                        return self.get_property_state("real_min")

                    @real_min.setter
                    def real_min(self, value: Real):
                        self.set_property_state("real_min", value)

                    @property
                    def real_max(self) -> Real:
                        """'real_max' property of 'fmu_parameter' object"""
                        return self.get_property_state("real_max")

                    @real_max.setter
                    def real_max(self, value: Real):
                        self.set_property_state("real_max", value)

                    @property
                    def integer_value(self) -> Integer:
                        """'integer_value' property of 'fmu_parameter' object"""
                        return self.get_property_state("integer_value")

                    @integer_value.setter
                    def integer_value(self, value: Integer):
                        self.set_property_state("integer_value", value)

                    @property
                    def integer_min(self) -> Integer:
                        """'integer_min' property of 'fmu_parameter' object"""
                        return self.get_property_state("integer_min")

                    @integer_min.setter
                    def integer_min(self, value: Integer):
                        self.set_property_state("integer_min", value)

                    @property
                    def integer_max(self) -> Integer:
                        """'integer_max' property of 'fmu_parameter' object"""
                        return self.get_property_state("integer_max")

                    @integer_max.setter
                    def integer_max(self, value: Integer):
                        self.set_property_state("integer_max", value)

                    @property
                    def logical_value(self) -> Boolean:
                        """'logical_value' property of 'fmu_parameter' object"""
                        return self.get_property_state("logical_value")

                    @logical_value.setter
                    def logical_value(self, value: Boolean):
                        self.set_property_state("logical_value", value)

                    @property
                    def string_value(self) -> String:
                        """'string_value' property of 'fmu_parameter' object"""
                        return self.get_property_state("string_value")

                    @string_value.setter
                    def string_value(self, value: String):
                        self.set_property_state("string_value", value)

            class execution_control(Group):
                """
                'execution_control' child of 'child_object_type' object
                """

                syc_name = "ExecutionControl"
                child_names = ["fluent_input"]

                class fluent_input(Group):
                    """
                    'fluent_input' child of 'execution_control' object
                    """

                    syc_name = "FluentInput"
                    property_names_types = [
                        ("option", "Option", "String"),
                        ("case_file", "CaseFile", "String"),
                        ("data_file", "DataFile", "String"),
                        ("journal_file", "JournalFile", "String"),
                    ]

                    @property
                    def option(self) -> String:
                        """'option' property of 'execution_control' object"""
                        return self.get_property_state("option")

                    @option.setter
                    def option(self, value: String):
                        self.set_property_state("option", value)

                    @property
                    def case_file(self) -> String:
                        """'case_file' property of 'execution_control' object"""
                        return self.get_property_state("case_file")

                    @case_file.setter
                    def case_file(self, value: String):
                        self.set_property_state("case_file", value)

                    @property
                    def data_file(self) -> String:
                        """'data_file' property of 'execution_control' object"""
                        return self.get_property_state("data_file")

                    @data_file.setter
                    def data_file(self, value: String):
                        self.set_property_state("data_file", value)

                    @property
                    def journal_file(self) -> String:
                        """'journal_file' property of 'execution_control' object"""
                        return self.get_property_state("journal_file")

                    @journal_file.setter
                    def journal_file(self, value: String):
                        self.set_property_state("journal_file", value)

                property_names_types = [
                    ("option", "Option", "String"),
                    ("working_directory", "WorkingDirectory", "String"),
                    ("executable", "Executable", "String"),
                    ("additional_arguments", "AdditionalArguments", "String"),
                    ("parallel_fraction", "ParallelFraction", "Real"),
                    ("initial_input", "InitialInput", "String"),
                    (
                        "additional_restart_input_file",
                        "AdditionalRestartInputFile",
                        "String",
                    ),
                    ("gui_mode", "GuiMode", "Boolean"),
                ]

                @property
                def option(self) -> String:
                    """'option' property of 'child_object_type' object"""
                    return self.get_property_state("option")

                @option.setter
                def option(self, value: String):
                    self.set_property_state("option", value)

                @property
                def working_directory(self) -> String:
                    """'working_directory' property of 'child_object_type' object"""
                    return self.get_property_state("working_directory")

                @working_directory.setter
                def working_directory(self, value: String):
                    self.set_property_state("working_directory", value)

                @property
                def executable(self) -> String:
                    """'executable' property of 'child_object_type' object"""
                    return self.get_property_state("executable")

                @executable.setter
                def executable(self, value: String):
                    self.set_property_state("executable", value)

                @property
                def additional_arguments(self) -> String:
                    """'additional_arguments' property of 'child_object_type' object"""
                    return self.get_property_state("additional_arguments")

                @additional_arguments.setter
                def additional_arguments(self, value: String):
                    self.set_property_state("additional_arguments", value)

                @property
                def parallel_fraction(self) -> Real:
                    """'parallel_fraction' property of 'child_object_type' object"""
                    return self.get_property_state("parallel_fraction")

                @parallel_fraction.setter
                def parallel_fraction(self, value: Real):
                    self.set_property_state("parallel_fraction", value)

                @property
                def initial_input(self) -> String:
                    """'initial_input' property of 'child_object_type' object"""
                    return self.get_property_state("initial_input")

                @initial_input.setter
                def initial_input(self, value: String):
                    self.set_property_state("initial_input", value)

                @property
                def additional_restart_input_file(self) -> String:
                    """'additional_restart_input_file' property of 'child_object_type' object"""
                    return self.get_property_state("additional_restart_input_file")

                @additional_restart_input_file.setter
                def additional_restart_input_file(self, value: String):
                    self.set_property_state("additional_restart_input_file", value)

                @property
                def gui_mode(self) -> Boolean:
                    """'gui_mode' property of 'child_object_type' object"""
                    return self.get_property_state("gui_mode")

                @gui_mode.setter
                def gui_mode(self, value: Boolean):
                    self.set_property_state("gui_mode", value)

            class external_data_file(Group):
                """
                'external_data_file' child of 'child_object_type' object
                """

                syc_name = "ExternalDataFile"
                property_names_types = [("file_path", "FilePath", "String")]

                @property
                def file_path(self) -> String:
                    """'file_path' property of 'child_object_type' object"""
                    return self.get_property_state("file_path")

                @file_path.setter
                def file_path(self, value: String):
                    self.set_property_state("file_path", value)

            property_names_types = [
                ("participant_type", "ParticipantType", "String"),
                ("participant_display_name", "ParticipantDisplayName", "String"),
                ("display_name", "DisplayName", "String"),
                ("participant_file_loaded", "ParticipantFileLoaded", "String"),
                ("logging_on", "LoggingOn", "Boolean"),
                ("participant_analysis_type", "ParticipantAnalysisType", "String"),
                ("use_new_ap_is", "UseNewAPIs", "Boolean"),
                ("restarts_supported", "RestartsSupported", "Boolean"),
            ]

            @property
            def participant_type(self) -> String:
                """'participant_type' property of 'coupling_participant' object"""
                return self.get_property_state("participant_type")

            @participant_type.setter
            def participant_type(self, value: String):
                self.set_property_state("participant_type", value)

            @property
            def participant_display_name(self) -> String:
                """'participant_display_name' property of 'coupling_participant' object"""
                return self.get_property_state("participant_display_name")

            @participant_display_name.setter
            def participant_display_name(self, value: String):
                self.set_property_state("participant_display_name", value)

            @property
            def display_name(self) -> String:
                """'display_name' property of 'coupling_participant' object"""
                return self.get_property_state("display_name")

            @display_name.setter
            def display_name(self, value: String):
                self.set_property_state("display_name", value)

            @property
            def participant_file_loaded(self) -> String:
                """'participant_file_loaded' property of 'coupling_participant' object"""
                return self.get_property_state("participant_file_loaded")

            @participant_file_loaded.setter
            def participant_file_loaded(self, value: String):
                self.set_property_state("participant_file_loaded", value)

            @property
            def logging_on(self) -> Boolean:
                """'logging_on' property of 'coupling_participant' object"""
                return self.get_property_state("logging_on")

            @logging_on.setter
            def logging_on(self, value: Boolean):
                self.set_property_state("logging_on", value)

            @property
            def participant_analysis_type(self) -> String:
                """'participant_analysis_type' property of 'coupling_participant' object"""
                return self.get_property_state("participant_analysis_type")

            @participant_analysis_type.setter
            def participant_analysis_type(self, value: String):
                self.set_property_state("participant_analysis_type", value)

            @property
            def use_new_ap_is(self) -> Boolean:
                """'use_new_ap_is' property of 'coupling_participant' object"""
                return self.get_property_state("use_new_ap_is")

            @use_new_ap_is.setter
            def use_new_ap_is(self, value: Boolean):
                self.set_property_state("use_new_ap_is", value)

            @property
            def restarts_supported(self) -> Boolean:
                """'restarts_supported' property of 'coupling_participant' object"""
                return self.get_property_state("restarts_supported")

            @restarts_supported.setter
            def restarts_supported(self, value: Boolean):
                self.set_property_state("restarts_supported", value)

    class analysis_control(Group):
        """
        'analysis_control' child of 'system_coupling' object
        """

        syc_name = "AnalysisControl"
        child_names = ["global_stabilization", "apip", "unmapped_value_options"]

        class global_stabilization(Group):
            """
            'global_stabilization' child of 'analysis_control' object
            """

            syc_name = "GlobalStabilization"
            property_names_types = [
                ("option", "Option", "String"),
                ("initial_iterations", "InitialIterations", "Integer"),
                ("initial_relaxation_factor", "InitialRelaxationFactor", "Real"),
                ("maximum_retained_time_steps", "MaximumRetainedTimeSteps", "Integer"),
                ("maximum_retained_iterations", "MaximumRetainedIterations", "Integer"),
                ("diagnostics_level", "DiagnosticsLevel", "Integer"),
                ("weight_option", "WeightOption", "String"),
                ("qr_tol_this_step", "QRTolThisStep", "Real"),
                ("qr_tol_old_steps", "QRTolOldSteps", "Real"),
            ]

            @property
            def option(self) -> String:
                """'option' property of 'analysis_control' object"""
                return self.get_property_state("option")

            @option.setter
            def option(self, value: String):
                self.set_property_state("option", value)

            @property
            def initial_iterations(self) -> Integer:
                """'initial_iterations' property of 'analysis_control' object"""
                return self.get_property_state("initial_iterations")

            @initial_iterations.setter
            def initial_iterations(self, value: Integer):
                self.set_property_state("initial_iterations", value)

            @property
            def initial_relaxation_factor(self) -> Real:
                """'initial_relaxation_factor' property of 'analysis_control' object"""
                return self.get_property_state("initial_relaxation_factor")

            @initial_relaxation_factor.setter
            def initial_relaxation_factor(self, value: Real):
                self.set_property_state("initial_relaxation_factor", value)

            @property
            def maximum_retained_time_steps(self) -> Integer:
                """'maximum_retained_time_steps' property of 'analysis_control' object"""
                return self.get_property_state("maximum_retained_time_steps")

            @maximum_retained_time_steps.setter
            def maximum_retained_time_steps(self, value: Integer):
                self.set_property_state("maximum_retained_time_steps", value)

            @property
            def maximum_retained_iterations(self) -> Integer:
                """'maximum_retained_iterations' property of 'analysis_control' object"""
                return self.get_property_state("maximum_retained_iterations")

            @maximum_retained_iterations.setter
            def maximum_retained_iterations(self, value: Integer):
                self.set_property_state("maximum_retained_iterations", value)

            @property
            def diagnostics_level(self) -> Integer:
                """'diagnostics_level' property of 'analysis_control' object"""
                return self.get_property_state("diagnostics_level")

            @diagnostics_level.setter
            def diagnostics_level(self, value: Integer):
                self.set_property_state("diagnostics_level", value)

            @property
            def weight_option(self) -> String:
                """'weight_option' property of 'analysis_control' object"""
                return self.get_property_state("weight_option")

            @weight_option.setter
            def weight_option(self, value: String):
                self.set_property_state("weight_option", value)

            @property
            def qr_tol_this_step(self) -> Real:
                """'qr_tol_this_step' property of 'analysis_control' object"""
                return self.get_property_state("qr_tol_this_step")

            @qr_tol_this_step.setter
            def qr_tol_this_step(self, value: Real):
                self.set_property_state("qr_tol_this_step", value)

            @property
            def qr_tol_old_steps(self) -> Real:
                """'qr_tol_old_steps' property of 'analysis_control' object"""
                return self.get_property_state("qr_tol_old_steps")

            @qr_tol_old_steps.setter
            def qr_tol_old_steps(self, value: Real):
                self.set_property_state("qr_tol_old_steps", value)

        class apip(Group):
            """
            'apip' child of 'analysis_control' object
            """

            syc_name = "Apip"
            property_names_types = [
                ("debug", "Debug", "Boolean"),
                ("disable", "Disable", "Boolean"),
            ]

            @property
            def debug(self) -> Boolean:
                """'debug' property of 'analysis_control' object"""
                return self.get_property_state("debug")

            @debug.setter
            def debug(self, value: Boolean):
                self.set_property_state("debug", value)

            @property
            def disable(self) -> Boolean:
                """'disable' property of 'analysis_control' object"""
                return self.get_property_state("disable")

            @disable.setter
            def disable(self, value: Boolean):
                self.set_property_state("disable", value)

        class unmapped_value_options(Group):
            """
            'unmapped_value_options' child of 'analysis_control' object
            """

            syc_name = "UnmappedValueOptions"
            property_names_types = [
                ("matrix_verbosity", "MatrixVerbosity", "Integer"),
                ("solver_verbosity", "SolverVerbosity", "Integer"),
                ("solver", "Solver", "String"),
                ("solver_relative_tolerance", "SolverRelativeTolerance", "Real"),
                ("solver_max_iterations", "SolverMaxIterations", "Integer"),
                (
                    "solver_max_search_directions",
                    "SolverMaxSearchDirections",
                    "Integer",
                ),
                ("preconditioner", "Preconditioner", "String"),
                ("ilut_tau", "IlutTau", "Real"),
                ("ilut_max_fill", "IlutMaxFill", "Integer"),
                ("ilut_pivot_tol", "IlutPivotTol", "Real"),
                ("face_filter_tolerance", "FaceFilterTolerance", "Real"),
                ("rbf_shape_parameter", "RbfShapeParameter", "Real"),
                ("rbf_linear_correction", "RbfLinearCorrection", "Boolean"),
                ("rbf_colinearity_tolerance", "RbfColinearityTolerance", "Real"),
            ]

            @property
            def matrix_verbosity(self) -> Integer:
                """'matrix_verbosity' property of 'analysis_control' object"""
                return self.get_property_state("matrix_verbosity")

            @matrix_verbosity.setter
            def matrix_verbosity(self, value: Integer):
                self.set_property_state("matrix_verbosity", value)

            @property
            def solver_verbosity(self) -> Integer:
                """'solver_verbosity' property of 'analysis_control' object"""
                return self.get_property_state("solver_verbosity")

            @solver_verbosity.setter
            def solver_verbosity(self, value: Integer):
                self.set_property_state("solver_verbosity", value)

            @property
            def solver(self) -> String:
                """'solver' property of 'analysis_control' object"""
                return self.get_property_state("solver")

            @solver.setter
            def solver(self, value: String):
                self.set_property_state("solver", value)

            @property
            def solver_relative_tolerance(self) -> Real:
                """'solver_relative_tolerance' property of 'analysis_control' object"""
                return self.get_property_state("solver_relative_tolerance")

            @solver_relative_tolerance.setter
            def solver_relative_tolerance(self, value: Real):
                self.set_property_state("solver_relative_tolerance", value)

            @property
            def solver_max_iterations(self) -> Integer:
                """'solver_max_iterations' property of 'analysis_control' object"""
                return self.get_property_state("solver_max_iterations")

            @solver_max_iterations.setter
            def solver_max_iterations(self, value: Integer):
                self.set_property_state("solver_max_iterations", value)

            @property
            def solver_max_search_directions(self) -> Integer:
                """'solver_max_search_directions' property of 'analysis_control' object"""
                return self.get_property_state("solver_max_search_directions")

            @solver_max_search_directions.setter
            def solver_max_search_directions(self, value: Integer):
                self.set_property_state("solver_max_search_directions", value)

            @property
            def preconditioner(self) -> String:
                """'preconditioner' property of 'analysis_control' object"""
                return self.get_property_state("preconditioner")

            @preconditioner.setter
            def preconditioner(self, value: String):
                self.set_property_state("preconditioner", value)

            @property
            def ilut_tau(self) -> Real:
                """'ilut_tau' property of 'analysis_control' object"""
                return self.get_property_state("ilut_tau")

            @ilut_tau.setter
            def ilut_tau(self, value: Real):
                self.set_property_state("ilut_tau", value)

            @property
            def ilut_max_fill(self) -> Integer:
                """'ilut_max_fill' property of 'analysis_control' object"""
                return self.get_property_state("ilut_max_fill")

            @ilut_max_fill.setter
            def ilut_max_fill(self, value: Integer):
                self.set_property_state("ilut_max_fill", value)

            @property
            def ilut_pivot_tol(self) -> Real:
                """'ilut_pivot_tol' property of 'analysis_control' object"""
                return self.get_property_state("ilut_pivot_tol")

            @ilut_pivot_tol.setter
            def ilut_pivot_tol(self, value: Real):
                self.set_property_state("ilut_pivot_tol", value)

            @property
            def face_filter_tolerance(self) -> Real:
                """'face_filter_tolerance' property of 'analysis_control' object"""
                return self.get_property_state("face_filter_tolerance")

            @face_filter_tolerance.setter
            def face_filter_tolerance(self, value: Real):
                self.set_property_state("face_filter_tolerance", value)

            @property
            def rbf_shape_parameter(self) -> Real:
                """'rbf_shape_parameter' property of 'analysis_control' object"""
                return self.get_property_state("rbf_shape_parameter")

            @rbf_shape_parameter.setter
            def rbf_shape_parameter(self, value: Real):
                self.set_property_state("rbf_shape_parameter", value)

            @property
            def rbf_linear_correction(self) -> Boolean:
                """'rbf_linear_correction' property of 'analysis_control' object"""
                return self.get_property_state("rbf_linear_correction")

            @rbf_linear_correction.setter
            def rbf_linear_correction(self, value: Boolean):
                self.set_property_state("rbf_linear_correction", value)

            @property
            def rbf_colinearity_tolerance(self) -> Real:
                """'rbf_colinearity_tolerance' property of 'analysis_control' object"""
                return self.get_property_state("rbf_colinearity_tolerance")

            @rbf_colinearity_tolerance.setter
            def rbf_colinearity_tolerance(self, value: Real):
                self.set_property_state("rbf_colinearity_tolerance", value)

        property_names_types = [
            ("analysis_type", "AnalysisType", "String"),
            ("optimize_if_one_way", "OptimizeIfOneWay", "Boolean"),
            ("allow_simultaneous_update", "AllowSimultaneousUpdate", "Boolean"),
            ("simultaneous_participants", "SimultaneousParticipants", "String"),
            ("partitioning_algorithm", "PartitioningAlgorithm", "String"),
            ("allow_iterations_only_mode", "AllowIterationsOnlyMode", "Boolean"),
            ("target_initialization_option", "TargetInitializationOption", "String"),
            ("fluent_region_update_at_step", "FluentRegionUpdateAtStep", "Boolean"),
            ("mesh_import_on_initialization", "MeshImportOnInitialization", "Boolean"),
            ("import_all_regions", "ImportAllRegions", "Boolean"),
            ("bypass_fluent_adapter", "BypassFluentAdapter", "Boolean"),
            (
                "variable_to_expression_transfer",
                "VariableToExpressionTransfer",
                "Boolean",
            ),
            ("update_mapping_weights", "UpdateMappingWeights", "String"),
            ("rotate_follower_forces", "RotateFollowerForces", "String"),
            (
                "solve_incremental_displacement_first",
                "SolveIncrementalDisplacementFirst",
                "Boolean",
            ),
            ("write_scs_file", "WriteScsFile", "Boolean"),
        ]

        @property
        def analysis_type(self) -> String:
            """'analysis_type' property of 'system_coupling' object"""
            return self.get_property_state("analysis_type")

        @analysis_type.setter
        def analysis_type(self, value: String):
            self.set_property_state("analysis_type", value)

        @property
        def optimize_if_one_way(self) -> Boolean:
            """'optimize_if_one_way' property of 'system_coupling' object"""
            return self.get_property_state("optimize_if_one_way")

        @optimize_if_one_way.setter
        def optimize_if_one_way(self, value: Boolean):
            self.set_property_state("optimize_if_one_way", value)

        @property
        def allow_simultaneous_update(self) -> Boolean:
            """'allow_simultaneous_update' property of 'system_coupling' object"""
            return self.get_property_state("allow_simultaneous_update")

        @allow_simultaneous_update.setter
        def allow_simultaneous_update(self, value: Boolean):
            self.set_property_state("allow_simultaneous_update", value)

        @property
        def simultaneous_participants(self) -> String:
            """'simultaneous_participants' property of 'system_coupling' object"""
            return self.get_property_state("simultaneous_participants")

        @simultaneous_participants.setter
        def simultaneous_participants(self, value: String):
            self.set_property_state("simultaneous_participants", value)

        @property
        def partitioning_algorithm(self) -> String:
            """'partitioning_algorithm' property of 'system_coupling' object"""
            return self.get_property_state("partitioning_algorithm")

        @partitioning_algorithm.setter
        def partitioning_algorithm(self, value: String):
            self.set_property_state("partitioning_algorithm", value)

        @property
        def allow_iterations_only_mode(self) -> Boolean:
            """'allow_iterations_only_mode' property of 'system_coupling' object"""
            return self.get_property_state("allow_iterations_only_mode")

        @allow_iterations_only_mode.setter
        def allow_iterations_only_mode(self, value: Boolean):
            self.set_property_state("allow_iterations_only_mode", value)

        @property
        def target_initialization_option(self) -> String:
            """'target_initialization_option' property of 'system_coupling' object"""
            return self.get_property_state("target_initialization_option")

        @target_initialization_option.setter
        def target_initialization_option(self, value: String):
            self.set_property_state("target_initialization_option", value)

        @property
        def fluent_region_update_at_step(self) -> Boolean:
            """'fluent_region_update_at_step' property of 'system_coupling' object"""
            return self.get_property_state("fluent_region_update_at_step")

        @fluent_region_update_at_step.setter
        def fluent_region_update_at_step(self, value: Boolean):
            self.set_property_state("fluent_region_update_at_step", value)

        @property
        def mesh_import_on_initialization(self) -> Boolean:
            """'mesh_import_on_initialization' property of 'system_coupling' object"""
            return self.get_property_state("mesh_import_on_initialization")

        @mesh_import_on_initialization.setter
        def mesh_import_on_initialization(self, value: Boolean):
            self.set_property_state("mesh_import_on_initialization", value)

        @property
        def import_all_regions(self) -> Boolean:
            """'import_all_regions' property of 'system_coupling' object"""
            return self.get_property_state("import_all_regions")

        @import_all_regions.setter
        def import_all_regions(self, value: Boolean):
            self.set_property_state("import_all_regions", value)

        @property
        def bypass_fluent_adapter(self) -> Boolean:
            """'bypass_fluent_adapter' property of 'system_coupling' object"""
            return self.get_property_state("bypass_fluent_adapter")

        @bypass_fluent_adapter.setter
        def bypass_fluent_adapter(self, value: Boolean):
            self.set_property_state("bypass_fluent_adapter", value)

        @property
        def variable_to_expression_transfer(self) -> Boolean:
            """'variable_to_expression_transfer' property of 'system_coupling' object"""
            return self.get_property_state("variable_to_expression_transfer")

        @variable_to_expression_transfer.setter
        def variable_to_expression_transfer(self, value: Boolean):
            self.set_property_state("variable_to_expression_transfer", value)

        @property
        def update_mapping_weights(self) -> String:
            """'update_mapping_weights' property of 'system_coupling' object"""
            return self.get_property_state("update_mapping_weights")

        @update_mapping_weights.setter
        def update_mapping_weights(self, value: String):
            self.set_property_state("update_mapping_weights", value)

        @property
        def rotate_follower_forces(self) -> String:
            """'rotate_follower_forces' property of 'system_coupling' object"""
            return self.get_property_state("rotate_follower_forces")

        @rotate_follower_forces.setter
        def rotate_follower_forces(self, value: String):
            self.set_property_state("rotate_follower_forces", value)

        @property
        def solve_incremental_displacement_first(self) -> Boolean:
            """'solve_incremental_displacement_first' property of 'system_coupling' object"""
            return self.get_property_state("solve_incremental_displacement_first")

        @solve_incremental_displacement_first.setter
        def solve_incremental_displacement_first(self, value: Boolean):
            self.set_property_state("solve_incremental_displacement_first", value)

        @property
        def write_scs_file(self) -> Boolean:
            """'write_scs_file' property of 'system_coupling' object"""
            return self.get_property_state("write_scs_file")

        @write_scs_file.setter
        def write_scs_file(self, value: Boolean):
            self.set_property_state("write_scs_file", value)

    class coupling_interface(NamedObject):
        """
        'coupling_interface' child of 'system_coupling' object
        """

        syc_name = "CouplingInterface"

        class child_object_type(Group):
            """
            'child_object_type' child of 'coupling_interface' object
            """

            syc_name = "child_object_type"
            child_names = ["side", "data_transfer", "mapping_control"]

            class side(NamedObject):
                """
                'side' child of 'child_object_type' object
                """

                syc_name = "Side"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'side' object
                    """

                    syc_name = "child_object_type"
                    property_names_types = [
                        ("coupling_participant", "CouplingParticipant", "String"),
                        ("region_list", "RegionList", "StringList"),
                        ("reference_frame", "ReferenceFrame", "String"),
                        ("instancing", "Instancing", "String"),
                    ]

                    @property
                    def coupling_participant(self) -> String:
                        """'coupling_participant' property of 'side' object"""
                        return self.get_property_state("coupling_participant")

                    @coupling_participant.setter
                    def coupling_participant(self, value: String):
                        self.set_property_state("coupling_participant", value)

                    @property
                    def region_list(self) -> StringList:
                        """'region_list' property of 'side' object"""
                        return self.get_property_state("region_list")

                    @region_list.setter
                    def region_list(self, value: StringList):
                        self.set_property_state("region_list", value)

                    @property
                    def reference_frame(self) -> String:
                        """'reference_frame' property of 'side' object"""
                        return self.get_property_state("reference_frame")

                    @reference_frame.setter
                    def reference_frame(self, value: String):
                        self.set_property_state("reference_frame", value)

                    @property
                    def instancing(self) -> String:
                        """'instancing' property of 'side' object"""
                        return self.get_property_state("instancing")

                    @instancing.setter
                    def instancing(self, value: String):
                        self.set_property_state("instancing", value)

            class data_transfer(NamedObject):
                """
                'data_transfer' child of 'child_object_type' object
                """

                syc_name = "DataTransfer"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'data_transfer' object
                    """

                    syc_name = "child_object_type"
                    child_names = ["stabilization"]

                    class stabilization(Group):
                        """
                        'stabilization' child of 'child_object_type' object
                        """

                        syc_name = "Stabilization"
                        property_names_types = [
                            ("option", "Option", "String"),
                            (
                                "couple_with_global_stabilization",
                                "CoupleWithGlobalStabilization",
                                "Boolean",
                            ),
                            ("initial_iterations", "InitialIterations", "Integer"),
                            (
                                "initial_relaxation_factor",
                                "InitialRelaxationFactor",
                                "Real",
                            ),
                            (
                                "maximum_retained_time_steps",
                                "MaximumRetainedTimeSteps",
                                "Integer",
                            ),
                            (
                                "maximum_retained_iterations",
                                "MaximumRetainedIterations",
                                "Integer",
                            ),
                            ("weight_factor", "WeightFactor", "Real"),
                            ("diagnostics_level", "DiagnosticsLevel", "Integer"),
                            ("weight_option", "WeightOption", "String"),
                            ("qr_tol_this_step", "QRTolThisStep", "Real"),
                            ("qr_tol_old_steps", "QRTolOldSteps", "Real"),
                            (
                                "time_step_initialization_option",
                                "TimeStepInitializationOption",
                                "String",
                            ),
                        ]

                        @property
                        def option(self) -> String:
                            """'option' property of 'child_object_type' object"""
                            return self.get_property_state("option")

                        @option.setter
                        def option(self, value: String):
                            self.set_property_state("option", value)

                        @property
                        def couple_with_global_stabilization(self) -> Boolean:
                            """'couple_with_global_stabilization' property of 'child_object_type' object"""
                            return self.get_property_state(
                                "couple_with_global_stabilization"
                            )

                        @couple_with_global_stabilization.setter
                        def couple_with_global_stabilization(self, value: Boolean):
                            self.set_property_state(
                                "couple_with_global_stabilization", value
                            )

                        @property
                        def initial_iterations(self) -> Integer:
                            """'initial_iterations' property of 'child_object_type' object"""
                            return self.get_property_state("initial_iterations")

                        @initial_iterations.setter
                        def initial_iterations(self, value: Integer):
                            self.set_property_state("initial_iterations", value)

                        @property
                        def initial_relaxation_factor(self) -> Real:
                            """'initial_relaxation_factor' property of 'child_object_type' object"""
                            return self.get_property_state("initial_relaxation_factor")

                        @initial_relaxation_factor.setter
                        def initial_relaxation_factor(self, value: Real):
                            self.set_property_state("initial_relaxation_factor", value)

                        @property
                        def maximum_retained_time_steps(self) -> Integer:
                            """'maximum_retained_time_steps' property of 'child_object_type' object"""
                            return self.get_property_state(
                                "maximum_retained_time_steps"
                            )

                        @maximum_retained_time_steps.setter
                        def maximum_retained_time_steps(self, value: Integer):
                            self.set_property_state(
                                "maximum_retained_time_steps", value
                            )

                        @property
                        def maximum_retained_iterations(self) -> Integer:
                            """'maximum_retained_iterations' property of 'child_object_type' object"""
                            return self.get_property_state(
                                "maximum_retained_iterations"
                            )

                        @maximum_retained_iterations.setter
                        def maximum_retained_iterations(self, value: Integer):
                            self.set_property_state(
                                "maximum_retained_iterations", value
                            )

                        @property
                        def weight_factor(self) -> Real:
                            """'weight_factor' property of 'child_object_type' object"""
                            return self.get_property_state("weight_factor")

                        @weight_factor.setter
                        def weight_factor(self, value: Real):
                            self.set_property_state("weight_factor", value)

                        @property
                        def diagnostics_level(self) -> Integer:
                            """'diagnostics_level' property of 'child_object_type' object"""
                            return self.get_property_state("diagnostics_level")

                        @diagnostics_level.setter
                        def diagnostics_level(self, value: Integer):
                            self.set_property_state("diagnostics_level", value)

                        @property
                        def weight_option(self) -> String:
                            """'weight_option' property of 'child_object_type' object"""
                            return self.get_property_state("weight_option")

                        @weight_option.setter
                        def weight_option(self, value: String):
                            self.set_property_state("weight_option", value)

                        @property
                        def qr_tol_this_step(self) -> Real:
                            """'qr_tol_this_step' property of 'child_object_type' object"""
                            return self.get_property_state("qr_tol_this_step")

                        @qr_tol_this_step.setter
                        def qr_tol_this_step(self, value: Real):
                            self.set_property_state("qr_tol_this_step", value)

                        @property
                        def qr_tol_old_steps(self) -> Real:
                            """'qr_tol_old_steps' property of 'child_object_type' object"""
                            return self.get_property_state("qr_tol_old_steps")

                        @qr_tol_old_steps.setter
                        def qr_tol_old_steps(self, value: Real):
                            self.set_property_state("qr_tol_old_steps", value)

                        @property
                        def time_step_initialization_option(self) -> String:
                            """'time_step_initialization_option' property of 'child_object_type' object"""
                            return self.get_property_state(
                                "time_step_initialization_option"
                            )

                        @time_step_initialization_option.setter
                        def time_step_initialization_option(self, value: String):
                            self.set_property_state(
                                "time_step_initialization_option", value
                            )

                    property_names_types = [
                        ("display_name", "DisplayName", "String"),
                        ("suppress", "Suppress", "Boolean"),
                        ("target_side", "TargetSide", "String"),
                        ("option", "Option", "String"),
                        ("source_variable", "SourceVariable", "String"),
                        ("target_variable", "TargetVariable", "String"),
                        ("value", "Value", "Real"),
                        ("ramping_option", "RampingOption", "String"),
                        ("relaxation_factor", "RelaxationFactor", "Real"),
                        ("convergence_target", "ConvergenceTarget", "Real"),
                        ("mapping_type", "MappingType", "String"),
                        ("unmapped_value_option", "UnmappedValueOption", "String"),
                        (
                            "time_step_initialization_option",
                            "TimeStepInitializationOption",
                            "String",
                        ),
                    ]

                    @property
                    def display_name(self) -> String:
                        """'display_name' property of 'data_transfer' object"""
                        return self.get_property_state("display_name")

                    @display_name.setter
                    def display_name(self, value: String):
                        self.set_property_state("display_name", value)

                    @property
                    def suppress(self) -> Boolean:
                        """'suppress' property of 'data_transfer' object"""
                        return self.get_property_state("suppress")

                    @suppress.setter
                    def suppress(self, value: Boolean):
                        self.set_property_state("suppress", value)

                    @property
                    def target_side(self) -> String:
                        """'target_side' property of 'data_transfer' object"""
                        return self.get_property_state("target_side")

                    @target_side.setter
                    def target_side(self, value: String):
                        self.set_property_state("target_side", value)

                    @property
                    def option(self) -> String:
                        """'option' property of 'data_transfer' object"""
                        return self.get_property_state("option")

                    @option.setter
                    def option(self, value: String):
                        self.set_property_state("option", value)

                    @property
                    def source_variable(self) -> String:
                        """'source_variable' property of 'data_transfer' object"""
                        return self.get_property_state("source_variable")

                    @source_variable.setter
                    def source_variable(self, value: String):
                        self.set_property_state("source_variable", value)

                    @property
                    def target_variable(self) -> String:
                        """'target_variable' property of 'data_transfer' object"""
                        return self.get_property_state("target_variable")

                    @target_variable.setter
                    def target_variable(self, value: String):
                        self.set_property_state("target_variable", value)

                    @property
                    def value(self) -> Real:
                        """'value' property of 'data_transfer' object"""
                        return self.get_property_state("value")

                    @value.setter
                    def value(self, value: Real):
                        self.set_property_state("value", value)

                    @property
                    def ramping_option(self) -> String:
                        """'ramping_option' property of 'data_transfer' object"""
                        return self.get_property_state("ramping_option")

                    @ramping_option.setter
                    def ramping_option(self, value: String):
                        self.set_property_state("ramping_option", value)

                    @property
                    def relaxation_factor(self) -> Real:
                        """'relaxation_factor' property of 'data_transfer' object"""
                        return self.get_property_state("relaxation_factor")

                    @relaxation_factor.setter
                    def relaxation_factor(self, value: Real):
                        self.set_property_state("relaxation_factor", value)

                    @property
                    def convergence_target(self) -> Real:
                        """'convergence_target' property of 'data_transfer' object"""
                        return self.get_property_state("convergence_target")

                    @convergence_target.setter
                    def convergence_target(self, value: Real):
                        self.set_property_state("convergence_target", value)

                    @property
                    def mapping_type(self) -> String:
                        """'mapping_type' property of 'data_transfer' object"""
                        return self.get_property_state("mapping_type")

                    @mapping_type.setter
                    def mapping_type(self, value: String):
                        self.set_property_state("mapping_type", value)

                    @property
                    def unmapped_value_option(self) -> String:
                        """'unmapped_value_option' property of 'data_transfer' object"""
                        return self.get_property_state("unmapped_value_option")

                    @unmapped_value_option.setter
                    def unmapped_value_option(self, value: String):
                        self.set_property_state("unmapped_value_option", value)

                    @property
                    def time_step_initialization_option(self) -> String:
                        """'time_step_initialization_option' property of 'data_transfer' object"""
                        return self.get_property_state(
                            "time_step_initialization_option"
                        )

                    @time_step_initialization_option.setter
                    def time_step_initialization_option(self, value: String):
                        self.set_property_state(
                            "time_step_initialization_option", value
                        )

            class mapping_control(Group):
                """
                'mapping_control' child of 'child_object_type' object
                """

                syc_name = "MappingControl"
                property_names_types = [
                    ("stop_if_poor_intersection", "StopIfPoorIntersection", "Boolean"),
                    (
                        "poor_intersection_threshold",
                        "PoorIntersectionThreshold",
                        "Real",
                    ),
                    ("face_alignment", "FaceAlignment", "String"),
                    ("absolute_gap_tolerance", "AbsoluteGapTolerance", "Real"),
                    ("relative_gap_tolerance", "RelativeGapTolerance", "Real"),
                    ("small_weight_tolerance", "SmallWeightTolerance", "Real"),
                    ("corner_tolerance", "CornerTolerance", "Real"),
                    ("halo_tolerance", "HaloTolerance", "Real"),
                    (
                        "conservative_reciprocity_factor",
                        "ConservativeReciprocityFactor",
                        "Real",
                    ),
                    (
                        "profile_preserving_reciprocity_factor",
                        "ProfilePreservingReciprocityFactor",
                        "Real",
                    ),
                    ("conservative_intensive", "ConservativeIntensive", "String"),
                    ("preserve_normal", "PreserveNormal", "String"),
                    (
                        "conservation_fix_tolerance_volume",
                        "ConservationFixToleranceVolume",
                        "Real",
                    ),
                    ("rbf_option", "RBFOption", "String"),
                    ("rbf_shape_parameter", "RBFShapeParameter", "Real"),
                    ("rbf_linear_correction", "RBFLinearCorrection", "Boolean"),
                    ("rbf_clipping_scale", "RBFClippingScale", "Real"),
                ]

                @property
                def stop_if_poor_intersection(self) -> Boolean:
                    """'stop_if_poor_intersection' property of 'child_object_type' object"""
                    return self.get_property_state("stop_if_poor_intersection")

                @stop_if_poor_intersection.setter
                def stop_if_poor_intersection(self, value: Boolean):
                    self.set_property_state("stop_if_poor_intersection", value)

                @property
                def poor_intersection_threshold(self) -> Real:
                    """'poor_intersection_threshold' property of 'child_object_type' object"""
                    return self.get_property_state("poor_intersection_threshold")

                @poor_intersection_threshold.setter
                def poor_intersection_threshold(self, value: Real):
                    self.set_property_state("poor_intersection_threshold", value)

                @property
                def face_alignment(self) -> String:
                    """'face_alignment' property of 'child_object_type' object"""
                    return self.get_property_state("face_alignment")

                @face_alignment.setter
                def face_alignment(self, value: String):
                    self.set_property_state("face_alignment", value)

                @property
                def absolute_gap_tolerance(self) -> Real:
                    """'absolute_gap_tolerance' property of 'child_object_type' object"""
                    return self.get_property_state("absolute_gap_tolerance")

                @absolute_gap_tolerance.setter
                def absolute_gap_tolerance(self, value: Real):
                    self.set_property_state("absolute_gap_tolerance", value)

                @property
                def relative_gap_tolerance(self) -> Real:
                    """'relative_gap_tolerance' property of 'child_object_type' object"""
                    return self.get_property_state("relative_gap_tolerance")

                @relative_gap_tolerance.setter
                def relative_gap_tolerance(self, value: Real):
                    self.set_property_state("relative_gap_tolerance", value)

                @property
                def small_weight_tolerance(self) -> Real:
                    """'small_weight_tolerance' property of 'child_object_type' object"""
                    return self.get_property_state("small_weight_tolerance")

                @small_weight_tolerance.setter
                def small_weight_tolerance(self, value: Real):
                    self.set_property_state("small_weight_tolerance", value)

                @property
                def corner_tolerance(self) -> Real:
                    """'corner_tolerance' property of 'child_object_type' object"""
                    return self.get_property_state("corner_tolerance")

                @corner_tolerance.setter
                def corner_tolerance(self, value: Real):
                    self.set_property_state("corner_tolerance", value)

                @property
                def halo_tolerance(self) -> Real:
                    """'halo_tolerance' property of 'child_object_type' object"""
                    return self.get_property_state("halo_tolerance")

                @halo_tolerance.setter
                def halo_tolerance(self, value: Real):
                    self.set_property_state("halo_tolerance", value)

                @property
                def conservative_reciprocity_factor(self) -> Real:
                    """'conservative_reciprocity_factor' property of 'child_object_type' object"""
                    return self.get_property_state("conservative_reciprocity_factor")

                @conservative_reciprocity_factor.setter
                def conservative_reciprocity_factor(self, value: Real):
                    self.set_property_state("conservative_reciprocity_factor", value)

                @property
                def profile_preserving_reciprocity_factor(self) -> Real:
                    """'profile_preserving_reciprocity_factor' property of 'child_object_type' object"""
                    return self.get_property_state(
                        "profile_preserving_reciprocity_factor"
                    )

                @profile_preserving_reciprocity_factor.setter
                def profile_preserving_reciprocity_factor(self, value: Real):
                    self.set_property_state(
                        "profile_preserving_reciprocity_factor", value
                    )

                @property
                def conservative_intensive(self) -> String:
                    """'conservative_intensive' property of 'child_object_type' object"""
                    return self.get_property_state("conservative_intensive")

                @conservative_intensive.setter
                def conservative_intensive(self, value: String):
                    self.set_property_state("conservative_intensive", value)

                @property
                def preserve_normal(self) -> String:
                    """'preserve_normal' property of 'child_object_type' object"""
                    return self.get_property_state("preserve_normal")

                @preserve_normal.setter
                def preserve_normal(self, value: String):
                    self.set_property_state("preserve_normal", value)

                @property
                def conservation_fix_tolerance_volume(self) -> Real:
                    """'conservation_fix_tolerance_volume' property of 'child_object_type' object"""
                    return self.get_property_state("conservation_fix_tolerance_volume")

                @conservation_fix_tolerance_volume.setter
                def conservation_fix_tolerance_volume(self, value: Real):
                    self.set_property_state("conservation_fix_tolerance_volume", value)

                @property
                def rbf_option(self) -> String:
                    """'rbf_option' property of 'child_object_type' object"""
                    return self.get_property_state("rbf_option")

                @rbf_option.setter
                def rbf_option(self, value: String):
                    self.set_property_state("rbf_option", value)

                @property
                def rbf_shape_parameter(self) -> Real:
                    """'rbf_shape_parameter' property of 'child_object_type' object"""
                    return self.get_property_state("rbf_shape_parameter")

                @rbf_shape_parameter.setter
                def rbf_shape_parameter(self, value: Real):
                    self.set_property_state("rbf_shape_parameter", value)

                @property
                def rbf_linear_correction(self) -> Boolean:
                    """'rbf_linear_correction' property of 'child_object_type' object"""
                    return self.get_property_state("rbf_linear_correction")

                @rbf_linear_correction.setter
                def rbf_linear_correction(self, value: Boolean):
                    self.set_property_state("rbf_linear_correction", value)

                @property
                def rbf_clipping_scale(self) -> Real:
                    """'rbf_clipping_scale' property of 'child_object_type' object"""
                    return self.get_property_state("rbf_clipping_scale")

                @rbf_clipping_scale.setter
                def rbf_clipping_scale(self, value: Real):
                    self.set_property_state("rbf_clipping_scale", value)

            property_names_types = [("display_name", "DisplayName", "String")]

            @property
            def display_name(self) -> String:
                """'display_name' property of 'coupling_interface' object"""
                return self.get_property_state("display_name")

            @display_name.setter
            def display_name(self, value: String):
                self.set_property_state("display_name", value)

    class solution_control(Group):
        """
        'solution_control' child of 'system_coupling' object
        """

        syc_name = "SolutionControl"
        child_names = ["available_ports"]

        class available_ports(Group):
            """
            'available_ports' child of 'solution_control' object
            """

            syc_name = "AvailablePorts"
            property_names_types = [
                ("option", "Option", "String"),
                ("range", "Range", "String"),
            ]

            @property
            def option(self) -> String:
                """'option' property of 'solution_control' object"""
                return self.get_property_state("option")

            @option.setter
            def option(self, value: String):
                self.set_property_state("option", value)

            @property
            def range(self) -> String:
                """'range' property of 'solution_control' object"""
                return self.get_property_state("range")

            @range.setter
            def range(self, value: String):
                self.set_property_state("range", value)

        property_names_types = [
            ("duration_option", "DurationOption", "String"),
            ("end_time", "EndTime", "Real"),
            ("number_of_steps", "NumberOfSteps", "Integer"),
            ("time_step_size", "TimeStepSize", "Real"),
            ("minimum_iterations", "MinimumIterations", "Integer"),
            ("maximum_iterations", "MaximumIterations", "Integer"),
        ]

        @property
        def duration_option(self) -> String:
            """'duration_option' property of 'system_coupling' object"""
            return self.get_property_state("duration_option")

        @duration_option.setter
        def duration_option(self, value: String):
            self.set_property_state("duration_option", value)

        @property
        def end_time(self) -> Real:
            """'end_time' property of 'system_coupling' object"""
            return self.get_property_state("end_time")

        @end_time.setter
        def end_time(self, value: Real):
            self.set_property_state("end_time", value)

        @property
        def number_of_steps(self) -> Integer:
            """'number_of_steps' property of 'system_coupling' object"""
            return self.get_property_state("number_of_steps")

        @number_of_steps.setter
        def number_of_steps(self, value: Integer):
            self.set_property_state("number_of_steps", value)

        @property
        def time_step_size(self) -> Real:
            """'time_step_size' property of 'system_coupling' object"""
            return self.get_property_state("time_step_size")

        @time_step_size.setter
        def time_step_size(self, value: Real):
            self.set_property_state("time_step_size", value)

        @property
        def minimum_iterations(self) -> Integer:
            """'minimum_iterations' property of 'system_coupling' object"""
            return self.get_property_state("minimum_iterations")

        @minimum_iterations.setter
        def minimum_iterations(self, value: Integer):
            self.set_property_state("minimum_iterations", value)

        @property
        def maximum_iterations(self) -> Integer:
            """'maximum_iterations' property of 'system_coupling' object"""
            return self.get_property_state("maximum_iterations")

        @maximum_iterations.setter
        def maximum_iterations(self, value: Integer):
            self.set_property_state("maximum_iterations", value)

    class output_control(Group):
        """
        'output_control' child of 'system_coupling' object
        """

        syc_name = "OutputControl"
        child_names = ["results", "ascii_output"]

        class results(Group):
            """
            'results' child of 'output_control' object
            """

            syc_name = "Results"
            child_names = ["type"]

            class type(Group):
                """
                'type' child of 'results' object
                """

                syc_name = "Type"
                property_names_types = [
                    ("option", "Option", "String"),
                    ("binary_format", "BinaryFormat", "Boolean"),
                ]

                @property
                def option(self) -> String:
                    """'option' property of 'results' object"""
                    return self.get_property_state("option")

                @option.setter
                def option(self, value: String):
                    self.set_property_state("option", value)

                @property
                def binary_format(self) -> Boolean:
                    """'binary_format' property of 'results' object"""
                    return self.get_property_state("binary_format")

                @binary_format.setter
                def binary_format(self, value: Boolean):
                    self.set_property_state("binary_format", value)

            property_names_types = [
                ("option", "Option", "String"),
                ("include_instances", "IncludeInstances", "String"),
                ("output_frequency", "OutputFrequency", "Integer"),
            ]

            @property
            def option(self) -> String:
                """'option' property of 'output_control' object"""
                return self.get_property_state("option")

            @option.setter
            def option(self, value: String):
                self.set_property_state("option", value)

            @property
            def include_instances(self) -> String:
                """'include_instances' property of 'output_control' object"""
                return self.get_property_state("include_instances")

            @include_instances.setter
            def include_instances(self, value: String):
                self.set_property_state("include_instances", value)

            @property
            def output_frequency(self) -> Integer:
                """'output_frequency' property of 'output_control' object"""
                return self.get_property_state("output_frequency")

            @output_frequency.setter
            def output_frequency(self, value: Integer):
                self.set_property_state("output_frequency", value)

        class ascii_output(Group):
            """
            'ascii_output' child of 'output_control' object
            """

            syc_name = "AsciiOutput"
            property_names_types = [
                ("option", "Option", "String"),
                ("format", "Format", "String"),
            ]

            @property
            def option(self) -> String:
                """'option' property of 'output_control' object"""
                return self.get_property_state("option")

            @option.setter
            def option(self, value: String):
                self.set_property_state("option", value)

            @property
            def format(self) -> String:
                """'format' property of 'output_control' object"""
                return self.get_property_state("format")

            @format.setter
            def format(self, value: String):
                self.set_property_state("format", value)

        property_names_types = [
            ("option", "Option", "String"),
            ("generate_csv_chart_output", "GenerateCSVChartOutput", "Boolean"),
            ("write_initial_snapshot", "WriteInitialSnapshot", "Boolean"),
            ("transcript_precision", "TranscriptPrecision", "Integer"),
            ("write_diagnostics", "WriteDiagnostics", "Boolean"),
            ("write_weights_matrix", "WriteWeightsMatrix", "Boolean"),
            ("write_residuals", "WriteResiduals", "Boolean"),
            ("output_frequency", "OutputFrequency", "Integer"),
        ]

        @property
        def option(self) -> String:
            """'option' property of 'system_coupling' object"""
            return self.get_property_state("option")

        @option.setter
        def option(self, value: String):
            self.set_property_state("option", value)

        @property
        def generate_csv_chart_output(self) -> Boolean:
            """'generate_csv_chart_output' property of 'system_coupling' object"""
            return self.get_property_state("generate_csv_chart_output")

        @generate_csv_chart_output.setter
        def generate_csv_chart_output(self, value: Boolean):
            self.set_property_state("generate_csv_chart_output", value)

        @property
        def write_initial_snapshot(self) -> Boolean:
            """'write_initial_snapshot' property of 'system_coupling' object"""
            return self.get_property_state("write_initial_snapshot")

        @write_initial_snapshot.setter
        def write_initial_snapshot(self, value: Boolean):
            self.set_property_state("write_initial_snapshot", value)

        @property
        def transcript_precision(self) -> Integer:
            """'transcript_precision' property of 'system_coupling' object"""
            return self.get_property_state("transcript_precision")

        @transcript_precision.setter
        def transcript_precision(self, value: Integer):
            self.set_property_state("transcript_precision", value)

        @property
        def write_diagnostics(self) -> Boolean:
            """'write_diagnostics' property of 'system_coupling' object"""
            return self.get_property_state("write_diagnostics")

        @write_diagnostics.setter
        def write_diagnostics(self, value: Boolean):
            self.set_property_state("write_diagnostics", value)

        @property
        def write_weights_matrix(self) -> Boolean:
            """'write_weights_matrix' property of 'system_coupling' object"""
            return self.get_property_state("write_weights_matrix")

        @write_weights_matrix.setter
        def write_weights_matrix(self, value: Boolean):
            self.set_property_state("write_weights_matrix", value)

        @property
        def write_residuals(self) -> Boolean:
            """'write_residuals' property of 'system_coupling' object"""
            return self.get_property_state("write_residuals")

        @write_residuals.setter
        def write_residuals(self, value: Boolean):
            self.set_property_state("write_residuals", value)

        @property
        def output_frequency(self) -> Integer:
            """'output_frequency' property of 'system_coupling' object"""
            return self.get_property_state("output_frequency")

        @output_frequency.setter
        def output_frequency(self, value: Integer):
            self.set_property_state("output_frequency", value)

    command_names = ["add_participant", "solve", "save", "get_parameter_options"]

    class add_participant(Command):
        """
        'add_participant' child of 'system_coupling' object

        Parameters
        ----------
            additional_arguments : str
                'additional_arguments' child of 'add_participant' object
            executable : str
                'executable' child of 'add_participant' object
            input_file : str
                'input_file' child of 'add_participant' object
            participant_type : str
                'participant_type' child of 'add_participant' object
            working_directory : str
                'working_directory' child of 'add_participant' object

        """

        syc_name = "AddParticipant"
        argument_names = [
            "additional_arguments",
            "executable",
            "input_file",
            "participant_type",
            "working_directory",
        ]

        class additional_arguments(String):
            """
            'additional_arguments' child of 'add_participant' object
            """

            syc_name = "AdditionalArguments"

        class executable(String):
            """
            'executable' child of 'add_participant' object
            """

            syc_name = "Executable"

        class input_file(String):
            """
            'input_file' child of 'add_participant' object
            """

            syc_name = "InputFile"

        class participant_type(String):
            """
            'participant_type' child of 'add_participant' object
            """

            syc_name = "ParticipantType"

        class working_directory(String):
            """
            'working_directory' child of 'add_participant' object
            """

            syc_name = "WorkingDirectory"

    class solve(Command):
        """
        'solve' child of 'system_coupling' object
        """

        syc_name = "Solve"

    class save(Command):
        """
        'save' child of 'system_coupling' object

        Parameters
        ----------
            file_path : str
                'file_path' child of 'save' object

        """

        syc_name = "Save"
        argument_names = ["file_path"]

        class file_path(String):
            """
            'file_path' child of 'save' object
            """

            syc_name = "FilePath"

    class get_parameter_options(PathCommand):
        """
        'get_parameter_options' child of 'system_coupling' object

        Parameters
        ----------
            name : str
                'name' child of 'get_parameter_options' object

        """

        syc_name = "GetParameterOptions"
        argument_names = ["name"]

        class name(String):
            """
            'name' child of 'get_parameter_options' object
            """

            syc_name = "Name"
