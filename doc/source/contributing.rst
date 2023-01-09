.. _ref_contributing:

============
Contributing
============
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/overview/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
it and all `Guidelines and Best Practices
<https://dev.docs.pyansys.com/guidelines/index.html>`_ before attempting to
contribute to PySystemCoupling.

The following contribution information is specific to PySystemCoupling.

Clone the repository
--------------------
To clone and install the latest PySystemCoupling release in development
mode, run:

.. code::

    git clone https://github.com/pyansys/pysystem-coupling.git
    cd pysystem-coupling
    python -m pip install --upgrade pip
    pip install -e .

.. _ref_generate_api:

Build the generated API code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the packaged version of PySystemCoupling, Python classes are generated during the
package build to provide an API to System Coupling facilities. The classes are largely
generated from metadata queried from a running instance of System Coupling.

For local development, you need to perform this additional generation step manually,
after the preceding installation steps.

.. code::

    pip install .[classesgen]
    python scripts/generate_datamodel.py

The generated code is written to a directory ``src/ansys/systemcoupling/core/adaptor/api_<version>``,
where ``<version>`` is the version of the System Coupling instance that was run in the background
by the generation script. The version takes the form ``23_1``, for example, which would correspond to
the 2023 Release 1 of Ansys. ``23_1`` is in fact the current default and this release of System
Coupling would be expected to be at an installation location given by the ``AWP_ROOT231`` environment
variable.

You can override the default behavior and run a different version -- and generate the API classes for
this different version -- by setting either
``SYSC_ROOT`` to point to the root directory of a System Coupling installation or ``AWP_ROOT`` to
point to the root of an Ansys installation. If ``SYSC_ROOT`` and ``AWP_ROOT`` are both set, the
former takes priority, and both take priority over ``AWP_ROOT231``.


Build documentation
-------------------
To build the PySystemCoupling documentation locally, the API classes must first have been generated
as outlined in :ref:`ref_generate_api`, because some of the documentation is extracted from these classes. Since
multiple versions of the API classes can exist, it is necessary to
set the environment variable ``PYSYC_DOC_BUILD_VERSION`` to tell the documentation build which
version to use. This *must* be set -- there is no default in this case. This variable should be set to a string that has the same form as the ``<version>`` component
of the ``api_<version>`` directory (for example, "23_1").

With this variable set, execute the following commands:

.. code::

    pip install .[doc]
    cd doc
    make html

After the build completes, the HTML documentation is located in the
``_builds/html`` directory. You can load the ``index.html`` file in
this directory into a web browser.

You can clear all HTML files from the ``_builds/html`` directory with:

.. code::

    make clean

Sphinx Gallery examples
^^^^^^^^^^^^^^^^^^^^^^^
By default, the `Sphinx Gallery` examples are *not* run as part of a documentation build. This is
because realistic runs of System Coupling, involving both System Coupling itself *and* the
participant solvers, are not currently possible on GitHub. Therefore, the examples are run
manually from time to time, and the resultant `Sphinx` files are committed to the repository.

To override the default behavior and perform a complete rebuild of documentation, including
regeneration of the `Sphinx Gallery` examples, set the ``PYSYC_BUILD_SPHINX_GALLERY``
environment variable (only its existence is examined so it may be given any value).




Post issues
-----------
Use the `PySystemCoupling Issues <https://github.com/pyansys/pysystem-coupling/issues>`_ page to
submit questions, report bugs, and request new features.


Adhere to code style
--------------------
PySystemCoupling is compliant with the `PyAnsys code style
<https://dev.docs.pyansys.com/coding-style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to check the code style. You can
install and activate this tool with:

.. code:: bash

   python -m pip install pre-commit
   pre-commit install

The ``pre-commit`` style checks will then run automatically on every ``git commit``
to your branch.

Alternatively, you can directly run `pre-commit <https://pre-commit.com/>`_ at any time with:

.. code:: bash

    pre-commit run --all-files --show-diff-on-failure
