# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Fixtures for testing the Order-based procflow pydantic models."""

# Third-Party Libraries
import pytest


@pytest.fixture
def valid_step_data():
    """Fixture to provide sample valid plugin data for testing."""
    return {
        "type": "reader",
        "name": "abi_netcdf",
        "arguments": {
            "area_def": "None",
            "chans": ["None"],
            "metadata_only": False,
            "self_register": False,
        },
    }


@pytest.fixture
def valid_reader_arguments_model_data():
    """Fixture to provide sample valid Reader arguments for testing."""
    return {
        "area_def": "None",
        "chans": ["None"],
        "metadata_only": True,
        "self_register": True,
    }


@pytest.fixture
def valid_plugin_types():
    """Fixture to provide the list of valid plugin types."""
    VALID_PLUGIN_TYPES = [
        "algorithm",
        "procflow",
        "sector_adjuster",
        "output_checker",
        "output_formatter",
        "reader",
        "gridline_annotator",
        "product_default",
        "sector_metadata_generator",
        "product",
        "sector_spec_generator",
        "title_formatter",
        "coverage_checker",
        "feature_annotator",
        "colormapper",
        "sector",
        "interpolator",
        "filename_formatter",
    ]
    return VALID_PLUGIN_TYPES


# test_bases.py
@pytest.fixture
def valid_plugin_data():
    """Fixture providing valid sample data for Plugin model."""
    return {
        "interface": "geoips_interface",
        "family": "geoips_family",
        "name": "geoips_name",
        "docstring": "This is a valid numpy docstring.",
        "package": "geoips_package",
        "relpath": "geoips/tests/unit_tests/pydantic",
        "abspath": "/home/kumar/geoips/geoips/tests/unit_tests/pydantic",
    }
