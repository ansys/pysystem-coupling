from copy import deepcopy
import json

command_modes = {}
with open("command_query_names.txt") as f:
    for line in f:
        cmd = line.strip()
        command_modes[cmd] = "default"

with open("command_query_names_gui.txt") as f:
    for line in f:
        cmd = line.strip()
        if cmd not in command_modes:
            command_modes[cmd] = "gui"

with open("command_query_names_test.txt") as f:
    for line in f:
        cmd = line.strip()
        if cmd not in command_modes:
            command_modes[cmd] = "test"

with open("command_query_test.json") as f:
    cmd_data = json.load(f)

# Basic transformation

cmd_dict = {}
arg_name_use = {}
arg_types = set()
ret_types = set()
for cmd_info in cmd_data:
    name = cmd_info["name"]
    mode = command_modes.get(name, "unknown")
    if mode == "test":
        continue
    info = deepcopy(cmd_info)
    info["mode"] = mode
    del info["name"]
    cmd_dict[name] = info

    ret_types.add(info["retType"])

    for arg, arg_data in info["args"].items():
        arg_uses = arg_name_use.setdefault(arg, set())
        arg_uses.add(name)
        arg_type = arg_data["Type"]
        arg_types.add(arg_type)


with open("command_query_info.json", "w") as f:
    json.dump(cmd_dict, fp=f, indent=2, sort_keys=True)

with open("arg_names_and_uses.json", "w") as f:
    arg_name_use = {arg: list(uses) for arg, uses in arg_name_use.items()}
    json.dump(arg_name_use, fp=f, indent=2, sort_keys=True)

with open("arg_types.json", "w") as f:
    json.dump(list(arg_types), fp=f, indent=2, sort_keys=True)

with open("ret_types.json", "w") as f:
    json.dump(list(ret_types), fp=f, indent=2, sort_keys=True)
