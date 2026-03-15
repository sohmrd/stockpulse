from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard envelope returned by every endpoint."""

    data: T | None = None
    error: str | None = None
    meta: dict[str, Any] | None = None
