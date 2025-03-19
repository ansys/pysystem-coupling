This directory contains the following archives:

SystemCoupling-25.1-gRPC-patch-linux.tgz
SystemCoupling-25.1-gRPC-patch-windows.7z

These are for Linux and Windows respectively, to be applied to the
SystemCoupling folder of an Ansys 25 R1 (v251) installation. They are intended
to be unpacked from the directory above the SystemCoupling folder in the
installation.

The unpatched version of this release has an issue that affects System Coupling's
startup in the gRPC server mode that is used by PySystemCoupling. The patches
replace various Python files in the installation that are concerned with
supporting PySystemCoupling.

PySystemCoupling releases 0.9 and greater are compatible with this patch. Earlier
releases of PySystemCoupling will not work with the 25 R1 release even if the patch
has been applied to it.

If it is not possible for you to apply the patch to the installed System Coupling,
you will have to use PySystemCoupling with an earlier version of the product.
