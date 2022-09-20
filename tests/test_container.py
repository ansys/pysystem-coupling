import ansys.systemcoupling.core as pysystemcoupling


def test_start_and_connect() -> None:
    syc = pysystemcoupling.launch_container()
    assert syc.ping()
    syc.exit()


def test_start_and_connect_container_env_var(with_launching_container) -> None:
    syc = pysystemcoupling.launch()
    assert syc.ping()
    syc.exit()


def test_set_and_get() -> None:
    syc = pysystemcoupling.launch_container()
    assert syc.ping()

    setup = syc.setup
    setup.library.expression.create("expr1")

    assert list(setup.library.expression.keys()) == ["expr1"]
    assert setup.library.expression.get_object_names() == ["expr1"]

    expr2 = setup.library.expression.create("expr2")
    assert list(setup.library.expression.keys()) == ["expr1", "expr2"]
    assert setup.library.expression.get_object_names() == ["expr1", "expr2"]

    expr2.expression_name = "bob"
    expr2.expression_string = "2 * x"

    assert expr2.expression_string == "2 * x"

    del setup.library.expression["expr2"]
    assert list(setup.library.expression.keys()) == ["expr1"]
    assert setup.library.expression.get_object_names() == ["expr1"]

    syc.exit()
