"""Pydantic base models for GeoIPS.

Intended for use by other base models.

``PluginModel`` should be used as the parent class of all other plugin models.

Other models defined here validate field types within child plugin models.
"""

# Python Standard Libraries
import keyword
import logging
from pathlib import Path

# Third-Party Libraries
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


# GeoIPS imports
from geoips.plugin_registry import plugin_registry

# from geoips import interfaces

LOG = logging.getLogger(__name__)


class PrettyBaseModel(BaseModel):
    """Make Pydantic models pretty-print by default.

    This model overrides the default string representation of Pyantic models to generate
    a user-friendly, JSON-formatted output with two-space indentation.
    """

    def __str__(self) -> str:
        """Return a pretty-print string representation of a Pydantic model.

        The returned string will be formatted as JSON with two-space indentation.

        Returns
        -------
        str
            A JSON-formatted string representation of the Pydantic model.
        """
        return self.model_dump_json(indent=2)


class StaticBaseModel(PrettyBaseModel):
    """Pydantic model with a customized ``ConfigDict`` configurations for GeoIPS.

    This model extends ``PrettyBaseModel`` and uses Pydantic ConfigDict to provide
    customized configurations such as forbidding extra fields.

    Attributes
    ----------
    model_config : ConfigDict
        Configuration for the Pydantic model:
        - `extra="forbid"`: Does not allow any additional fileds in the input data.
        - `populate_by_name=True`: Enables populaitng fields by their aliases.


    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


def python_identifier(val: str) -> str:
    """Validate if a string is a valid Python identifier.

    Validate if a string is a valid Python identifier and not a reserved Python keyword.
    See https://docs.python.org/3/reference/lexical_analysis.html#identifiers for more
    information on Python identifiers and reserved keywords.

    Validation is performed by calling `str.isidentifier` and `keyword.iskeyword`.

    Parameters
    ----------
    val : str
        The input string to validate.

    Returns
    -------
    str
        The input string if it is a valid Python identifier.

    Raises
    ------
    ValueError
        If the input string is invalid as a Python identifier or a reserved keyword.
    """
    error_messages = []
    if not val.isidentifier():
        error_messages.append(f"{val} is not a valid Python identifier.")
    if keyword.iskeyword(val):
        error_messages.append(f"{val} is a reserved Python keyword.")

    if error_messages:
        error_message = " ".join(error_messages) + " Please update it."
        LOG.error(error_message, exc_info=True)
        raise ValueError(error_message)

    return val


# Create the PythonIdentifier type
PythonIdentifier = Annotated[str, AfterValidator(python_identifier)]


class PluginModel(StaticBaseModel):
    """Base Plugin model for all GeoIPS plugins.

    This should be used as the base class for all top-level
    PluginModels. It adds standard plugin attributes for inheritance.
    It validates YAML plugins for the order based procflow.

    See the YAML plugin documentation here for more information about
    how this is used. [TODO: add link]
    """

    # TODO: constrain this list to the interfaces of GeoIPS
    interface: PythonIdentifier = Field(
        ...,
        description="""Name of the plugin's interface. Run geoips list interfaces to see
        available options.""",
    )
    family: PythonIdentifier = Field(
        ..., description="Family of the plugin."
    )  # TODO: constrain this list to the interfaces of GeoIPS
    name: PythonIdentifier = Field(..., description="Plugin name.")
    docstring: str = Field(..., description="Docstring for the plugin in numpy format.")
    description: str = Field(
        None,
        description=("A short description or defaults to first line from docstring."),
    )
    package: PythonIdentifier = Field(
        ...,
        description="Package that contains this plugin.",
        default_factory=plugin_registry.get_package_name,
    )
    relpath: str = Field(
        None, description="Path to the plugin file relative to its parent package."
    )
    abspath: str = Field(None, description="Absolute path to the plugin file.")

    # TODO: Update to have two validators, allowing for full numpy docstrings
    @model_validator(mode="before")
    def _set_description(cls, values):
        """Set ``description`` to first line of ``dosctring`` field if not provided."""
        if "description" not in values:
            # first_line_from_docstring = values["docstring"].strip().split("\n", 1)[0]
            values["description"] = values["docstring"].strip().split(".")[0]
            # return first_line_from_docstring
        return values

    @field_validator("description")
    # (length limit)
    def validate_one_line_numpy_docstring(cls: type["PluginModel"], value: str) -> str:
        """Validate string is one line, starts uppercase, and ends with a period."""
        if "\n" in value:
            raise PydanticCustomError(
                "single_line", "Docstring must be a single line.\n"
            )
        if not (value[0].isupper() and value.endswith(".")):
            raise PydanticCustomError(
                "format_error",
                "Docstring must start with a capital letter and end with a period.",
            )
        return value

    @field_validator("relpath")
    def validate_relative_path(cls: type["PluginModel"], value: str) -> str:
        """Validate string can be cast as Path and is a relative path."""
        custom_exception = PydanticCustomError(
            "relative_path_error",
            f"'relpath' must be relative path. Got '{value}'.",
        )
        try:
            path = Path(value)
        except (ValueError, TypeError) as e:
            raise custom_exception from e

        if path.is_absolute():
            raise custom_exception
        return value

    @field_validator("abspath")
    def validate_absolute_path(cls: type["PluginModel"], value: str) -> str:
        """Validate string can be cast as Path and is an absolute path."""
        custom_exception = PydanticCustomError(
            "absolute_path_error",
            f"'abspath' must be absolute path. Got '{value}'.",
        )
        try:
            path = Path(value)
        except (ValueError, TypeError) as e:
            raise custom_exception from e

        if not path.is_absolute():
            raise custom_exception
        return value
