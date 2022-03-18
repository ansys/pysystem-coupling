import glob
import os
from pathlib import Path
import re
import shutil

from grpc_tools import protoc

_THIS_DIRNAME = os.path.dirname(__file__)
_PROTOS_PATH = os.path.abspath(
    os.path.join(_THIS_DIRNAME, "..", "protos", "ansys", "api", "systemcoupling", "v0")
)
_PY_OUT_PATH = os.path.abspath(
    os.path.join(_THIS_DIRNAME, "..", "ansys", "api", "systemcoupling", "v0")
)
_PACKAGE_NAME = "ansys.api.systemcoupling.v0"

out_path = _PY_OUT_PATH
protos_path = _PROTOS_PATH

shutil.rmtree(out_path, ignore_errors=True)
Path.mkdir(Path(out_path), parents=True, exist_ok=True)

proto_files = glob.glob(os.path.join(protos_path, "*.proto"), recursive=True)

args = (
    "",
    f"-I{protos_path}",
    f"--python_out={out_path}",
    f"--grpc_python_out={out_path}",
    *proto_files,
)
protoc.main(args)

grpc_source_files = glob.glob(os.path.join(out_path, "*.py"), recursive=True)
py_source = {}
for filename in grpc_source_files:
    relative_path = filename.replace(out_path, "")
    module_name = ".".join(re.split(r"\\|/", relative_path))
    module_name = module_name.rstrip(".py").strip(".")
    with open(filename) as f:
        py_source[module_name] = f.read()

# The default protoc-generated Python does not handle relative
# imports of generate modules well (it probably worked for Python 2)
# So, for example, replace
#     import variant_pb2 as variant__pb2
# with
#     import ansys.api.systemcoupling.v0.variant_pb2 as variant__pb2
for module_name in py_source:
    find_str = f"import {module_name}"
    repl_str = f"import {_PACKAGE_NAME}.{module_name}"
    for mod_name, mod_source in py_source.items():
        py_source[mod_name] = mod_source.replace(find_str, repl_str)

# write python source
for module_name, module_source in py_source.items():
    relative_module_path = module_name.split(".")
    relative_module_path[-1] = f"{relative_module_path[-1]}.py"
    filename = os.path.join(out_path, *relative_module_path)

    with open(filename, "w") as f:
        f.write(module_source)
