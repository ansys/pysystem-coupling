This directory contains the following archives:

SystemCoupling-25.1-gRPC-patch-linux.tgz
SystemCoupling-25.1-gRPC-patch-windows.7z

These are for Linux and Windows respectively, to be applied to the
SystemCoupling folder of an Ansys 25 R1 (v251) installation.

WARNING: Do NOT attempt to apply to any other version of System Coupling!

You should unpack the archive from the directory above the SystemCoupling
folder in the installation.

The unpatched version of this release has an issue that affects System Coupling's
startup when it is running in the gRPC server mode that is needed by
PySystemCoupling. The patches replace various Python files in the installation
that are concerned with supporting PySystemCoupling.

PySystemCoupling releases 0.9 and greater are compatible with this patch. Earlier
releases of PySystemCoupling will not work with the 25 R1 release even if the patch
has been applied to it.

If it is not possible for you to apply the patch to the installed System Coupling,
you will have to use PySystemCoupling with a different version of the product. If
a version later than 25 R1 is available, you are recommended to use that in any case.
