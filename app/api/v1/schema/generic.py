"""
The schemas of user are defined in here.
"""

from typing import Generic, List, Optional, TypeVar

from fastapi import Query

# pytype: enable=import-error
from pydantic import Field
from pydantic.generics import GenericModel

# pytype: disable=import-error

T = TypeVar("T")


QueryLimit: int = Query(
    10,
    description="Optional, determine the number of returned rows after skipped offset, if it is 0, return all items.",
    examples=[10],
)

QueryOffset: int = Query(0, description="Optional, determine the number of rows need be skipped.", examples=0)


class ListResponse(GenericModel, Generic[T]):
    """ListResponse schema"""

    total: Optional[int] = Field(None, title="total", description="The total count of entries.", examples=[0])
    data: List[T] = Field(..., title="data", description="The entry list.")
