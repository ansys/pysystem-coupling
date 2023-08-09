from ansys.systemcoupling.core.syc_version import SYC_VERSION_DOT


def get_syc_version(api) -> str:
    """Get the System Coupling version.

    The version is returned in a string like ``"23.2"``.

    System Coupling versions earlier than 23.2 (2023 R2) do not expose
    the ``GetVersion`` query. Because the first version of the server
    that PySystemCoupling is able to connect to is 23.1 (2023 R1), the
    version is assumed to be 23.1 if no version query exists.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling *native API* .
    """

    def clean_version_string(version_in: str) -> str:
        year, _, release = version_in.partition(" ")
        if len(year) == 4 and year.startswith("20") and release.startswith("R"):
            try:
                year = int(year[2:])
                release = int(release[1:])
                return f"{year}.{release}"
            except:
                pass
        raise RuntimeError(
            f"Version string {version_in} has invalid format (expect '20yy Rn')."
        )

    cmds = api.GetCommandAndQueryMetadata()
    exists = any(cmd["name"] == "GetVersion" for cmd in cmds)
    return clean_version_string(api.GetVersion()) if exists else SYC_VERSION_DOT
