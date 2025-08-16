import logging
from collections.abc import Sequence
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field

logger = logging.getLogger("service.core.entity")

class ErrorEntity(BaseModel):
    code: str
    message: str
    request_id: UUID | None = Field(default=None, description="Request ID for the request that caused the error")
    addional_info: Any | None = Field(default=None, description="Additional information related to the error")



class ListCriterion(BaseModel):
    sort_field: str | None = Field(description="Must be a field returned by the list", default=None)
    sort_direction: Literal["asc", "desc"] = Field(default="asc", description="Sort direction, asc or desc")
    limit: int = Field(lt=1000, default=100)
    offset: int = Field(gt=-1, default=0)
    filter: str | None = Field(
        default=None,
        description="Filter to apply to the list. Must be a valid JSON string.",
    )


class ListResponse[DataType](BaseModel):
    """
    Represents a paginated list response containing a sequence of items and metadata about the pagination.

    Attributes:
        data (Sequence[DataType]): List of items of type `DataType`.
        limit (int): The maximum number of items per page.
        offset (int): The starting index of the current page.
        total (int): The total number of items available.
    """
    data: Sequence[DataType] = Field(description="List of items")
    limit: int = Field(description="Page size")
    offset: int = Field(description="Page number")
    total: int = Field(description="Total number of items")


class FilterDefinition(BaseModel):
    """
    FilterDefinition is a model that defines the structure of a filter used in the application.

    Attributes:
        type (Literal["fts", "date_range", "select"]): Specifies the type of the filter. 
            Possible values are:
            - "fts": Full-text search filter.
            - "date_range": Filter based on a range of dates.
            - "select": Filter with selectable options.
            Defaults to "fts".
        is_multiselect (bool): Indicates whether the filter allows multiple selections.
            Defaults to False.
        select_options (Sequence[dict[str, str]]): A list of selectable options for the filter.
            Each option is represented as a dictionary with string keys and values.
            Defaults to an empty list.
    """
    type: Literal["fts", "date_range", "select"] = Field(description="Filter type", default="fts")
    is_multiselect: bool = Field(description="Is the filter multiselect", default=False)
    select_options: Sequence[dict[str, str]] = Field(description="List of options for the filter", default_factory=list)


class ListOptionField(BaseModel):
    """
    Represents a list option field with metadata for display, filtering, and sorting.

    Attributes:
        field (str): The name of the field.
        name (str): The display name of the field.
        filterable (FilterDefinition | None): The filter definition for the field, if applicable. Defaults to None.
        is_sortable (bool): Indicates whether the field is sortable. Defaults to False.
    """
    name: str = Field(description="Field display name")
    filterable: FilterDefinition | None = Field(description="Filter definition", default=None)
    is_sortable: bool = Field(description="Is the field sortable", default=False)


class ListOptions(BaseModel):
    """
    ListOptions is a data model that represents a collection of list option fields.

    Attributes:
        fields (dict[str, ListOptionField]): A dictionary where the keys are strings
            representing field names, and the values are instances of ListOptionField.
            Defaults to an empty dictionary.
    """
    fields: dict[str, ListOptionField] = Field(default_factory=dict)
