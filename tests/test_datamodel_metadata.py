import pytest

"""``datamodel_metadata`` is the datamodel API that plays a role in the "native" API."""

from ansys.systemcoupling.core.native_api.datamodel_metadata import (
    build as build_metadata,
)
from dm_raw_metadata import dm_metadata


@pytest.fixture(name="metadata")
def _metadata():
    return build_metadata(dm_metadata)


def test_is_object_path(metadata) -> None:
    assert metadata.is_object_path("/SystemCoupling/Library")
    assert metadata.is_object_path("/SystemCoupling/CouplingInterface:intf1")
    assert metadata.is_object_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt"
    )


def test_is_object_path_failure(metadata) -> None:
    assert not metadata.is_object_path("/Bob")
    assert not metadata.is_object_path("/SystemCoupling/Library/Bob")
    assert not metadata.is_object_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Value"
    )


def test_is_parameter_path(metadata) -> None:
    assert metadata.is_parameter_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Value"
    )
    assert metadata.is_parameter_path("/SystemCoupling/ActivateHidden/BetaFeatures")


def test_is_parameter_path_failure(metadata) -> None:
    assert not metadata.is_parameter_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Bob"
    )
    assert not metadata.is_parameter_path(
        "/SystemCoupling/CouplingInterface:intf1/Bob:dt/Value"
    )
    assert not metadata.is_parameter_path("/SystemCoupling/Library")


def test_is_named_object_path(metadata) -> None:
    assert not metadata.is_named_object_path("/SystemCoupling/Library")
    assert metadata.is_named_object_path("/SystemCoupling/CouplingInterface:intf1")
    assert not metadata.is_named_object_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Stabilization"
    )
    assert not metadata.is_named_object_path(
        "/SystemCoupling/CouplingInterface:intf1/Bob:dt"
    )
