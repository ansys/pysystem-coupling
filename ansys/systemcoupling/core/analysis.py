from ansys.systemcoupling.core.command_metadata import CommandMetadata
from ansys.systemcoupling.core.datamodel_metadata import build as build_dm_meta
from ansys.systemcoupling.core.object_path import ObjectPath
from ansys.systemcoupling.core.path_util import join_path_strs
from ansys.systemcoupling.core.settings.datamodel import get_root
from ansys.systemcoupling.core.syc_proxy_adapter import SycProxyAdapter


class _MetaWrapper:
    def __init__(self, dm_meta, cmd_meta):
        self.__dm_meta = dm_meta
        self.__cmd_meta = cmd_meta

    def __getattr__(self, name):
        try:
            return getattr(self.__dm_meta, name)
        except AttributeError:
            return getattr(self.__cmd_meta, name)


class _DefunctRpcImpl:
    def __getattr__(self, _):
        raise RuntimeError(
            "This analysis instance has exited. Launch or " "attach to a new instance."
        )


class SycAnalysis:
    """Encapsulates a System Coupling analysis, providing access to the
    System Coupling data model and its command and query API.

    System Coupling is presumed to be running remotely and is accessed
    via the provided "rpc impl" which services command and query
    requests made via ``SycAnalysis``.
    """

    def __init__(self, rpc_impl):
        self.__setup_root = None
        self.__rpc_impl = rpc_impl
        self._init_datamodel()
        self._init_cmds()
        self.__meta_wrapper = _MetaWrapper(self.__dm_meta, self.__cmd_meta)
        self.__root = ObjectPath(
            "/" + self.__dm_meta.root_type(), self, self.__meta_wrapper
        )
        self.__top_level_types = set(self.__dm_meta.child_types(self.__root))

    def execute_command(self, name, **kwargs):
        """Execute the named command or query and return the result.

        All commands and queries take one or many keyword arguments. Some
        of these can be optional, depending on the command or query.

        A query will return a value of a type that is dependent on the
        query.

        A few commands return a value (again with a type dependent on
        the command), but most return ``None``.
        """
        return self.__rpc_impl.execute_command(name, **kwargs)

    def exit(self):
        """Close the remote System Coupling instance.

        Following this, the current instance of this class will not
        be usable. Create a new instance if required.
        """
        self.__rpc_impl.exit()
        self.__rpc_impl = _DefunctRpcImpl()
        self.__setup_root = None

    def start_output(self, handle_output=None):
        """Start streaming the "standard output" written by System Coupling.

        The "stdout" and "stderr" streams are merged into a single stream.

        By default, the output text is written to the console, but a custom
        handler may be specified that deals with it in a different way (e.g.,
        write to a file or display in a separate window). Note that if the
        default is used, the printing is done from a separate thread. This
        may lead to unusual behaviour in some Python console environments.
        In such cases, a custom approach based on the handler could be
        adopted.

        Streaming can be cancelled via the `end_output` method.

        Parameters
        ----------
        handle_output : callable
            Called with str argument that provides the latest text in the
            stream. Might represent multiple lines of output (with embedded
            newlines).
        """
        self.__rpc_impl.start_output(handle_output)

    def end_output(self):
        """Cancels output streaming previously started by `start_output`."""
        self.__rpc_impl.end_output()

    def solve(self):
        self.__rpc_impl.solve()

    def interrupt(self, reason_msg=""):
        self.__rpc_impl.interrupt(reason=reason_msg)

    def abort(self, reason_msg=""):
        self.__rpc_impl.abort(reason=reason_msg)

    def ping(self):
        return self.__rpc_impl.ping()

    @property
    def setup(self):
        """Provides access to the 'Pythonic' client-side form of the System
        Coupling API and data model.
        """
        if self.__setup_root is None:
            if isinstance(self.__rpc_impl, _DefunctRpcImpl):
                self.__rpc_impl.trigger_error

            sycproxy = SycProxyAdapter(self.__rpc_impl)
            self.__setup_root = get_root(sycproxy)
        return self.__setup_root

    def __getattr__(self, name):
        """Provides access to the native System Coupling commands and queries API
        (and, implicitly thereby, the data model settings) as attributes of
        this class's instance.

        For example, the System Coupling command ``Solve()`` may be invoked on an
        instance of this class, ``syc`` as follows:

        ``syc.Solve()``

        This is an alternative to

        ``syc.execute_command('Solve')``

        If System Coupling exposes a data model object, ``SolutionControl``
        say, then the following interactions are enabled by the present
        method.

        Query state of object:
        ``state = syc.SolutionControl.GetState()``

        (Note that this is an alternative to:
        ``state = syc.execute_command('GetState',
            ObjectPath='/SystemCoupling/SolutionControl')``)

        Query value of object property:
        ``option = syc.SolutionControl.DurationOption``

        Set multiple object object properties:
        ``syc.SolutionControl = {
            'DurationOption': 'NumberOfSteps',
            'NumberofSteps': 5
          }``

        Set single property:
        ``syc.SolutionControl.NumberOfSteps = 6``

        Full "path" syntax for the data model is supported. Thus:
        ``syc.CouplingInterface['intf1'].DataTransfer['temp']...``
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
        dm_meta_raw = self.__rpc_impl.GetMetadata()
        self.__dm_meta = build_dm_meta(dm_meta_raw)

    def _init_cmds(self):
        cmd_meta = self.__rpc_impl.GetCommandAndQueryMetadata()
        self.__cmd_meta = CommandMetadata(cmd_meta)
