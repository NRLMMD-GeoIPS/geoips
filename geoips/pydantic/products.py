"""Product plugin format."""

from typing import Literal
from pydantic import BaseModel, Field
from geoips.pydantic.bases import Plugin


class ReaderArguments(BaseModel):
    """Arguments to pass to the reader plugin."""

    variables: list[str] = Field(
        None, description="The variables to read from the input file."
    )


class ReaderStep(BaseModel):
    """A step to read data from a file."""

    # We want this to be a constant field
    # It should not need to be set in the YAML file
    # instead it should just always appear in the resulting object
    # after loading the YAML file in the order-based procflow.
    interface: str = Field(
        description="The name of the interface.",
        const=True,
        default="readers",
    )
    reader: str = Field(description="The name of the reader plugin to be used.")
    arguments: ReaderArguments = Field(
        description="The arguments to pass to the reader plugin."
    )


class ProductSpec(BaseModel):
    """The specification for a product."""

    steps: list[ReaderStep] = Field(description="The steps to produce the product.")


class ProductPlugin(Plugin):
    """A plugin that produces a product."""

    spec: ProductSpec = Field(description="The product specification")
