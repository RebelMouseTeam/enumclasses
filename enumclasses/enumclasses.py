from enum import Enum, unique

import sys
if sys.version_info >= (3, 10):
    from inspect import get_annotations
else:
    def get_annotations(cls):
        return cls.__annotations__

from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

from enumclasses.utils import deep_replace

T = TypeVar('T')
Enum_T = TypeVar('Enum_T', bound=Enum)


# _cls should never be specified by keyword, so start it with an
# underscore.  The presence of _cls is used to detect if this
# decorator is being called with parameters or not.
def enumclass(_cls: Type[T] = None, *, is_unique=True) -> Type[Enum_T]:

    def decorator(cls):
        return ClassDecorator(is_unique).decorate(cls)

    if _cls is None:
        return decorator
    else:
        return decorator(_cls)


class ClassDecorator:
    def __init__(self, is_unique: bool):
        self.is_unique = is_unique

    def decorate(self, cls: Type[T]) -> Type[Enum_T]:
        names = list(self._stream_names(cls))
        enum_cls = self._make_enum_cls(cls, names)
        enum_cls = self._ensure_unique_if_required(enum_cls)
        enum_cls = self._replace_values(enum_cls, cls, names)
        return enum_cls

    def _stream_names(self, cls: Type[T]) -> Iterator[str]:
        for field, annotation in get_annotations(cls).items():
            if self._is_name_annotation(cls, annotation):
                yield field

    @staticmethod
    def _make_enum_cls(cls: Type[T], names: Iterable[str]):
        return Enum(
            value=cls.__name__,
            names=names,
            module=cls.__module__,
            qualname=cls.__qualname__,
        )

    def _ensure_unique_if_required(self, enum_cls: Type[T]) -> Type[T]:
        if self.is_unique:
            return unique(enum_cls)
        else:
            return enum_cls

    def _replace_values(self, enum_cls: Type[Enum_T], cls: Type[T], names: Iterable[str]):
        old_to_new_value_map: Optional[Mapping[Any, Enum_T]] = None

        for field, annotation in get_annotations(cls).items():
            if not self._is_name_annotation(cls, annotation):
                old_to_new_value_map = old_to_new_value_map or dict(self._stream_old_and_new_values(names, cls, enum_cls))
                value = getattr(cls, field)
                value = deep_replace(value, old_to_new_value_map)
                setattr(enum_cls, field, value)

        return enum_cls

    @staticmethod
    def _stream_old_and_new_values(names: Iterable[str], cls: Type[T], enum_cls: Type[Enum_T]) -> Iterator[Tuple[Any, Enum_T]]:
        for name in names:
            old_value = getattr(cls, name)
            new_value = getattr(enum_cls, name)
            yield old_value, new_value

    @staticmethod
    def _is_name_annotation(cls: Type[T], annotation: str) -> bool:
        return cls.__qualname__ == annotation
