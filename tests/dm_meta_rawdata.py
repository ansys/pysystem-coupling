"""Data model metadata raw data for testing purposes.
"""

dm_meta_testing_raw_data = {
    'SystemCoupling':
    {'__children':
     {'ActivateHidden':
      {'__children':  {},
       '__parameters':
       {'AlphaFeatures':
        {'ordinal': 1,
         'type': 'Logical'},
        'BetaFeatures':
        {'ordinal': 0,
         'type': 'Logical'},
        'LenientValidation':
        {'ordinal': 2,
         'type': 'Logical'}},
       'creatableNamedChildren': [],
       'isEntity': False,
       'isNamed': False,
       'ordinal': 0},
      'AnalysisControl':
      {'__children':
       {'Apip':
        {'__children':
         {},
         '__parameters':
         {'Debug':
          {'ordinal': 0,
           'type': 'Logical'},
          'Disable':
          {'ordinal': 1,
           'type': 'Logical'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 1},
        'GlobalStabilization':
        {'__children':
         {},
         '__parameters':
         {'DiagnosticsLevel':
          {'ordinal': 5,
           'type': 'Integer'},
          'InitialIterations':
          {'ordinal': 1,
           'type': 'Integer'},
          'InitialRelaxationFactor':
          {'ordinal': 2,
           'quant': 'Dimensionless',
           'type': 'Real'},
          'MaximumRetainedIterations':
          {'ordinal': 4,
           'type': 'Integer'},
          'MaximumRetainedTimeSteps':
          {'ordinal': 3,
           'type': 'Integer'},
          'Option':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('None',
                             'Quasi-Newton'),
           'type': 'String'},
          'QRTolOldSteps':
          {'ordinal': 8,
           'quant': 'Dimensionless',
           'type': 'Real'},
          'QRTolThisStep':
          {'ordinal': 7,
           'quant': 'Dimensionless',
           'type': 'Real'},
          'WeightOption':
          {'isRestricted': True,
           'ordinal': 6,
           'staticOptions': ('Constant',
                             'InverseResidual',
                             'InverseResidualSum',
                             'Residual',
                             'ResidualSum',
                             'Value'),
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 0},
        'UnmappedValueOptions':
        {'__children':
         {},
         '__parameters':
         {'FaceFilterTolerance':
          {'ordinal': 10,
           'quant': '',
           'type': 'Real'},
          'IlutMaxFill':
          {'ordinal': 8,
           'type': 'Integer'},
          'IlutPivotTol':
          {'ordinal': 9,
           'quant': '',
           'type': 'Real'},
          'IlutTau':
          {'ordinal': 7,
           'quant': '',
           'type': 'Real'},
          'MatrixVerbosity':
          {'ordinal': 0,
           'type': 'Integer'},
          'Preconditioner':
          {'isRestricted': True,
           'ordinal': 6,
           'staticOptions': ('ILUT',
                             'None'),
           'type': 'String'},
          'RbfColinearityTolerance':
          {'ordinal': 13,
           'quant': '',
           'type': 'Real'},
          'RbfLinearCorrection':
          {'ordinal': 12,
           'type': 'Logical'},
          'RbfShapeParameter':
          {'ordinal': 11,
           'quant': '',
           'type': 'Real'},
          'Solver':
          {'isRestricted': True,
           'ordinal': 2,
           'staticOptions': ('FGMRES',
                             'GMRES'),
           'type': 'String'},
          'SolverMaxIterations':
          {'ordinal': 4,
           'type': 'Integer'},
          'SolverMaxSearchDirections':
          {'ordinal': 5,
           'type': 'Integer'},
          'SolverRelativeTolerance':
          {'ordinal': 3,
           'quant': '',
           'type': 'Real'},
          'SolverVerbosity':
          {'ordinal': 1,
           'type': 'Integer'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 2}},
       '__parameters':
       {'AllowIterationsOnlyMode':
        {'ordinal': 5,
         'type': 'Logical'},
        'AllowSimultaneousUpdate':
        {'ordinal': 2,
         'type': 'Logical'},
        'AnalysisType':
        {'isRestricted': True,
         'ordinal': 0,
         'staticOptions': ('Steady',
                           'Transient'),
         'type': 'String'},
        'BypassFluentAdapter':
        {'ordinal': 10,
         'type': 'Logical'},
        'FluentRegionUpdateAtStep':
        {'ordinal': 7,
         'type': 'Logical'},
        'ImportAllRegions':
        {'ordinal': 9,
         'type': 'Logical'},
        'MeshImportOnInitialization':
        {'ordinal': 8,
         'type': 'Logical'},
        'OptimizeIfOneWay':
        {'ordinal': 1,
         'type': 'Logical'},
        'PartitioningAlgorithm':
        {'isRestricted': True,
         'ordinal': 4,
         'staticOptions': ('DistributedAllocateCores',
                           'DistributedAllocateMachines',
                           'SharedAllocateCores',
                           'SharedAllocateMachines'),
         'type': 'String'},
        'RotateFollowerForces':
        {'isRestricted': True,
         'ordinal': 13,
         'staticOptions': ('MeshImport',
                           'StartOfStep'),
         'type': 'String'},
        'SimultaneousParticipants':
        {'isRestricted': True,
         'ordinal': 3,
         'staticOptions': ('All',
                           'Independent'),
         'type': 'String'},
        'SolveIncrementalDisplacementFirst':
        {'ordinal': 14,
         'type': 'Logical'},
        'TargetInitializationOption':
        {'isRestricted': True,
         'ordinal': 6,
         'staticOptions': ('UseConstantValue',
                           'UseInterpolation'),
         'type': 'String'},
        'UpdateMappingWeights':
        {'isRestricted': True,
         'ordinal': 12,
         'staticOptions': ('EveryIteration',
                           'EveryStep',
                           'Off'),
         'type': 'String'},
        'VariableToExpressionTransfer':
        {'ordinal': 11,
         'type': 'Logical'},
        'WriteScsFile':
        {'ordinal': 15,
         'type': 'Logical'}},
       'creatableNamedChildren': [],
       'isEntity': True,
       'isNamed': False,
       'ordinal': 3},
      'CouplingInterface':
      {'__children':
       {'DataTransfer':
        {'__children':
         {'Stabilization':
          {'__children':
           {},
           '__parameters':
           {'CoupleWithGlobalStabilization':
            {'ordinal': 1,
             'type': 'Logical'},
            'DiagnosticsLevel':
            {'ordinal': 7,
             'type': 'Integer'},
            'InitialIterations':
            {'ordinal': 2,
             'type': 'Integer'},
            'InitialRelaxationFactor':
            {'ordinal': 3,
             'quant': 'Dimensionless',
             'type': 'Real'},
            'MaximumRetainedIterations':
            {'ordinal': 5,
             'type': 'Integer'},
            'MaximumRetainedTimeSteps':
            {'ordinal': 4,
             'type': 'Integer'},
            'Option':
            {'isRestricted': True,
             'ordinal': 0,
             'staticOptions': ('Aitken',
                               'None',
                               'ProgramControlled',
                               'Quasi-Newton'),
             'type': 'String'},
            'QRTolOldSteps':
            {'ordinal': 10,
             'quant': 'Dimensionless',
             'type': 'Real'},
            'QRTolThisStep':
            {'ordinal': 9,
             'quant': 'Dimensionless',
             'type': 'Real'},
            'TimeStepInitializationOption':
            {'isRestricted': True,
             'ordinal': 11,
             'staticOptions': ('Continue',
                               'Restart'),
             'type': 'String'},
            'WeightFactor':
            {'ordinal': 6,
             'quant': 'Dimensionless',
             'type': 'Real'},
            'WeightOption':
            {'isRestricted': True,
             'ordinal': 8,
             'staticOptions': ('Constant',
                               'InverseResidual',
                               'InverseResidualSum',
                               'Residual',
                               'ResidualSum',
                               'Value'),
             'type': 'String'}},
           'creatableNamedChildren': [],
           'isEntity': False,
           'isNamed': False,
           'ordinal': 0}},
         '__parameters':
         {'ConvergenceTarget':
          {'ordinal': 9,
           'quant': 'Dimensionless',
           'type': 'Real'},
          'DisplayName':
          {'isRestricted': False,
           'ordinal': 0,
           'type': 'String'},
          'MappingType':
          {'isRestricted': True,
           'ordinal': 10,
           'staticOptions': ('Conservative',
                             'ProfilePreserving'),
           'type': 'String'},
          'Option':
          {'isRestricted': True,
           'ordinal': 3,
           'staticOptions': ('UsingExpression',
                             'UsingVariable'),
           'type': 'String'},
          'RampingOption':
          {'isRestricted': True,
           'ordinal': 7,
           'staticOptions': ('Linear',
                             'None'),
           'type': 'String'},
          'RelaxationFactor':
          {'ordinal': 8,
           'quant': 'Dimensionless',
           'type': 'Real'},
          'SourceVariable':
          {'isRestricted': True,
           'ordinal': 4,
           'type': 'String'},
          'Suppress':
          {'ordinal': 1,
           'type': 'Logical'},
          'TargetSide':
          {'isRestricted': True,
           'ordinal': 2,
           'staticOptions': ('One',
                             'Two'),
           'type': 'String'},
          'TargetVariable':
          {'isRestricted': True,
           'ordinal': 5,
           'type': 'String'},
          'TimeStepInitializationOption':
          {'isRestricted': True,
           'ordinal': 12,
           'staticOptions': ('LinearExtrapolation',
                             'PreviousStep',
                             'QuadraticExtrapolation'),
           'type': 'String'},
          'UnmappedValueOption':
          {'isRestricted': True,
           'ordinal': 11,
           'staticOptions': ('Average',
                             'Extrapolation',
                             'Nearest '
                             'Value'),
           'type': 'String'},
          'Value':
          {'ordinal': 6,
           'quant': '',
           'type': 'Real'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 1},
        'MappingControl':
        {'__children':
         {},
         '__parameters':
         {'AbsoluteGapTolerance':
          {'ordinal': 3,
           'quant': 'Length',
           'type': 'Real'},
          'ConservationFixToleranceVolume':
          {'ordinal': 12,
           'quant': '',
           'type': 'Real'},
          'ConservativeIntensive':
          {'isRestricted': True,
           'ordinal': 10,
           'staticOptions': ('Off',
                             'On',
                             'ProgramControlled'),
           'type': 'String'},
          'ConservativeReciprocityFactor':
          {'ordinal': 8,
           'quant': '',
           'type': 'Real'},
          'CornerTolerance':
          {'ordinal': 6,
           'quant': '',
           'type': 'Real'},
          'FaceAlignment':
          {'isRestricted': True,
           'ordinal': 2,
           'staticOptions': ('AnyOrientation',
                             'OppositeOrientation',
                             'ProgramControlled',
                             'SameOrientation'),
           'type': 'String'},
          'HaloTolerance':
          {'ordinal': 7,
           'quant': '',
           'type': 'Real'},
          'PoorIntersectionThreshold':
          {'ordinal': 1,
           'quant': '',
           'type': 'Real'},
          'PreserveNormal':
          {'isRestricted': True,
           'ordinal': 11,
           'staticOptions': ('Off',
                             'On',
                             'ProgramControlled'),
           'type': 'String'},
          'ProfilePreservingReciprocityFactor':
          {'ordinal': 9,
           'quant': '',
           'type': 'Real'},
          'RBFClippingScale':
          {'ordinal': 16,
           'quant': '',
           'type': 'Real'},
          'RBFLinearCorrection':
          {'ordinal': 15,
           'type': 'Logical'},
          'RBFOption':
          {'isRestricted': True,
           'ordinal': 13,
           'staticOptions': ('Gaussian',
                             'ThinPlateSpline'),
           'type': 'String'},
          'RBFShapeParameter':
          {'ordinal': 14,
           'quant': '',
           'type': 'Real'},
          'RelativeGapTolerance':
          {'ordinal': 4,
           'quant': '',
           'type': 'Real'},
          'SmallWeightTolerance':
          {'ordinal': 5,
           'quant': '',
           'type': 'Real'},
          'StopIfPoorIntersection':
          {'ordinal': 0,
           'type': 'Logical'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 2},
        'Side':
        {'__children':
         {},
         '__parameters':
         {'CouplingParticipant':
          {'isRestricted': True,
           'ordinal': 0,
           'type': 'String'},
          'Instancing':
          {'isRestricted': True,
           'ordinal': 3,
           'type': 'String'},
          'ReferenceFrame':
          {'isRestricted': True,
           'ordinal': 2,
           'type': 'String'},
          'RegionList':
          {'isRestricted': True,
           'ordinal': 1,
           'type': 'String '
           'List'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 0}},
       '__parameters':
       {'DisplayName':
        {'isRestricted': False,
         'ordinal': 0,
         'type': 'String'}},
       'creatableNamedChildren': ['DataTransfer'],
       'isEntity': True,
       'isNamed': True,
       'ordinal': 4},
      'CouplingParticipant':
      {'__children':
       {'ExecutionControl':
        {'__children':
         {'FluentInput':
          {'__children':
           {},
           '__parameters':
           {'CaseFile':
            {'isRestricted': False,
             'ordinal': 1,
             'type': 'String'},
            'DataFile':
            {'isRestricted': False,
             'ordinal': 2,
             'type': 'String'},
            'JournalFile':
            {'isRestricted': False,
             'ordinal': 3,
             'type': 'String'},
            'Option':
            {'isRestricted': True,
             'ordinal': 0,
             'staticOptions': ('InitialCaseAndDataFile',
                               'InitialCaseFile',
                               'JournalFile'),
             'type': 'String'}},
           'creatableNamedChildren': [],
           'isEntity': False,
           'isNamed': False,
           'ordinal': 0}},
         '__parameters':
         {'AdditionalArguments':
          {'isRestricted': False,
           'ordinal': 3,
           'type': 'String'},
          'AdditionalRestartInputFile':
          {'isRestricted': False,
           'ordinal': 6,
           'type': 'String'},
          'Executable':
          {'isRestricted': False,
           'ordinal': 2,
           'type': 'String'},
          'GuiMode':
          {'ordinal': 7,
           'type': 'Logical'},
          'InitialInput':
          {'isRestricted': False,
           'ordinal': 5,
           'type': 'String'},
          'Option':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('ExternallyManaged',
                             'ProgramControlled',
                             'UserDefined'),
           'type': 'String'},
          'ParallelFraction':
          {'ordinal': 4,
           'quant': '',
           'type': 'Real'},
          'WorkingDirectory':
          {'isRestricted': False,
           'ordinal': 1,
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 4},
        'ExternalDataFile':
        {'__children':
         {},
         '__parameters':
         {'FilePath':
          {'isRestricted': False,
           'ordinal': 0,
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 5},
        'FMUParameter':
        {'__children':
         {},
         '__parameters':
         {'DataType':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('Integer',
                             'Logical',
                             'None',
                             'Real',
                             'String'),
           'type': 'String'},
          'DisplayName':
          {'isRestricted': False,
           'ordinal': 2,
           'type': 'String'},
          'IntegerMax':
          {'ordinal': 8,
           'type': 'Integer'},
          'IntegerMin':
          {'ordinal': 7,
           'type': 'Integer'},
          'IntegerValue':
          {'ordinal': 6,
           'type': 'Integer'},
          'LogicalValue':
          {'ordinal': 9,
           'type': 'Logical'},
          'ParticipantDisplayName':
          {'isRestricted': False,
           'ordinal': 1,
           'type': 'String'},
          'RealMax':
          {'ordinal': 5,
           'quant': '',
           'type': 'Real'},
          'RealMin':
          {'ordinal': 4,
           'quant': '',
           'type': 'Real'},
          'RealValue':
          {'ordinal': 3,
           'quant': '',
           'type': 'Real'},
          'StringValue':
          {'isRestricted': False,
           'ordinal': 10,
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 3},
        'Region':
        {'__children':
         {},
         '__parameters':
         {'DisplayName':
          {'isRestricted': False,
           'ordinal': 3,
           'type': 'String'},
          'InputVariables':
          {'isRestricted': False,
           'ordinal': 1,
           'type': 'String '
           'List'},
          'OutputVariables':
          {'isRestricted': False,
           'ordinal': 2,
           'type': 'String '
           'List'},
          'Topology':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('PlanarSurface',
                             'Surface',
                             'Undefined',
                             'Volume'),
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 1},
        'UpdateControl':
        {'__children':
         {},
         '__parameters':
         {'Option':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('EveryIteration',
                             'FirstCouplingIteration',
                             'ProgramControlled',
                             'StepInterval',
                             'Suspended'),
           'type': 'String'},
          'UpdateFrequency':
          {'ordinal': 1,
           'type': 'Integer'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 2},
        'Variable':
        {'__children':
         {'Attribute':
          {'__children':
           {'Dimensionality':
            {'__children':
             {},
             '__parameters':
             {'AmountOfSubstance':
              {'ordinal': 4,
               'quant': '',
               'type': 'Real'},
              'Angle':
              {'ordinal': 7,
               'quant': '',
               'type': 'Real'},
              'Current':
              {'ordinal': 5,
               'quant': '',
               'type': 'Real'},
              'Length':
              {'ordinal': 0,
               'quant': '',
               'type': 'Real'},
              'LuminousIntensity':
              {'ordinal': 6,
               'quant': '',
               'type': 'Real'},
              'Mass':
              {'ordinal': 2,
               'quant': '',
               'type': 'Real'},
              'Temperature':
              {'ordinal': 3,
               'quant': '',
               'type': 'Real'},
              'Time':
              {'ordinal': 1,
               'quant': '',
               'type': 'Real'}},
             'creatableNamedChildren': [],
             'isEntity': False,
             'isNamed': False,
             'ordinal': 0}},
           '__parameters':
           {'AttributeType':
            {'isRestricted': True,
             'ordinal': 0,
             'staticOptions': ('Integer',
                               'Real'),
             'type': 'String'},
            'IntegerValue':
            {'ordinal': 2,
             'type': 'Integer'},
            'RealValue':
            {'ordinal': 1,
             'quant': '',
             'type': 'Real'}},
           'creatableNamedChildren': [],
           'isEntity': False,
           'isNamed': True,
           'ordinal': 0}},
         '__parameters':
         {'DataType':
          {'isRestricted': True,
           'ordinal': 4,
           'staticOptions': ('Complex',
                             'Integer',
                             'Logical',
                             'None',
                             'Real',
                             'String'),
           'type': 'String'},
          'DisplayName':
          {'isRestricted': False,
           'ordinal': 3,
           'type': 'String'},
          'IntegerInitialValue':
          {'ordinal': 6,
           'type': 'Integer'},
          'IntegerMax':
          {'ordinal': 12,
           'type': 'Integer'},
          'IntegerMin':
          {'ordinal': 11,
           'type': 'Integer'},
          'IsExtensive':
          {'ordinal': 14,
           'type': 'Logical'},
          'Location':
          {'isRestricted': True,
           'ordinal': 1,
           'staticOptions': ('Element',
                             'Node'),
           'type': 'String'},
          'LogicalInitialValue':
          {'ordinal': 7,
           'type': 'Logical'},
          'ParticipantDisplayName':
          {'isRestricted': False,
           'ordinal': 2,
           'type': 'String'},
          'QuantityType':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('Convection '
                             'Reference '
                             'Temperature',
                             'Force',
                             'Heat '
                             'Rate',
                             'Heat '
                             'Transfer '
                             'Coefficient',
                             'Incremental '
                             'Displacement',
                             'Mode '
                             'Shape',
                             'Temperature',
                             'Unspecified'),
           'type': 'String'},
          'RealInitialValue':
          {'ordinal': 5,
           'quant': '',
           'type': 'Real'},
          'RealMax':
          {'ordinal': 10,
           'quant': '',
           'type': 'Real'},
          'RealMin':
          {'ordinal': 9,
           'quant': '',
           'type': 'Real'},
          'StringInitialValue':
          {'isRestricted': False,
           'ordinal': 8,
           'type': 'String'},
          'TensorType':
          {'isRestricted': True,
           'ordinal': 13,
           'staticOptions': ('Scalar',
                             'Vector'),
           'type': 'String'}},
         'creatableNamedChildren': ['Attribute'],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 0}},
       '__parameters':
       {'DisplayName':
        {'isRestricted': False,
         'ordinal': 2,
         'type': 'String'},
        'LoggingOn':
        {'ordinal': 4,
         'type': 'Logical'},
        'ParticipantAnalysisType':
        {'isRestricted': True,
         'ordinal': 5,
         'staticOptions': ('Steady',
                           'Transient'),
         'type': 'String'},
        'ParticipantDisplayName':
        {'isRestricted': False,
         'ordinal': 1,
         'type': 'String'},
        'ParticipantFileLoaded':
        {'isRestricted': False,
         'ordinal': 3,
         'type': 'String'},
        'ParticipantType':
        {'isRestricted': True,
         'ordinal': 0,
         'staticOptions': ('AEDT',
                           'CFD-SRV',
                           'CFX',
                           'DEFAULT',
                           'DEFAULT-SRV',
                           'EXTERNALDATA',
                           'FLUENT',
                           'FMU',
                           'FORTE',
                           'MAPDL',
                           'MECH-SRV'),
         'type': 'String'},
        'RestartsSupported':
        {'ordinal': 7,
         'type': 'Logical'},
        'UseNewAPIs':
        {'ordinal': 6,
         'type': 'Logical'}},
       'creatableNamedChildren': ['Variable',
                                  'Region',
                                  'FMUParameter'],
       'isEntity': False,
       'isNamed': True,
       'ordinal': 2},
      'Library':
      {'__children':
       {'Expression':
        {'__children':
         {},
         '__parameters':
         {'ExpressionName':
          {'isRestricted': False,
           'ordinal': 0,
           'type': 'String'},
          'ExpressionString':
          {'isRestricted': False,
           'ordinal': 1,
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 0},
        'ExpressionFunction':
        {'__children':
         {},
         '__parameters':
         {'Function':
          {'isRestricted': True,
           'ordinal': 1,
           'type': 'String'},
          'FunctionName':
          {'isRestricted': False,
           'ordinal': 2,
           'type': 'String'},
          'Module':
          {'isRestricted': True,
           'ordinal': 0,
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 1},
        'Instancing':
        {'__children':
         {},
         '__parameters':
         {'InstancesForMapping':
          {'ordinal': 2,
           'type': 'Integer'},
          'InstancesInFullCircle':
          {'ordinal': 1,
           'type': 'Integer'},
          'ReferenceFrame':
          {'isRestricted': True,
           'ordinal': 0,
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 3},
        'ReferenceFrame':
        {'__children':
         {'Transformation':
          {'__children':
           {},
           '__parameters':
           {'Angle':
            {'ordinal': 1,
             'quant': 'Angle',
             'type': 'Real'},
            'Axis':
            {'isRestricted': True,
             'ordinal': 2,
             'staticOptions': ('UserDefined',
                               'XAxis',
                               'YAxis',
                               'ZAxis'),
             'type': 'String'},
            'Option':
            {'isRestricted': True,
             'ordinal': 0,
             'staticOptions': ('Rotation',
                               'Translation'),
             'type': 'String'},
            'Vector':
            {'ordinal': 3,
             'quant': '',
             'type': 'Real '
             'Triplet'}},
           'creatableNamedChildren': [],
           'isEntity': False,
           'isNamed': True,
           'ordinal': 0}},
         '__parameters':
         {'Option':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('ByMatrix',
                             'ByTransformation'),
           'type': 'String'},
          'ParentReferenceFrame':
          {'isRestricted': True,
           'ordinal': 1,
           'type': 'String'},
          'TransformationMatrix':
          {'ordinal': 3,
           'quant': '',
           'type': 'Real '
           'List'},
          'TransformationOrder':
          {'isRestricted': False,
           'ordinal': 2,
           'type': 'String '
           'List'}},
         'creatableNamedChildren': ['Transformation'],
         'isEntity': False,
         'isNamed': True,
         'ordinal': 2}},
       '__parameters':
       {},
       'creatableNamedChildren': ['Expression',
                                  'ExpressionFunction',
                                  'ReferenceFrame',
                                  'Instancing'],
       'isEntity': True,
       'isNamed': False,
       'ordinal': 1},
      'OutputControl':
      {'__children':
       {'AsciiOutput':
        {'__children':
         {},
         '__parameters':
         {'Format':
          {'isRestricted': True,
           'ordinal': 1,
           'staticOptions': ('Axdt',
                             'Csv'),
           'type': 'String'},
          'Option':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('EveryIteration',
                             'EveryStep',
                             'Off'),
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 1},
        'Results':
        {'__children':
         {'Type':
          {'__children':
           {},
           '__parameters':
           {'BinaryFormat':
            {'ordinal': 1,
             'type': 'Logical'},
            'Option':
            {'isRestricted': True,
             'ordinal': 0,
             'staticOptions': ('EnsightGold',),
             'type': 'String'}},
           'creatableNamedChildren': [],
           'isEntity': False,
           'isNamed': False,
           'ordinal': 0}},
         '__parameters':
         {'IncludeInstances':
          {'isRestricted': True,
           'ordinal': 1,
           'staticOptions': ('All',
                             'ProgramControlled',
                             'ReferenceOnly'),
           'type': 'String'},
          'Option':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('EveryIteration',
                             'EveryStep',
                             'IterationInterval',
                             'LastIteration',
                             'LastStep',
                             'Off',
                             'ProgramControlled',
                             'StepInterval'),
           'type': 'String'},
          'OutputFrequency':
          {'ordinal': 2,
           'type': 'Integer'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 0}},
       '__parameters':
       {'GenerateCSVChartOutput':
        {'ordinal': 1,
         'type': 'Logical'},
        'Option':
        {'isRestricted': True,
         'ordinal': 0,
         'staticOptions': ('EveryIteration',
                           'EveryStep',
                           'IterationInterval',
                           'LastIteration',
                           'LastStep',
                           'StepInterval'),
         'type': 'String'},
        'OutputFrequency':
        {'ordinal': 7,
         'type': 'Integer'},
        'TranscriptPrecision':
        {'ordinal': 3,
         'type': 'Integer'},
        'WriteDiagnostics':
        {'ordinal': 4,
         'type': 'Logical'},
        'WriteInitialSnapshot':
        {'ordinal': 2,
         'type': 'Logical'},
        'WriteResiduals':
        {'ordinal': 6,
         'type': 'Logical'},
        'WriteWeightsMatrix':
        {'ordinal': 5,
         'type': 'Logical'}},
       'creatableNamedChildren': [],
       'isEntity': True,
       'isNamed': False,
       'ordinal': 6},
      'SolutionControl':
      {'__children':
       {'AvailablePorts':
        {'__children':
         {},
         '__parameters':
         {'Option':
          {'isRestricted': True,
           'ordinal': 0,
           'staticOptions': ('ProgramControlled',
                             'UserDefined'),
           'type': 'String'},
          'Range':
          {'isRestricted': False,
           'ordinal': 1,
           'type': 'String'}},
         'creatableNamedChildren': [],
         'isEntity': False,
         'isNamed': False,
         'ordinal': 0}},
       '__parameters':
       {'DurationOption':
        {'isRestricted': True,
         'ordinal': 0,
         'staticOptions': ('EndTime',
                           'NumberOfSteps'),
         'type': 'String'},
        'EndTime':
        {'ordinal': 1,
         'quant': 'Time',
         'type': 'Real'},
        'MaximumIterations':
        {'ordinal': 5,
         'type': 'Integer'},
        'MinimumIterations':
        {'ordinal': 4,
         'type': 'Integer'},
        'NumberOfSteps':
        {'ordinal': 2,
         'type': 'Integer'},
        'TimeStepSize':
        {'ordinal': 3,
         'quant': 'Time',
         'type': 'Real'}},
       'creatableNamedChildren': [],
       'isEntity': True,
       'isNamed': False,
       'ordinal': 5}},
     '__parameters':
     {},
     'creatableNamedChildren': ['CouplingParticipant',
                                'CouplingInterface'],
     'isEntity': False,
     'isNamed': False,
     'ordinal': 0}
}
