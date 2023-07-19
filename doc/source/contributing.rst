.. _ref_contributing:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/dev/how-to/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
this guide before attempting to contribute to PySystemCoupling.

The following contribution information is specific to PySystemCoupling.

Clone the repository
--------------------
To clone and install the latest PySystemCoupling release in development
mode, run:

.. code::

    git clone https://github.com/ansys/pysystem-coupling.git
    cd pysystem-coupling
    python -m pip install --upgrade pip
    pip install -e .

.. _ref_generate_api:

Build the generated API code
----------------------------
In the packaged version of PySystemCoupling, Python classes are generated during the
package build to provide an API to System Coupling facilities. The classes are largely
generated from metadata queried from a running instance of System Coupling.

For local development, you must perform this additional generation step manually,
after the preceding steps for cloning and installing the package.

.. code::

    pip install -e .[classesgen]
    python scripts/generate_datamodel.py


The generated code is written to the directory ``src/ansys/systemcoupling/core/adaptor/api_<version>``,
where ``<version>`` is the version of the System Coupling instance that was run in the background
by the generation script. For example, the version ``23_2`` corresponds to the System Coupling 2023 R2.
The default is ``23_2``, which means that this release of System Coupling is expected to be at the
installation location given by the ``AWP_ROOT232`` environment variable.

You can override the default behavior and run a different version, and generate the API classes for
this different version, by setting either the ``SYSC_ROOT`` environment variable to point to the
root directory of your System Coupling installation or the ``AWP_ROOT`` environment variable to
point to the root of an Ansys installation. If ``SYSC_ROOT`` and ``AWP_ROOT`` environment variables
are both set, the former takes priority. Additionally, both of these environment variables take priority
over the ``AWP_ROOT232`` environment variable.


Build documentation
-------------------
To build the PySystemCoupling documentation locally, you must have first generated the API classes
as described in :ref:`ref_generate_api`. This is because some of the documentation is extracted
from these classes.

Because multiple versions of the API classes can exist, you must set the ``PYSYC_DOC_BUILD_VERSION``
environment variable to tell the documentation build which version to use. Given that there is
no default for this environment variable, you *must* set it. The value should be a string in the
same form as the ``<version>`` component of the ``api_<version>`` directory. For example,
"23_2".

With this variable set, run this code to build the documentation:

.. code::

    pip install -e .[doc]
    cd doc
    make html

After the build completes, the HTML documentation is located in the
``_builds/html`` directory. You can load the ``index.html`` file in
this directory into a web browser.

You can clear all HTML files from the ``_builds/html`` directory with:

.. code::

    make clean

Run Sphinx Gallery examples
---------------------------
The *Sphinx Gallery* examples are *not* run as part of a documentation build by default.
This is because realistic runs of System Coupling, involving both System Coupling itself
*and* the participant solvers, are not currently possible on GitHub. Therefore, examples
are run manually from time to time and the resulting `Sphinx` files are committed to the
repository.

To override the default behavior and rebuild the entire documentation, including
regeneration of the Sphinx Gallery examples, set the ``PYSYC_BUILD_SPHINX_GALLERY``
environment variable. Because only its existence is examined, you can give any value
to this environment variable.

Post issues
-----------
Use the `PySystemCoupling Issues <https://github.com/ansys/pysystem-coupling/issues>`_ page to
submit questions, report bugs, and request new features.


Adhere to code style
--------------------
PySystemCoupling is compliant with the `PyAnsys code style
<https://dev.docs.pyansys.com/dev/coding-style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to check the code style. You can
install and activate this tool with:

.. code:: bash

   python -m pip install pre-commit
   pre-commit install

When pre-commit is active, it automatically runs style checks on every ``git commit``
to your branch.

Alternatively, you can directly run `pre-commit <https://pre-commit.com/>`_ at any time
with this command:

.. code:: bash

    pre-commit run --all-files --show-diff-on-failure
