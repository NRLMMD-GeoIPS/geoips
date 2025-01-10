"""Pydantic base models for GeoIPS.

Intended for use by other base models.

``PluginModel`` should be used as the parent class of all other plugin models.

Other models defined here validate field types within child plugin models.
"""

# Python Standard Libraries
import keyword
from pathlib import Path
from typing import Tuple


# Third-Party Libraries
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


class PrettyBaseModel(BaseModel):
    """Make Pydantic models pretty-print by default."""

    def __str__(self) -> str:
        """Return a pretty-print string representation of a Pydantic model.

        The returned string will be formatted as JSON with two-space indentation.

        Returns
        -------
            str: A string representation of the Pydantic model.
        """
        return self.model_dump_json(indent=2)


class StaticBaseModel(PrettyBaseModel):
    """A pydantic model with a custom Pydantic ConfigDict.
    
    Future
    ------
    
    We will set these in future implementations of this class:

     - strict: False
validate_default = go for True if int type and default None are accpeted during validation
- Will the sphinx shows None if the default value is not set
str_strip_whitespace = yes
set_min_length should be set to 1
extra = allow (all plugins should accept **kwargs) on the ArgumentsModel such as Reader Arguments Model but forbid in all other places




NEW

New
10:40
populate_by_name = true
10:40
validate_assignment = True when we have Frozen as False
10:40
arbitary_types_allowed: not for YAML stuff but for class stuff
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
        val: str
            The input string to validate.

    Returns
    -------
        str: The input string if it is a valid Python identifier.

    Raises
    ------
        ValueError: If the input string is not a valid Python identifier or if it's a
        reserved Python keyword.
    """
    if not val.isidentifier():
        raise ValueError(f"{val} is not a valid Python identifier")
    if keyword.iskeyword(val):
        raise ValueError(f"{val} is a reserved Python keyword")
    return val


# Create the PythonIdentifier type
PythonIdentifier = Annotated[str, AfterValidator(python_identifier)]


class PluginModel(StaticBaseModel):
    """Base Plugin model for all GeoIPS plugins.
    
    This should be used as the base class for all top-level
    PluginModels. It adds standard plugin attributes for inheritance.
    It validates YAML plugins for the order based procflow.
    
    See the YAML plugin documentation here for more information about
    how this is used. [TODO: add link]"""

    interface: PythonIdentifier = Field(
        ..., description="The name of the plugin's interface."
    )
    family: PythonIdentifier = Field(..., description="The family of the plugin.")
    name: PythonIdentifier = Field(..., description="The name of the plugin.")
    docstring: str = Field(..., description="The docstring for the plugin.")
    package: PythonIdentifier = Field(
        None, description="The package the plugin belongs to."
    )
    relpath: str = Field(None, description="The relative path to the plugin.")
    abspath: str = Field(None, description="The absolute path to the plugin.")

    @field_validator("docstring")
    def validate_one_line_numpy_docstring(cls: type["PluginModel"], value: str) -> str:
        """Check that the docstring is a single line."""
        if "\n" in value:
            raise PydanticCustomError(
                "single_line", "The docstring should be a single line.\n"
            )
        if not (value[0].isupper() and value.endswith(".")):
            raise PydanticCustomError(
                "format_error",
                "The docstring should start with a Capital letter & end with a period",
            )
        return value

    @field_validator("relpath")
    def validate_relative_path(cls: type["PluginModel"], value: str) -> str:
        """Validate the relative path."""
        path = Path(value)

        if path.is_absolute():
            raise PydanticCustomError(
                "relative_path_error",
                "The relpath must be relative path, not an absolute path.\n\n",
            )
        return value

    @field_validator("abspath")
    def validate_absolute_path(cls: type["PluginModel"], value: str) -> str:
        """Validate absolute path."""
        path = Path(value)
        if not path.is_absolute():
            raise PydanticCustomError(
                "absolute_path_error", "The path must be an absolute path.\n\n"
            )
        return value


def mpl_artist_args(args: dict, artist: Artist) -> dict:
    """Validate the arguments for a matplotlib artist."""
    line = artist([0, 1], [0, 1])
    for key, arg in args.items():
        if key == "enabled":
            continue
        line.set(**{key: arg})
    return args


def line_args(args: dict) -> dict:
    """Validate the arguments for a matplotlib line."""
    return mpl_artist_args(args, Line2D([0, 1], [0, 1]))


LineArgs = Annotated[dict, AfterValidator(line_args)]


def lat_lon_coordinate(arg: tuple[float, float]) -> tuple[float, float]:
    """Validate a latitude and longitude coordinate."""
    if arg[0] < -90 or arg[0] > 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if arg[1] < -180 or arg[1] > 180:
        raise ValueError("Longitude must be between -180 and 180.")
    return arg


LatLonCoordinate = Annotated[Tuple[float, float], AfterValidator(lat_lon_coordinate)]
