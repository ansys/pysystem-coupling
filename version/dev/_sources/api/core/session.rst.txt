.. _ref_session:

Session
========
The ``Session`` class is the client interface to a System Coupling service
instance, providing a Pythonic API for setting up and solving coupled analyses.

.. currentmodule:: ansys.systemcoupling.core

.. autosummary::
    :toctree: _autosummary

    session.Session

The ``Session`` class also exposes a *quasi-private* property to access
the System Coupling native API directly. For more information, see
:ref:`ref_native_api_property` and :ref:`ref_native_api_class`.