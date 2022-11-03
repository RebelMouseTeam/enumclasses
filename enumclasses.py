from enum import Enum, unique
from functools import partial
from typing import TypeVar, Type, List, Any, Mapping

from rebelmouse.tools import filter_dict, dict_from_list, deep_replace

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
        name_list = self._make_name_list(cls)
        enum_cls = self._make_enum_cls(cls, name_list)
        enum_cls = self._ensure_unique_if_required(enum_cls)
        enum_cls = self._replace_values(enum_cls, cls, name_list)
        return enum_cls

    def _make_name_list(self, cls):
        name_to_annotation_map = filter_dict(cls.__annotations__, partial(self._is_name_annotation, cls))
        return list(name_to_annotation_map.keys())

    @staticmethod
    def _make_enum_cls(cls, name_list):
        return Enum(
            value=cls.__name__,
            names=name_list,
            module=cls.__module__,
            qualname=cls.__qualname__,
        )

    def _ensure_unique_if_required(self, enum_cls: Type[T]) -> Type[T]:
        if self.is_unique:
            return unique(enum_cls)
        else:
            return enum_cls

    def _replace_values(self, enum_cls: Type[Enum_T], cls: Type[T], name_list: List[str]):
        old_to_new_value_map = self._make_old_to_new_value_map(name_list, cls, enum_cls)
        for field, annotation in cls.__annotations__.items():
            if not self._is_name_annotation(cls, annotation):
                value = getattr(cls, field)
                value = deep_replace(value, old_to_new_value_map)
                setattr(enum_cls, field, value)

        return enum_cls

    @staticmethod
    def _make_old_to_new_value_map(name_list: List[str], cls: Type[T], enum_cls: Type[Enum_T]) -> Mapping[Any, Enum_T]:
        return dict_from_list(name_list, key_func=partial(getattr, cls), value_func=partial(getattr, enum_cls))

    @staticmethod
    def _is_name_annotation(cls: Type[T], annotation: str) -> bool:
        return cls.__qualname__ == annotation
