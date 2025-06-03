.. _basic_settings_types:

:orphan:

Basic setting types
====================

Although organized hierarchically into dictionary-like structures, all System
Coupling settings are ultimately instances of basic Python built-in types or are simple
containers of such types.

The basic types are:

- String (``str``)
- Integer (``int``)
- Real (``float``)
- Boolean (``bool``)

System Coupling supports expressions for real valued settings, and these are specified as strings.
Therefore a Python `type hint` :ref:`RealType<real_type>` is defined in the API to
allow this option to be expressed.

Similarly, type hints are defined for the derived list types.

These additional type hint definitions are documented in the following sections.


.. _real_type:

``RealType``
~~~~~~~~~~~~

``Union[float, str]`` - the underlying data model type is ``float`` but an expression string may also
be assigned.

.. _string_list_type:

``StringListType``
~~~~~~~~~~~~~~~~~~~

``List[str]`` - list of ``str`` values.

.. _integer_list_type:

``IntegerListType``
~~~~~~~~~~~~~~~~~~~~

``List[int]`` - list of ``int`` values.

.. _real_list_type:

``RealListType``
~~~~~~~~~~~~~~~~~

``List[RealType]`` - list of :ref:`RealType<real_type>` values.

.. _real_vector_type:

``RealVectorType``
~~~~~~~~~~~~~~~~~~~

``Tuple[RealType, RealType, RealType]`` - 3-tuple of :ref:`RealType<real_type>` values. Holds a real 3D vector or coordinate value.

.. _bool_list_type:

``BoolListType``
~~~~~~~~~~~~~~~~~

``List[bool]`` - list of ``bool`` values.