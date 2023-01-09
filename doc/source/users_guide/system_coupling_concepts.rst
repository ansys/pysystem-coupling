.. _ref_syc_concepts:

System Coupling Concepts
========================

A coupled analysis involves two or more `participant` solvers. System Coupling is responsible for
coordinating the progress of each solution and for transferring variable data between the solver
at appropriate points during the solution.

For example, in a fluid-structure interaction (FSI) case, pressure data is transferred from the
fluid to the structural solver, and displacement data is transferred from the structural to the
fluid solver. Because each solver is generally working with a different mesh, the transfer of
data involves a mapping of the data from one mesh to the other, and System Coupling is
responsible for performing this task.

The main concepts therefore are:

* The `participants` --- the solvers, representing different physics types, that are being coupled.

  * The participants in turn expose various `variables` --- these are the quantities that are
    potentially available to be transferred.

  * They also expose the potential `regions` on which the data may be transferred. For example, in
    an FSI case, the relevant fluid regions would be the wall boundaries where pressure is being
    transferred to the structure.

* The `interfaces` between participants.

  * Each interface has two `sides`.

  * Each side is associated with a participant and with a subset of the regions exposed by that
    participant.

  * An interface must also define at least one `data transfer`.

* A `data transfer` is a one-way transfer of a particular variable (pressure, displacement, etc.) between
  the two participants/sides of the transfer's containing interface. For a given transfer, one of the
  sides is regarded as the source and the other the target of the data. This defines the direction of
  the transfer.

  * A coupled analysis can be `one-way` or `two-way` depending on whether transfers are defined in both
    directions on the interface.

Setting up a coupled analysis involves populating a hierarchical `data model` of settings. This data
model closely follows the concepts that have been outlined here. See :ref:`ref_syc_datamodel` for more
information.
