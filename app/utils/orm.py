from uuid import UUID
from typing import (
    Type,
    TypeVar,
    Sequence,
    List,
)


ModelType = TypeVar("ModelType")


def get_model_fields(
    model: Type[ModelType],
    fields: Sequence[str] = [],
) List:
    return [getattr(self.model, field) for field in fields]