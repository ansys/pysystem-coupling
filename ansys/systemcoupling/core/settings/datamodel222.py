"""This is an auto-generated file.  DO NOT EDIT!"""

from ansys.systemcoupling.core.settings.datamodel import *

SHASH = "0fc69b812870d58105ab2869a7feaace0a599a02faa2f1e9215f070900dca536"

class SystemCoupling(Group):
    """
    root object
    """
    syc_name = "SystemCoupling"
    child_names = \
        ['ActivateHidden', 'AnalysisControl', 'CouplingInterface',
         'CouplingParticipant', 'Library', 'OutputControl',
         'SolutionControl']

    class ActivateHidden(Group):
        """
        'ActivateHidden' child of 'SystemCoupling' object
        """
        syc_name = "ActivateHidden"
        child_names = \
            ['AlphaFeatures', 'BetaFeatures', 'LenientValidation']

        class AlphaFeatures(Boolean):
            """
            'AlphaFeatures' child of 'ActivateHidden' object
            """
            syc_name = "AlphaFeatures"

        class BetaFeatures(Boolean):
            """
            'BetaFeatures' child of 'ActivateHidden' object
            """
            syc_name = "BetaFeatures"

        class LenientValidation(Boolean):
            """
            'LenientValidation' child of 'ActivateHidden' object
            """
            syc_name = "LenientValidation"

    class AnalysisControl(Group):
        """
        'AnalysisControl' child of 'SystemCoupling' object
        """
        syc_name = "AnalysisControl"
        child_names = \
            ['Apip', 'GlobalStabilization', 'UnmappedValueOptions',
             'AllowIterationsOnlyMode', 'AllowSimultaneousUpdate',
             'AnalysisType', 'BypassFluentAdapter',
             'FluentRegionUpdateAtStep', 'ImportAllRegions',
             'MeshImportOnInitialization', 'OptimizeIfOneWay',
             'PartitioningAlgorithm', 'RotateFollowerForces',
             'SimultaneousParticipants', 'SolveIncrementalDisplacementFirst',
             'TargetInitializationOption', 'UpdateMappingWeights',
             'VariableToExpressionTransfer', 'WriteScsFile']

        class Apip(Group):
            """
            'Apip' child of 'AnalysisControl' object
            """
            syc_name = "Apip"
            child_names = \
                ['Debug', 'Disable']

            class Debug(Boolean):
                """
                'Debug' child of 'Apip' object
                """
                syc_name = "Debug"

            class Disable(Boolean):
                """
                'Disable' child of 'Apip' object
                """
                syc_name = "Disable"

        class GlobalStabilization(Group):
            """
            'GlobalStabilization' child of 'AnalysisControl' object
            """
            syc_name = "GlobalStabilization"
            child_names = \
                ['DiagnosticsLevel', 'InitialIterations',
                 'InitialRelaxationFactor', 'MaximumRetainedIterations',
                 'MaximumRetainedTimeSteps', 'Option', 'QRTolOldSteps',
                 'QRTolThisStep', 'WeightOption']

            class DiagnosticsLevel(Integer):
                """
                'DiagnosticsLevel' child of 'GlobalStabilization' object
                """
                syc_name = "DiagnosticsLevel"

            class InitialIterations(Integer):
                """
                'InitialIterations' child of 'GlobalStabilization' object
                """
                syc_name = "InitialIterations"

            class InitialRelaxationFactor(Real):
                """
                'InitialRelaxationFactor' child of 'GlobalStabilization' object
                """
                syc_name = "InitialRelaxationFactor"

            class MaximumRetainedIterations(Integer):
                """
                'MaximumRetainedIterations' child of 'GlobalStabilization' object
                """
                syc_name = "MaximumRetainedIterations"

            class MaximumRetainedTimeSteps(Integer):
                """
                'MaximumRetainedTimeSteps' child of 'GlobalStabilization' object
                """
                syc_name = "MaximumRetainedTimeSteps"

            class Option(String):
                """
                'Option' child of 'GlobalStabilization' object
                """
                syc_name = "Option"

            class QRTolOldSteps(Real):
                """
                'QRTolOldSteps' child of 'GlobalStabilization' object
                """
                syc_name = "QRTolOldSteps"

            class QRTolThisStep(Real):
                """
                'QRTolThisStep' child of 'GlobalStabilization' object
                """
                syc_name = "QRTolThisStep"

            class WeightOption(String):
                """
                'WeightOption' child of 'GlobalStabilization' object
                """
                syc_name = "WeightOption"

        class UnmappedValueOptions(Group):
            """
            'UnmappedValueOptions' child of 'AnalysisControl' object
            """
            syc_name = "UnmappedValueOptions"
            child_names = \
                ['FaceFilterTolerance', 'IlutMaxFill', 'IlutPivotTol',
                 'IlutTau', 'MatrixVerbosity', 'Preconditioner',
                 'RbfColinearityTolerance', 'RbfLinearCorrection',
                 'RbfShapeParameter', 'Solver', 'SolverMaxIterations',
                 'SolverMaxSearchDirections', 'SolverRelativeTolerance',
                 'SolverVerbosity']

            class FaceFilterTolerance(Real):
                """
                'FaceFilterTolerance' child of 'UnmappedValueOptions' object
                """
                syc_name = "FaceFilterTolerance"

            class IlutMaxFill(Integer):
                """
                'IlutMaxFill' child of 'UnmappedValueOptions' object
                """
                syc_name = "IlutMaxFill"

            class IlutPivotTol(Real):
                """
                'IlutPivotTol' child of 'UnmappedValueOptions' object
                """
                syc_name = "IlutPivotTol"

            class IlutTau(Real):
                """
                'IlutTau' child of 'UnmappedValueOptions' object
                """
                syc_name = "IlutTau"

            class MatrixVerbosity(Integer):
                """
                'MatrixVerbosity' child of 'UnmappedValueOptions' object
                """
                syc_name = "MatrixVerbosity"

            class Preconditioner(String):
                """
                'Preconditioner' child of 'UnmappedValueOptions' object
                """
                syc_name = "Preconditioner"

            class RbfColinearityTolerance(Real):
                """
                'RbfColinearityTolerance' child of 'UnmappedValueOptions' object
                """
                syc_name = "RbfColinearityTolerance"

            class RbfLinearCorrection(Boolean):
                """
                'RbfLinearCorrection' child of 'UnmappedValueOptions' object
                """
                syc_name = "RbfLinearCorrection"

            class RbfShapeParameter(Real):
                """
                'RbfShapeParameter' child of 'UnmappedValueOptions' object
                """
                syc_name = "RbfShapeParameter"

            class Solver(String):
                """
                'Solver' child of 'UnmappedValueOptions' object
                """
                syc_name = "Solver"

            class SolverMaxIterations(Integer):
                """
                'SolverMaxIterations' child of 'UnmappedValueOptions' object
                """
                syc_name = "SolverMaxIterations"

            class SolverMaxSearchDirections(Integer):
                """
                'SolverMaxSearchDirections' child of 'UnmappedValueOptions' object
                """
                syc_name = "SolverMaxSearchDirections"

            class SolverRelativeTolerance(Real):
                """
                'SolverRelativeTolerance' child of 'UnmappedValueOptions' object
                """
                syc_name = "SolverRelativeTolerance"

            class SolverVerbosity(Integer):
                """
                'SolverVerbosity' child of 'UnmappedValueOptions' object
                """
                syc_name = "SolverVerbosity"

        class AllowIterationsOnlyMode(Boolean):
            """
            'AllowIterationsOnlyMode' child of 'AnalysisControl' object
            """
            syc_name = "AllowIterationsOnlyMode"

        class AllowSimultaneousUpdate(Boolean):
            """
            'AllowSimultaneousUpdate' child of 'AnalysisControl' object
            """
            syc_name = "AllowSimultaneousUpdate"

        class AnalysisType(String):
            """
            'AnalysisType' child of 'AnalysisControl' object
            """
            syc_name = "AnalysisType"

        class BypassFluentAdapter(Boolean):
            """
            'BypassFluentAdapter' child of 'AnalysisControl' object
            """
            syc_name = "BypassFluentAdapter"

        class FluentRegionUpdateAtStep(Boolean):
            """
            'FluentRegionUpdateAtStep' child of 'AnalysisControl' object
            """
            syc_name = "FluentRegionUpdateAtStep"

        class ImportAllRegions(Boolean):
            """
            'ImportAllRegions' child of 'AnalysisControl' object
            """
            syc_name = "ImportAllRegions"

        class MeshImportOnInitialization(Boolean):
            """
            'MeshImportOnInitialization' child of 'AnalysisControl' object
            """
            syc_name = "MeshImportOnInitialization"

        class OptimizeIfOneWay(Boolean):
            """
            'OptimizeIfOneWay' child of 'AnalysisControl' object
            """
            syc_name = "OptimizeIfOneWay"

        class PartitioningAlgorithm(String):
            """
            'PartitioningAlgorithm' child of 'AnalysisControl' object
            """
            syc_name = "PartitioningAlgorithm"

        class RotateFollowerForces(String):
            """
            'RotateFollowerForces' child of 'AnalysisControl' object
            """
            syc_name = "RotateFollowerForces"

        class SimultaneousParticipants(String):
            """
            'SimultaneousParticipants' child of 'AnalysisControl' object
            """
            syc_name = "SimultaneousParticipants"

        class SolveIncrementalDisplacementFirst(Boolean):
            """
            'SolveIncrementalDisplacementFirst' child of 'AnalysisControl' object
            """
            syc_name = "SolveIncrementalDisplacementFirst"

        class TargetInitializationOption(String):
            """
            'TargetInitializationOption' child of 'AnalysisControl' object
            """
            syc_name = "TargetInitializationOption"

        class UpdateMappingWeights(String):
            """
            'UpdateMappingWeights' child of 'AnalysisControl' object
            """
            syc_name = "UpdateMappingWeights"

        class VariableToExpressionTransfer(Boolean):
            """
            'VariableToExpressionTransfer' child of 'AnalysisControl' object
            """
            syc_name = "VariableToExpressionTransfer"

        class WriteScsFile(Boolean):
            """
            'WriteScsFile' child of 'AnalysisControl' object
            """
            syc_name = "WriteScsFile"

    class CouplingInterface(NamedObject):
        """
        'CouplingInterface' child of 'SystemCoupling' object
        """
        syc_name = "CouplingInterface"

        class child_object_type(Group):
            """
            'child_object_type' child of 'CouplingInterface' object
            """
            syc_name = "child_object_type"
            child_names = \
                ['DataTransfer', 'MappingControl', 'Side', 'DisplayName']

            class DataTransfer(NamedObject):
                """
                'DataTransfer' child of 'child_object_type' object
                """
                syc_name = "DataTransfer"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'DataTransfer' object
                    """
                    syc_name = "child_object_type"
                    child_names = \
                        ['Stabilization', 'ConvergenceTarget', 'DisplayName',
                         'MappingType', 'Option', 'RampingOption',
                         'RelaxationFactor', 'SourceVariable', 'Suppress',
                         'TargetSide', 'TargetVariable',
                         'TimeStepInitializationOption',
                         'UnmappedValueOption', 'Value']

                    class Stabilization(Group):
                        """
                        'Stabilization' child of 'child_object_type' object
                        """
                        syc_name = "Stabilization"
                        child_names = \
                            ['CoupleWithGlobalStabilization',
                             'DiagnosticsLevel', 'InitialIterations',
                             'InitialRelaxationFactor',
                             'MaximumRetainedIterations',
                             'MaximumRetainedTimeSteps', 'Option',
                             'QRTolOldSteps', 'QRTolThisStep',
                             'TimeStepInitializationOption', 'WeightFactor',
                             'WeightOption']

                        class CoupleWithGlobalStabilization(Boolean):
                            """
                            'CoupleWithGlobalStabilization' child of 'Stabilization' object
                            """
                            syc_name = "CoupleWithGlobalStabilization"

                        class DiagnosticsLevel(Integer):
                            """
                            'DiagnosticsLevel' child of 'Stabilization' object
                            """
                            syc_name = "DiagnosticsLevel"

                        class InitialIterations(Integer):
                            """
                            'InitialIterations' child of 'Stabilization' object
                            """
                            syc_name = "InitialIterations"

                        class InitialRelaxationFactor(Real):
                            """
                            'InitialRelaxationFactor' child of 'Stabilization' object
                            """
                            syc_name = "InitialRelaxationFactor"

                        class MaximumRetainedIterations(Integer):
                            """
                            'MaximumRetainedIterations' child of 'Stabilization' object
                            """
                            syc_name = "MaximumRetainedIterations"

                        class MaximumRetainedTimeSteps(Integer):
                            """
                            'MaximumRetainedTimeSteps' child of 'Stabilization' object
                            """
                            syc_name = "MaximumRetainedTimeSteps"

                        class Option(String):
                            """
                            'Option' child of 'Stabilization' object
                            """
                            syc_name = "Option"

                        class QRTolOldSteps(Real):
                            """
                            'QRTolOldSteps' child of 'Stabilization' object
                            """
                            syc_name = "QRTolOldSteps"

                        class QRTolThisStep(Real):
                            """
                            'QRTolThisStep' child of 'Stabilization' object
                            """
                            syc_name = "QRTolThisStep"

                        class TimeStepInitializationOption(String):
                            """
                            'TimeStepInitializationOption' child of 'Stabilization' object
                            """
                            syc_name = "TimeStepInitializationOption"

                        class WeightFactor(Real):
                            """
                            'WeightFactor' child of 'Stabilization' object
                            """
                            syc_name = "WeightFactor"

                        class WeightOption(String):
                            """
                            'WeightOption' child of 'Stabilization' object
                            """
                            syc_name = "WeightOption"

                    class ConvergenceTarget(Real):
                        """
                        'ConvergenceTarget' child of 'child_object_type' object
                        """
                        syc_name = "ConvergenceTarget"

                    class DisplayName(String):
                        """
                        'DisplayName' child of 'child_object_type' object
                        """
                        syc_name = "DisplayName"

                    class MappingType(String):
                        """
                        'MappingType' child of 'child_object_type' object
                        """
                        syc_name = "MappingType"

                    class Option(String):
                        """
                        'Option' child of 'child_object_type' object
                        """
                        syc_name = "Option"

                    class RampingOption(String):
                        """
                        'RampingOption' child of 'child_object_type' object
                        """
                        syc_name = "RampingOption"

                    class RelaxationFactor(Real):
                        """
                        'RelaxationFactor' child of 'child_object_type' object
                        """
                        syc_name = "RelaxationFactor"

                    class SourceVariable(String):
                        """
                        'SourceVariable' child of 'child_object_type' object
                        """
                        syc_name = "SourceVariable"

                    class Suppress(Boolean):
                        """
                        'Suppress' child of 'child_object_type' object
                        """
                        syc_name = "Suppress"

                    class TargetSide(String):
                        """
                        'TargetSide' child of 'child_object_type' object
                        """
                        syc_name = "TargetSide"

                    class TargetVariable(String):
                        """
                        'TargetVariable' child of 'child_object_type' object
                        """
                        syc_name = "TargetVariable"

                    class TimeStepInitializationOption(String):
                        """
                        'TimeStepInitializationOption' child of 'child_object_type' object
                        """
                        syc_name = "TimeStepInitializationOption"

                    class UnmappedValueOption(String):
                        """
                        'UnmappedValueOption' child of 'child_object_type' object
                        """
                        syc_name = "UnmappedValueOption"

                    class Value(Real):
                        """
                        'Value' child of 'child_object_type' object
                        """
                        syc_name = "Value"

            class MappingControl(Group):
                """
                'MappingControl' child of 'child_object_type' object
                """
                syc_name = "MappingControl"
                child_names = \
                    ['AbsoluteGapTolerance', 'ConservationFixToleranceVolume',
                     'ConservativeIntensive', 'ConservativeReciprocityFactor',
                     'CornerTolerance', 'FaceAlignment', 'HaloTolerance',
                     'PoorIntersectionThreshold', 'PreserveNormal',
                     'ProfilePreservingReciprocityFactor', 'RBFClippingScale',
                     'RBFLinearCorrection', 'RBFOption', 'RBFShapeParameter',
                     'RelativeGapTolerance', 'SmallWeightTolerance',
                     'StopIfPoorIntersection']

                class AbsoluteGapTolerance(Real):
                    """
                    'AbsoluteGapTolerance' child of 'MappingControl' object
                    """
                    syc_name = "AbsoluteGapTolerance"

                class ConservationFixToleranceVolume(Real):
                    """
                    'ConservationFixToleranceVolume' child of 'MappingControl' object
                    """
                    syc_name = "ConservationFixToleranceVolume"

                class ConservativeIntensive(String):
                    """
                    'ConservativeIntensive' child of 'MappingControl' object
                    """
                    syc_name = "ConservativeIntensive"

                class ConservativeReciprocityFactor(Real):
                    """
                    'ConservativeReciprocityFactor' child of 'MappingControl' object
                    """
                    syc_name = "ConservativeReciprocityFactor"

                class CornerTolerance(Real):
                    """
                    'CornerTolerance' child of 'MappingControl' object
                    """
                    syc_name = "CornerTolerance"

                class FaceAlignment(String):
                    """
                    'FaceAlignment' child of 'MappingControl' object
                    """
                    syc_name = "FaceAlignment"

                class HaloTolerance(Real):
                    """
                    'HaloTolerance' child of 'MappingControl' object
                    """
                    syc_name = "HaloTolerance"

                class PoorIntersectionThreshold(Real):
                    """
                    'PoorIntersectionThreshold' child of 'MappingControl' object
                    """
                    syc_name = "PoorIntersectionThreshold"

                class PreserveNormal(String):
                    """
                    'PreserveNormal' child of 'MappingControl' object
                    """
                    syc_name = "PreserveNormal"

                class ProfilePreservingReciprocityFactor(Real):
                    """
                    'ProfilePreservingReciprocityFactor' child of 'MappingControl' object
                    """
                    syc_name = "ProfilePreservingReciprocityFactor"

                class RBFClippingScale(Real):
                    """
                    'RBFClippingScale' child of 'MappingControl' object
                    """
                    syc_name = "RBFClippingScale"

                class RBFLinearCorrection(Boolean):
                    """
                    'RBFLinearCorrection' child of 'MappingControl' object
                    """
                    syc_name = "RBFLinearCorrection"

                class RBFOption(String):
                    """
                    'RBFOption' child of 'MappingControl' object
                    """
                    syc_name = "RBFOption"

                class RBFShapeParameter(Real):
                    """
                    'RBFShapeParameter' child of 'MappingControl' object
                    """
                    syc_name = "RBFShapeParameter"

                class RelativeGapTolerance(Real):
                    """
                    'RelativeGapTolerance' child of 'MappingControl' object
                    """
                    syc_name = "RelativeGapTolerance"

                class SmallWeightTolerance(Real):
                    """
                    'SmallWeightTolerance' child of 'MappingControl' object
                    """
                    syc_name = "SmallWeightTolerance"

                class StopIfPoorIntersection(Boolean):
                    """
                    'StopIfPoorIntersection' child of 'MappingControl' object
                    """
                    syc_name = "StopIfPoorIntersection"

            class Side(NamedObject):
                """
                'Side' child of 'child_object_type' object
                """
                syc_name = "Side"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'Side' object
                    """
                    syc_name = "child_object_type"
                    child_names = \
                        ['CouplingParticipant', 'Instancing',
                         'ReferenceFrame', 'RegionList']

                    class CouplingParticipant(String):
                        """
                        'CouplingParticipant' child of 'child_object_type' object
                        """
                        syc_name = "CouplingParticipant"

                    class Instancing(String):
                        """
                        'Instancing' child of 'child_object_type' object
                        """
                        syc_name = "Instancing"

                    class ReferenceFrame(String):
                        """
                        'ReferenceFrame' child of 'child_object_type' object
                        """
                        syc_name = "ReferenceFrame"

                    class RegionList(StringList):
                        """
                        'RegionList' child of 'child_object_type' object
                        """
                        syc_name = "RegionList"

            class DisplayName(String):
                """
                'DisplayName' child of 'child_object_type' object
                """
                syc_name = "DisplayName"

    class CouplingParticipant(NamedObject):
        """
        'CouplingParticipant' child of 'SystemCoupling' object
        """
        syc_name = "CouplingParticipant"

        class child_object_type(Group):
            """
            'child_object_type' child of 'CouplingParticipant' object
            """
            syc_name = "child_object_type"
            child_names = \
                ['ExecutionControl', 'ExternalDataFile', 'FMUParameter',
                 'Region', 'UpdateControl', 'Variable', 'DisplayName',
                 'LoggingOn', 'ParticipantAnalysisType',
                 'ParticipantDisplayName', 'ParticipantFileLoaded',
                 'ParticipantType', 'RestartsSupported', 'UseNewAPIs']

            class ExecutionControl(Group):
                """
                'ExecutionControl' child of 'child_object_type' object
                """
                syc_name = "ExecutionControl"
                child_names = \
                    ['FluentInput', 'AdditionalArguments',
                     'AdditionalRestartInputFile', 'Executable', 'GuiMode',
                     'InitialInput', 'Option', 'ParallelFraction',
                     'WorkingDirectory']

                class FluentInput(Group):
                    """
                    'FluentInput' child of 'ExecutionControl' object
                    """
                    syc_name = "FluentInput"
                    child_names = \
                        ['CaseFile', 'DataFile', 'JournalFile', 'Option']

                    class CaseFile(String):
                        """
                        'CaseFile' child of 'FluentInput' object
                        """
                        syc_name = "CaseFile"

                    class DataFile(String):
                        """
                        'DataFile' child of 'FluentInput' object
                        """
                        syc_name = "DataFile"

                    class JournalFile(String):
                        """
                        'JournalFile' child of 'FluentInput' object
                        """
                        syc_name = "JournalFile"

                    class Option(String):
                        """
                        'Option' child of 'FluentInput' object
                        """
                        syc_name = "Option"

                class AdditionalArguments(String):
                    """
                    'AdditionalArguments' child of 'ExecutionControl' object
                    """
                    syc_name = "AdditionalArguments"

                class AdditionalRestartInputFile(String):
                    """
                    'AdditionalRestartInputFile' child of 'ExecutionControl' object
                    """
                    syc_name = "AdditionalRestartInputFile"

                class Executable(String):
                    """
                    'Executable' child of 'ExecutionControl' object
                    """
                    syc_name = "Executable"

                class GuiMode(Boolean):
                    """
                    'GuiMode' child of 'ExecutionControl' object
                    """
                    syc_name = "GuiMode"

                class InitialInput(String):
                    """
                    'InitialInput' child of 'ExecutionControl' object
                    """
                    syc_name = "InitialInput"

                class Option(String):
                    """
                    'Option' child of 'ExecutionControl' object
                    """
                    syc_name = "Option"

                class ParallelFraction(Real):
                    """
                    'ParallelFraction' child of 'ExecutionControl' object
                    """
                    syc_name = "ParallelFraction"

                class WorkingDirectory(String):
                    """
                    'WorkingDirectory' child of 'ExecutionControl' object
                    """
                    syc_name = "WorkingDirectory"

            class ExternalDataFile(Group):
                """
                'ExternalDataFile' child of 'child_object_type' object
                """
                syc_name = "ExternalDataFile"
                child_names = \
                    ['FilePath']

                class FilePath(String):
                    """
                    'FilePath' child of 'ExternalDataFile' object
                    """
                    syc_name = "FilePath"

            class FMUParameter(NamedObject):
                """
                'FMUParameter' child of 'child_object_type' object
                """
                syc_name = "FMUParameter"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'FMUParameter' object
                    """
                    syc_name = "child_object_type"
                    child_names = \
                        ['DataType', 'DisplayName', 'IntegerMax',
                         'IntegerMin', 'IntegerValue', 'LogicalValue',
                         'ParticipantDisplayName', 'RealMax', 'RealMin',
                         'RealValue', 'StringValue']

                    class DataType(String):
                        """
                        'DataType' child of 'child_object_type' object
                        """
                        syc_name = "DataType"

                    class DisplayName(String):
                        """
                        'DisplayName' child of 'child_object_type' object
                        """
                        syc_name = "DisplayName"

                    class IntegerMax(Integer):
                        """
                        'IntegerMax' child of 'child_object_type' object
                        """
                        syc_name = "IntegerMax"

                    class IntegerMin(Integer):
                        """
                        'IntegerMin' child of 'child_object_type' object
                        """
                        syc_name = "IntegerMin"

                    class IntegerValue(Integer):
                        """
                        'IntegerValue' child of 'child_object_type' object
                        """
                        syc_name = "IntegerValue"

                    class LogicalValue(Boolean):
                        """
                        'LogicalValue' child of 'child_object_type' object
                        """
                        syc_name = "LogicalValue"

                    class ParticipantDisplayName(String):
                        """
                        'ParticipantDisplayName' child of 'child_object_type' object
                        """
                        syc_name = "ParticipantDisplayName"

                    class RealMax(Real):
                        """
                        'RealMax' child of 'child_object_type' object
                        """
                        syc_name = "RealMax"

                    class RealMin(Real):
                        """
                        'RealMin' child of 'child_object_type' object
                        """
                        syc_name = "RealMin"

                    class RealValue(Real):
                        """
                        'RealValue' child of 'child_object_type' object
                        """
                        syc_name = "RealValue"

                    class StringValue(String):
                        """
                        'StringValue' child of 'child_object_type' object
                        """
                        syc_name = "StringValue"

            class Region(NamedObject):
                """
                'Region' child of 'child_object_type' object
                """
                syc_name = "Region"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'Region' object
                    """
                    syc_name = "child_object_type"
                    child_names = \
                        ['DisplayName', 'InputVariables', 'OutputVariables',
                         'Topology']

                    class DisplayName(String):
                        """
                        'DisplayName' child of 'child_object_type' object
                        """
                        syc_name = "DisplayName"

                    class InputVariables(StringList):
                        """
                        'InputVariables' child of 'child_object_type' object
                        """
                        syc_name = "InputVariables"

                    class OutputVariables(StringList):
                        """
                        'OutputVariables' child of 'child_object_type' object
                        """
                        syc_name = "OutputVariables"

                    class Topology(String):
                        """
                        'Topology' child of 'child_object_type' object
                        """
                        syc_name = "Topology"

            class UpdateControl(Group):
                """
                'UpdateControl' child of 'child_object_type' object
                """
                syc_name = "UpdateControl"
                child_names = \
                    ['Option', 'UpdateFrequency']

                class Option(String):
                    """
                    'Option' child of 'UpdateControl' object
                    """
                    syc_name = "Option"

                class UpdateFrequency(Integer):
                    """
                    'UpdateFrequency' child of 'UpdateControl' object
                    """
                    syc_name = "UpdateFrequency"

            class Variable(NamedObject):
                """
                'Variable' child of 'child_object_type' object
                """
                syc_name = "Variable"

                class child_object_type(Group):
                    """
                    'child_object_type' child of 'Variable' object
                    """
                    syc_name = "child_object_type"
                    child_names = \
                        ['Attribute', 'DataType', 'DisplayName',
                         'IntegerInitialValue', 'IntegerMax', 'IntegerMin',
                         'IsExtensive', 'Location', 'LogicalInitialValue',
                         'ParticipantDisplayName', 'QuantityType',
                         'RealInitialValue', 'RealMax', 'RealMin',
                         'StringInitialValue', 'TensorType']

                    class Attribute(NamedObject):
                        """
                        'Attribute' child of 'child_object_type' object
                        """
                        syc_name = "Attribute"

                        class child_object_type(Group):
                            """
                            'child_object_type' child of 'Attribute' object
                            """
                            syc_name = "child_object_type"
                            child_names = \
                                ['Dimensionality', 'AttributeType',
                                 'IntegerValue', 'RealValue']

                            class Dimensionality(Group):
                                """
                                'Dimensionality' child of 'child_object_type' object
                                """
                                syc_name = "Dimensionality"
                                child_names = \
                                    ['AmountOfSubstance', 'Angle', 'Current',
                                     'Length', 'LuminousIntensity', 'Mass',
                                     'Temperature', 'Time']

                                class AmountOfSubstance(Real):
                                    """
                                    'AmountOfSubstance' child of 'Dimensionality' object
                                    """
                                    syc_name = "AmountOfSubstance"

                                class Angle(Real):
                                    """
                                    'Angle' child of 'Dimensionality' object
                                    """
                                    syc_name = "Angle"

                                class Current(Real):
                                    """
                                    'Current' child of 'Dimensionality' object
                                    """
                                    syc_name = "Current"

                                class Length(Real):
                                    """
                                    'Length' child of 'Dimensionality' object
                                    """
                                    syc_name = "Length"

                                class LuminousIntensity(Real):
                                    """
                                    'LuminousIntensity' child of 'Dimensionality' object
                                    """
                                    syc_name = "LuminousIntensity"

                                class Mass(Real):
                                    """
                                    'Mass' child of 'Dimensionality' object
                                    """
                                    syc_name = "Mass"

                                class Temperature(Real):
                                    """
                                    'Temperature' child of 'Dimensionality' object
                                    """
                                    syc_name = "Temperature"

                                class Time(Real):
                                    """
                                    'Time' child of 'Dimensionality' object
                                    """
                                    syc_name = "Time"

                            class AttributeType(String):
                                """
                                'AttributeType' child of 'child_object_type' object
                                """
                                syc_name = "AttributeType"

                            class IntegerValue(Integer):
                                """
                                'IntegerValue' child of 'child_object_type' object
                                """
                                syc_name = "IntegerValue"

                            class RealValue(Real):
                                """
                                'RealValue' child of 'child_object_type' object
                                """
                                syc_name = "RealValue"

                    class DataType(String):
                        """
                        'DataType' child of 'child_object_type' object
                        """
                        syc_name = "DataType"

                    class DisplayName(String):
                        """
                        'DisplayName' child of 'child_object_type' object
                        """
                        syc_name = "DisplayName"

                    class IntegerInitialValue(Integer):
                        """
                        'IntegerInitialValue' child of 'child_object_type' object
                        """
                        syc_name = "IntegerInitialValue"

                    class IntegerMax(Integer):
                        """
                        'IntegerMax' child of 'child_object_type' object
                        """
                        syc_name = "IntegerMax"

                    class IntegerMin(Integer):
                        """
                        'IntegerMin' child of 'child_object_type' object
                        """
                        syc_name = "IntegerMin"

                    class IsExtensive(Boolean):
                        """
                        'IsExtensive' child of 'child_object_type' object
                        """
                        syc_name = "IsExtensive"

                    class Location(String):
                        """
                        'Location' child of 'child_object_type' object
                        """
                        syc_name = "Location"

                    class LogicalInitialValue(Boolean):
                        """
                        'LogicalInitialValue' child of 'child_object_type' object
                        """
                        syc_name = "LogicalInitialValue"

                    class ParticipantDisplayName(String):
                        """
                        'ParticipantDisplayName' child of 'child_object_type' object
                        """
                        syc_name = "ParticipantDisplayName"

                    class QuantityType(String):
                        """
                        'QuantityType' child of 'child_object_type' object
                        """
                        syc_name = "QuantityType"

                    class RealInitialValue(Real):
                        """
                        'RealInitialValue' child of 'child_object_type' object
                        """
                        syc_name = "RealInitialValue"

                    class RealMax(Real):
                        """
                        'RealMax' child of 'child_object_type' object
                        """
                        syc_name = "RealMax"

                    class RealMin(Real):
                        """
                        'RealMin' child of 'child_object_type' object
                        """
                        syc_name = "RealMin"

                    class StringInitialValue(String):
                        """
                        'StringInitialValue' child of 'child_object_type' object
                        """
                        syc_name = "StringInitialValue"

                    class TensorType(String):
                        """
                        'TensorType' child of 'child_object_type' object
                        """
                        syc_name = "TensorType"

            class DisplayName(String):
                """
                'DisplayName' child of 'child_object_type' object
                """
                syc_name = "DisplayName"

            class LoggingOn(Boolean):
                """
                'LoggingOn' child of 'child_object_type' object
                """
                syc_name = "LoggingOn"

            class ParticipantAnalysisType(String):
                """
                'ParticipantAnalysisType' child of 'child_object_type' object
                """
                syc_name = "ParticipantAnalysisType"

            class ParticipantDisplayName(String):
                """
                'ParticipantDisplayName' child of 'child_object_type' object
                """
                syc_name = "ParticipantDisplayName"

            class ParticipantFileLoaded(String):
                """
                'ParticipantFileLoaded' child of 'child_object_type' object
                """
                syc_name = "ParticipantFileLoaded"

            class ParticipantType(String):
                """
                'ParticipantType' child of 'child_object_type' object
                """
                syc_name = "ParticipantType"

            class RestartsSupported(Boolean):
                """
                'RestartsSupported' child of 'child_object_type' object
                """
                syc_name = "RestartsSupported"

            class UseNewAPIs(Boolean):
                """
                'UseNewAPIs' child of 'child_object_type' object
                """
                syc_name = "UseNewAPIs"

    class Library(Group):
        """
        'Library' child of 'SystemCoupling' object
        """
        syc_name = "Library"
        child_names = \
            ['Expression', 'ExpressionFunction', 'Instancing',
             'ReferenceFrame']

        class Expression(NamedObject):
            """
            'Expression' child of 'Library' object
            """
            syc_name = "Expression"

            class child_object_type(Group):
                """
                'child_object_type' child of 'Expression' object
                """
                syc_name = "child_object_type"
                child_names = \
                    ['ExpressionName', 'ExpressionString']

                class ExpressionName(String):
                    """
                    'ExpressionName' child of 'child_object_type' object
                    """
                    syc_name = "ExpressionName"

                class ExpressionString(String):
                    """
                    'ExpressionString' child of 'child_object_type' object
                    """
                    syc_name = "ExpressionString"

        class ExpressionFunction(NamedObject):
            """
            'ExpressionFunction' child of 'Library' object
            """
            syc_name = "ExpressionFunction"

            class child_object_type(Group):
                """
                'child_object_type' child of 'ExpressionFunction' object
                """
                syc_name = "child_object_type"
                child_names = \
                    ['Function', 'FunctionName', 'Module']

                class Function(String):
                    """
                    'Function' child of 'child_object_type' object
                    """
                    syc_name = "Function"

                class FunctionName(String):
                    """
                    'FunctionName' child of 'child_object_type' object
                    """
                    syc_name = "FunctionName"

                class Module(String):
                    """
                    'Module' child of 'child_object_type' object
                    """
                    syc_name = "Module"

        class Instancing(NamedObject):
            """
            'Instancing' child of 'Library' object
            """
            syc_name = "Instancing"

            class child_object_type(Group):
                """
                'child_object_type' child of 'Instancing' object
                """
                syc_name = "child_object_type"
                child_names = \
                    ['InstancesForMapping', 'InstancesInFullCircle',
                     'ReferenceFrame']

                class InstancesForMapping(Integer):
                    """
                    'InstancesForMapping' child of 'child_object_type' object
                    """
                    syc_name = "InstancesForMapping"

                class InstancesInFullCircle(Integer):
                    """
                    'InstancesInFullCircle' child of 'child_object_type' object
                    """
                    syc_name = "InstancesInFullCircle"

                class ReferenceFrame(String):
                    """
                    'ReferenceFrame' child of 'child_object_type' object
                    """
                    syc_name = "ReferenceFrame"

        class ReferenceFrame(NamedObject):
            """
            'ReferenceFrame' child of 'Library' object
            """
            syc_name = "ReferenceFrame"

            class child_object_type(Group):
                """
                'child_object_type' child of 'ReferenceFrame' object
                """
                syc_name = "child_object_type"
                child_names = \
                    ['Transformation', 'Option', 'ParentReferenceFrame',
                     'TransformationMatrix', 'TransformationOrder']

                class Transformation(NamedObject):
                    """
                    'Transformation' child of 'child_object_type' object
                    """
                    syc_name = "Transformation"

                    class child_object_type(Group):
                        """
                        'child_object_type' child of 'Transformation' object
                        """
                        syc_name = "child_object_type"
                        child_names = \
                            ['Angle', 'Axis', 'Option', 'Vector']

                        class Angle(Real):
                            """
                            'Angle' child of 'child_object_type' object
                            """
                            syc_name = "Angle"

                        class Axis(String):
                            """
                            'Axis' child of 'child_object_type' object
                            """
                            syc_name = "Axis"

                        class Option(String):
                            """
                            'Option' child of 'child_object_type' object
                            """
                            syc_name = "Option"

                        class Vector(RealList):
                            """
                            'Vector' child of 'child_object_type' object
                            """
                            syc_name = "Vector"

                class Option(String):
                    """
                    'Option' child of 'child_object_type' object
                    """
                    syc_name = "Option"

                class ParentReferenceFrame(String):
                    """
                    'ParentReferenceFrame' child of 'child_object_type' object
                    """
                    syc_name = "ParentReferenceFrame"

                class TransformationMatrix(RealList):
                    """
                    'TransformationMatrix' child of 'child_object_type' object
                    """
                    syc_name = "TransformationMatrix"

                class TransformationOrder(StringList):
                    """
                    'TransformationOrder' child of 'child_object_type' object
                    """
                    syc_name = "TransformationOrder"

    class OutputControl(Group):
        """
        'OutputControl' child of 'SystemCoupling' object
        """
        syc_name = "OutputControl"
        child_names = \
            ['AsciiOutput', 'Results', 'GenerateCSVChartOutput', 'Option',
             'OutputFrequency', 'TranscriptPrecision', 'WriteDiagnostics',
             'WriteInitialSnapshot', 'WriteResiduals', 'WriteWeightsMatrix']

        class AsciiOutput(Group):
            """
            'AsciiOutput' child of 'OutputControl' object
            """
            syc_name = "AsciiOutput"
            child_names = \
                ['Format', 'Option']

            class Format(String):
                """
                'Format' child of 'AsciiOutput' object
                """
                syc_name = "Format"

            class Option(String):
                """
                'Option' child of 'AsciiOutput' object
                """
                syc_name = "Option"

        class Results(Group):
            """
            'Results' child of 'OutputControl' object
            """
            syc_name = "Results"
            child_names = \
                ['Type', 'IncludeInstances', 'Option', 'OutputFrequency']

            class Type(Group):
                """
                'Type' child of 'Results' object
                """
                syc_name = "Type"
                child_names = \
                    ['BinaryFormat', 'Option']

                class BinaryFormat(Boolean):
                    """
                    'BinaryFormat' child of 'Type' object
                    """
                    syc_name = "BinaryFormat"

                class Option(String):
                    """
                    'Option' child of 'Type' object
                    """
                    syc_name = "Option"

            class IncludeInstances(String):
                """
                'IncludeInstances' child of 'Results' object
                """
                syc_name = "IncludeInstances"

            class Option(String):
                """
                'Option' child of 'Results' object
                """
                syc_name = "Option"

            class OutputFrequency(Integer):
                """
                'OutputFrequency' child of 'Results' object
                """
                syc_name = "OutputFrequency"

        class GenerateCSVChartOutput(Boolean):
            """
            'GenerateCSVChartOutput' child of 'OutputControl' object
            """
            syc_name = "GenerateCSVChartOutput"

        class Option(String):
            """
            'Option' child of 'OutputControl' object
            """
            syc_name = "Option"

        class OutputFrequency(Integer):
            """
            'OutputFrequency' child of 'OutputControl' object
            """
            syc_name = "OutputFrequency"

        class TranscriptPrecision(Integer):
            """
            'TranscriptPrecision' child of 'OutputControl' object
            """
            syc_name = "TranscriptPrecision"

        class WriteDiagnostics(Boolean):
            """
            'WriteDiagnostics' child of 'OutputControl' object
            """
            syc_name = "WriteDiagnostics"

        class WriteInitialSnapshot(Boolean):
            """
            'WriteInitialSnapshot' child of 'OutputControl' object
            """
            syc_name = "WriteInitialSnapshot"

        class WriteResiduals(Boolean):
            """
            'WriteResiduals' child of 'OutputControl' object
            """
            syc_name = "WriteResiduals"

        class WriteWeightsMatrix(Boolean):
            """
            'WriteWeightsMatrix' child of 'OutputControl' object
            """
            syc_name = "WriteWeightsMatrix"

    class SolutionControl(Group):
        """
        'SolutionControl' child of 'SystemCoupling' object
        """
        syc_name = "SolutionControl"
        child_names = \
            ['AvailablePorts', 'DurationOption', 'EndTime',
             'MaximumIterations', 'MinimumIterations', 'NumberOfSteps',
             'TimeStepSize']

        class AvailablePorts(Group):
            """
            'AvailablePorts' child of 'SolutionControl' object
            """
            syc_name = "AvailablePorts"
            child_names = \
                ['Option', 'Range']

            class Option(String):
                """
                'Option' child of 'AvailablePorts' object
                """
                syc_name = "Option"

            class Range(String):
                """
                'Range' child of 'AvailablePorts' object
                """
                syc_name = "Range"

        class DurationOption(String):
            """
            'DurationOption' child of 'SolutionControl' object
            """
            syc_name = "DurationOption"

        class EndTime(Real):
            """
            'EndTime' child of 'SolutionControl' object
            """
            syc_name = "EndTime"

        class MaximumIterations(Integer):
            """
            'MaximumIterations' child of 'SolutionControl' object
            """
            syc_name = "MaximumIterations"

        class MinimumIterations(Integer):
            """
            'MinimumIterations' child of 'SolutionControl' object
            """
            syc_name = "MinimumIterations"

        class NumberOfSteps(Integer):
            """
            'NumberOfSteps' child of 'SolutionControl' object
            """
            syc_name = "NumberOfSteps"

        class TimeStepSize(Real):
            """
            'TimeStepSize' child of 'SolutionControl' object
            """
            syc_name = "TimeStepSize"
