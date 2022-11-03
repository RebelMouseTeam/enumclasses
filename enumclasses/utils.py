from typing import Any
from typing import Mapping


def deep_replace(source: Any, replacement_map: Mapping) -> Mapping:

    def _replace(obj):
        if isinstance(obj, dict):
            keys = map(_replace, obj.keys())
            values = map(_replace, obj.values())
            return type(obj)(zip(keys, values))
        elif isinstance(obj, (tuple, list, set, frozenset)):
            return type(obj)(map(_replace, obj))
        try:
            return replacement_map[obj]
        except LookupError:
            return obj

    return _replace(source)
