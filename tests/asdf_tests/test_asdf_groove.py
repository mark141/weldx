"""Test all ASDF groove implementations."""

import matplotlib.pyplot as plt
import pytest

from weldx.asdf.tags.weldx.core.iso_groove import (
    BaseGroove,
    _create_test_grooves,
    get_groove,
)
from weldx.asdf.utils import _write_read_buffer
from weldx.constants import WELDX_QUANTITY as Q_
from weldx.geometry import Profile

test_params = _create_test_grooves()


@pytest.mark.parametrize(
    "groove, expected_dtype", test_params.values(), ids=test_params.keys()
)
def test_asdf_groove(groove: BaseGroove, expected_dtype):
    """Test ASDF functionality for all grooves.

    Parameters
    ----------
    groove:
       Groove instance to be tested.

    expected_dtype:
       Expected type of the groove to be tested.

    """
    k = "groove"
    tree = {k: groove}

    data = _write_read_buffer(tree)
    assert isinstance(
        data[k], expected_dtype
    ), f"Did not match expected type {expected_dtype} on item {data[k]}"
    # test content equality using dataclass built-in functions
    assert (
        groove == data[k]
    ), f"Could not correctly reconstruct groove of type {type(groove)}"
    # test to_profile
    assert isinstance(
        groove.to_profile(), Profile
    ), f"Error calling plot function of {type(groove)} "

    # call plot function
    fig, ax = plt.subplots()
    groove.plot(ax=ax)
    plt.close(fig)


def test_asdf_groove_exceptions():
    """Test special cases and exceptions of groove classes."""
    # test parameter string generation
    v_groove = get_groove(
        groove_type="VGroove",
        workpiece_thickness=Q_(9, "mm"),
        groove_angle=Q_(50, "deg"),
        root_face=Q_(4, "mm"),
        root_gap=Q_(2, "mm"),
    )

    assert set(v_groove.param_strings()) == {
        "alpha=50 deg",
        "b=2 mm",
        "c=4 mm",
        "t=9 mm",
    }

    # test custom groove axis labels
    fig, _ = plt.subplots()
    v_groove.plot(axis_label=["x", "y"])
    plt.close(fig)

    # test exceptions
    with pytest.raises(ValueError):
        get_groove(
            groove_type="WrongGrooveString",
            workpiece_thickness=Q_(9, "mm"),
            groove_angle=Q_(50, "deg"),
        )

    with pytest.raises(NotImplementedError):
        BaseGroove().to_profile()

    with pytest.raises(ValueError):
        get_groove(
            groove_type="FrontalFaceGroove",
            workpiece_thickness=Q_(2, "mm"),
            workpiece_thickness2=Q_(5, "mm"),
            groove_angle=Q_(80, "deg"),
            root_gap=Q_(1, "mm"),
            code_number="6.1.1",
        ).to_profile()