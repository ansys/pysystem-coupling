.. _ref_index_api:

.. currentmodule:: ansys.systemcoupling

=============
API reference
=============

There are three main "levels" of interaction with the PySystemCoupling API:

* Launching and/or connecting to a System Coupling server instance by calling
  :func:`launch<core.launch>` or :func:`connect<core.connect>`. These functions
  returns a :class:`Session<core.session.Session>` object by means of
  which the user may interact with the System Coupling server.
* The :class:`Session<core.session.Session>` object itself provides some high-level
  capability such as controlling streaming of standard streams from the server,
  and lifetime management of the session. It also contains three important attributes, ``case``, ``setup`` and
  ``solution`` through which the user gains access to the third aspect of the API.
* The :meth:`case<core.session.Session.case>`, :meth:`setup<core.session.Session.setup>`
  and :meth:`solution<core.session.Session.solution>` attributes of :class:`Session<core.session.Session>` are
  *root* objects that constitute an entry point to an *adaptor* API for core System Coupling features.
  The bulk of the PySystemCoupling API resides under these roots. This is where most of the
  interactions required to set up and solve a coupled analysis take place.

.. autosummary::
   :toctree: _autosummary

.. toctree::
   :maxdepth: 4
   :hidden:

   core/launching
   core/session
   core/adaptor/api
