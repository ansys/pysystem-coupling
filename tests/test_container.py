import time

import ansys.systemcoupling.core as pysystemcoupling


def test_start_and_connect() -> None:
    with pysystemcoupling.launch_container() as syc:
        assert syc.ping()


def test_start_and_connect_container_env_var(with_launching_container) -> None:
    with pysystemcoupling.launch() as syc:
        assert syc.ping()


def test_set_and_get() -> None:
    with pysystemcoupling.launch_container() as syc:
        assert syc.ping()

        setup = syc.setup
        setup.library.expression.create("expr1")

        assert list(setup.library.expression.keys()) == ["expr1"]
        assert setup.library.expression.get_object_names() == ["expr1"]

        expr2 = setup.library.expression.create("expr2")
        assert set(setup.library.expression.keys()) == set(["expr1", "expr2"])
        assert set(setup.library.expression.get_object_names()) == set(
            ["expr1", "expr2"]
        )

        expr2.expression_name = "bob"
        expr2.expression_string = "2 * x"

        assert expr2.expression_string == "2 * x"

        del setup.library.expression["expr2"]
        assert list(setup.library.expression.keys()) == ["expr1"]
        assert setup.library.expression.get_object_names() == ["expr1"]


def test_more_datamodel_operations() -> None:
    with pysystemcoupling.launch_container() as syc:
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
    with pysystemcoupling.launch_container() as syc:
        assert syc.ping()

        # Set some state up
        setup = syc.setup
        for i in range(5):
            expr = setup.library.expression.create(f"expr{i}")
            expr.expression_name = f"expr_{i}"
            expr.expression_string = f"{i+1} * x"

        # Turn streaming output on, with a custom handler
        def handle_output(text):
            handle_output.buf += text

        handle_output.buf = ""

        syc.start_output(handle_output=handle_output)

        # Use native 'PrintState' which will generate some stdout
        native_api = syc._native_api
        for i in range(5):
            native_api.PrintState()
        # output is managed on separate thread and sometimes doesn't
        # flush immediately
        time.sleep(5)
        syc.end_output()

        # Rough test that we got some output
        assert "expr_2" in handle_output.buf

        # Reset output and verify no streaming
        handle_output.buf = ""
        for i in range(5):
            native_api.PrintState()
        assert handle_output.buf == ""


def test_misc_items_for_coverage() -> None:
    # Mop up some coverage items that are
    # relatively difficult to probe.
    with pysystemcoupling.launch_container() as syc:
        assert syc.ping()

        # Force error response in generic command handling
        native_api = syc._native_api
        try:
            native_api.AddNamedExpression()
            assert False, "Exception expected"
        except RuntimeError:
            pass

        # Access case and solution apis.
        # (Accessors not currently exercised otherwise.)
        syc.case
        solution = syc.solution

        # Try calling solve even though we know it will fail.
        # This exercises specialised error handling on solve and "injected commands".
        try:
            solution.solve()
            assert False, "Exception expected"
        except RuntimeError:
            pass
