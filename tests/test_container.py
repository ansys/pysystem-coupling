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
    assert set(setup.library.expression.keys()) == set(["expr1", "expr2"])
    assert set(setup.library.expression.get_object_names()) == set(["expr1", "expr2"])

    expr2.expression_name = "bob"
    expr2.expression_string = "2 * x"

    assert expr2.expression_string == "2 * x"

    del setup.library.expression["expr2"]
    assert list(setup.library.expression.keys()) == ["expr1"]
    assert setup.library.expression.get_object_names() == ["expr1"]

    syc.exit()


def test_more_datamodel_operations() -> None:
    syc = pysystemcoupling.launch_container()
    assert syc.ping()

    setup = syc.setup

    setup.activate_hidden.beta_features = True
    setup.activate_hidden.alpha_features = True

    frame_name = setup.add_reference_frame()

    frame = setup.library.reference_frame[frame_name]

    assert frame.get_property_options("option")

    state = setup.get_state()
    assert "activate_hidden" in state and "library" in state


def test_streaming() -> None:
    syc = pysystemcoupling.launch_container()
    assert syc.ping()

    setup = syc.setup
    for i in range(5):
        expr = setup.library.expression.create(f"expr{i}")
        expr.expression_name = f"expr_{i}"
        expr.expression_string = f"{i+1} * x"

    def handle_output(text):
        handle_output.buf += text

    handle_output.buf = ""

    syc.start_output(handle_output=handle_output)

    native_api = syc._native_api
    for i in range(5):
        native_api.PrintState()

    syc.end_output()

    assert "expr_2" in handle_output.buf
