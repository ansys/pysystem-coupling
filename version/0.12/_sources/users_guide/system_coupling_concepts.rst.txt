.. _ref_syc_concepts:

System Coupling concepts
========================

A coupled analysis involves two or more *participant* solvers. System Coupling is responsible for
coordinating the progress of each solution and for transferring variable data between the solvers
at appropriate points during the solution.

For example, in a Fluid-Structure Interaction (FSI) case, pressure data is transferred from the
fluid to the structural solver, and displacement data is transferred from the structural solver
to the fluid solver. Because each solver is generally working with a different mesh, the transfer
of data involves a mapping of the data from one mesh to the other. System Coupling is responsible
for performing this task.

Descriptions follow of the main concepts.

Participants
 These are the solvers, representing different physics types, that are being coupled.

    Variables
     The participants expose *variables*. These are the quantities that are potentially available
     to be transferred.
     
    Regions
     The participants also expose the potential *regions* on which the data may be transferred.
     For example, in an FSI case, the relevant fluid regions would be the wall boundaries where
     pressure is being transferred to the structure.

Interfaces
 These are the *interfaces* between participants.

    Sides    
     Each interface has two *sides*.
     
     Each side is associated with a participant and with a subset of the regions exposed by
     this participant.
    
    Data transfers
     Each interface must define at least one *data transfer*, which is a one-way transfer of
     a particular variable (such as pressure or displacement) between the two participants'
     sides of the transfer's containing interface. For a given transfer, one of the sides
     is regarded as the *source* of the data, and the other side is regarded as the *target*
     of the data. This defines the direction of the transfer.
     
     A coupled analysis can be *one-way* or *two-way*, depending on whether transfers are
     defined in one or both directions on the interface.

Data model
 Setting up a coupled analysis involves populating a hierarchical *data model* of settings.
 The data model closely follows the concepts that have been outlined here. For more information,
 see  :ref:`ref_syc_datamodel`.
