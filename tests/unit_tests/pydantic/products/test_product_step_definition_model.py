# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Test Order-based procflow ProductStepDefinition Model."""


# Python Standard Libraries
import copy

# Third-Party Libraries
from pydantic import ValidationError
import pytest

# GeoIPS Libraries
from geoips.pydantic import products


def test_good_product_step_definition_model_valid_step(valid_step_data):
    """Tests ProductStepDefinitionModel with valid data."""
    # creating an instance of PSDModel
    model = products.ProductStepDefinitionModel(**valid_step_data)

    assert model.type == "reader"
    assert model.name == "abi_netcdf"
    assert model.arguments == {
        "area_def": "None",
        "chans": ["None"],
        "metadata_only": False,
        "self_register": False,
    }


def test_bad_product_step_definition_model_invalid_field_type(
    mocker, valid_reader_arguments_model_data, valid_step_data
):
    """Tests ProductStepDefinitionModel for invalid field type instantiation."""

    def mock_init(self, **kwargs):
        self.__dict__.update(kwargs)

    mocker.patch.object(products.ProductStepDefinitionModel, "__init__", mock_init)

    invalid_test_data_PSDModel = {
        "type": 123,
        "name": 123,
        "arguments": valid_reader_arguments_model_data,
    }
    model = products.ProductStepDefinitionModel(**invalid_test_data_PSDModel)

    assert model.type == 123, "Expected 'type' to retain the invalid value"
    assert model.name == 123, "Expected 'name' to retain the invalid value"


def test_bad_product_step_definition_model_additional_field(valid_step_data):
    """Tests ReaderArgumentsModel with additonal field."""
    invalid_data = copy.deepcopy(valid_step_data)
    invalid_data["unexpected_field"] = "unexpected_value"

    with pytest.raises(ValidationError) as exec_info:
        products.ProductStepDefinitionModel(**invalid_data)

    error_info = exec_info.value.errors()
    assert any(
        err["type"] == "extra_forbidden" for err in error_info
    ), "expected 'extra_frobidden' error type"
    assert "unexpected_field" in str(
        exec_info.value
    ), "Unexpected field should be rejected by the ProductStepDefinitionModel"
