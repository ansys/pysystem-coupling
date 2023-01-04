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

Build the generated API code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the packaged version of PySystemCoupling, Python classes are generated during the
package build to provide an API to System Coupling facilities. The classes are largely
generated from metadata queried from a running instance of System Coupling.

For local development, you need to perform this additional generation step manually,
following the installation as described above.

.. code::

    pip install .[classesgen]
    python scripts/generate_datamodel.py


Build documentation
-------------------
To build the PySystemCoupling documentation locally, in the root directory of the
repository, run:

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
