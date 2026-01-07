# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ansys.systemcoupling.core.native_api.command_metadata import CommandMetadata
from ansys.systemcoupling.core.native_api.datamodel_metadata import (
    build as build_dm_meta,
)
from ansys.systemcoupling.core.util.logging import LOG
from ansys.systemcoupling.core.util.pathstr import join_path_strs

from .meta_wrapper import MetaWrapper
from .object_path import ObjectPath


class NativeApi:
    """Exposes the *native* System Coupling command and query API into
    PySystemCoupling.

    This class allows commands and queries to be scripted similarly to how it
    is done in System Coupling's own command-line interface (CLI). The main difference
    is that rather than being exposed into the global Python environment,
    here commands and queries are made available as attributes of this class.

    The path-based syntax of the native API is also supported. However,
    instead of using the global ``DatamodelRoot()`` query as the path root,
    use the instance of this class as the root. (Note that while
    ``DatamodelRoot`` can be called here, it returns the string value
    of the root path, so it cannot be used in the same way as in the System
    Coupling CLI.)
    """

    def __init__(self, rpc_impl):
        """Create an instance of the ``NativeApi`` class.

        Parameters
        ----------
        rpc_impl
            Provider of remote command and query services.
        """
        self.__rpc_impl = rpc_impl
        LOG.debug("NativeApi: initialize datamodel...")
        self._init_datamodel()
        LOG.debug("NativeApi: initialize commands...")
        self._init_cmds()
        LOG.debug("...done")
        self.__meta_wrapper = MetaWrapper(self.__dm_meta, self.__cmd_meta)
        self.__root = ObjectPath(
            "/" + self.__dm_meta.root_type(), self, self.__meta_wrapper
        )
        self.__top_level_types = set(self.__dm_meta.child_types(self.__root))

    def execute_command(self, name, **kwargs):
        """Execute the named command or query and return the result.

        All commands and queries take one or more keyword arguments. Some
        of these arguments can be optional, depending on the command or query.

        A query returns a value of a type that is dependent on the
        query.

        A few commands return a value (again with a type dependent on
        the command), but most return ``None``.

        Note that the `__getattr__`-based exposure of the API provides
        a more convenient syntax.

        Parameters
        ----------
        name
            Name of the command (or query) to execute.
        kwargs
            Keyword arguments to the command.
        """
        return self.__rpc_impl.execute_command(name, **kwargs)

    def __getattr__(self, name):
        """Provides access to the native System Coupling commands and queries API
        as attributes of this class's instance.

        For example, the System Coupling ``Solve()`` command can be invoked on an
        instance of the ``syc`` class as follows::

            syc.Solve()

        .. note:: This is equivalent to using the `execute_command` method like this:

            ``syc.execute_command('Solve')``

        This method also supports a convenient data model access syntax, which is
        very close to that available in the native CLI.

        For example, if System Coupling exposes a data model object ``SolutionControl``,
        then various operations are supported, as shown below.

            Query state of object::

                state = syc.SolutionControl.GetState()

            Note that this is an alternative to::

                state = syc.execute_command('GetState',
                                            ObjectPath='/SystemCoupling/SolutionControl')

            Query value of object property::

                option = syc.SolutionControl.DurationOption


            Set multiple object object properties::

                syc.SolutionControl = {
                    'DurationOption': 'NumberOfSteps',
                    'NumberofSteps': 5
                }

            Set single property::

                syc.SolutionControl.NumberOfSteps = 6

        In general, full "path" access to the data model is supported, including
        named object syntax familiar from the native CLI::

            syc.CouplingInterface['intf1'].DataTransfer['temp']...

        Parameters
        ----------
        name
            Name of the attribute being accessed.
        """
        if self.__cmd_meta.is_command_or_query(name):
            # Looks like an API command/query call
            def non_objpath_cmd(**kwargs):
                return self.__rpc_impl.execute_command(name, **kwargs)

            def objpath_cmd(**kwargs):
                if "ObjectPath" not in kwargs:
                    return self.__rpc_impl.execute_command(
                        name, ObjectPath=self.__root, **kwargs
                    )
                return self.__rpc_impl.execute_command(name, **kwargs)

            if not self.__cmd_meta.is_objpath_command_or_query(name):
                return non_objpath_cmd
            else:
                return objpath_cmd

        if not name in self.__top_level_types:
            raise AttributeError(f"Unknown attribute of System Coupling API: '{name}'")

        # Can assume accessing a datamodel path
        return self.__root.make_path(join_path_strs(self.__root, name))

    def _init_datamodel(self):
        LOG.debug("Query for metadata")
        dm_meta_raw = self.__rpc_impl.GetMetadata(json_ret=True)
        LOG.debug("Build local metadata")
        self.__dm_meta = build_dm_meta(dm_meta_raw)
        LOG.debug("...datamodel metadata initialized for native API")

    def _init_cmds(self):
        cmd_meta = self.__rpc_impl.GetCommandAndQueryMetadata()
        self.__cmd_meta = CommandMetadata(cmd_meta)

    def _exit(self, rpc_impl=None):
        self.__rpc_impl = rpc_impl
