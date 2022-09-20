from ansys.systemcoupling.core.util import yaml_helper


def test_write_to_string() -> None:

    d = {}

    d["A"] = {"text": ("This is a multi-\n" "line\n" "string.")}
    d["B"] = {"text": ("And\n" "  so\n" "    is\n" "      this.")}

    expect = (
        "A:\n"
        "    text: |-\n"
        "        This is a multi-\n"
        "        line\n"
        "        string.\n"
        "B:\n"
        "    text: |-\n"
        "        And\n"
        "          so\n"
        "            is\n"
        "              this.\n"
    )

    ys = yaml_helper.yaml_dump_to_string(d, sort_keys=True)
    assert ys == expect
