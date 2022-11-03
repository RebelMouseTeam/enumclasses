from pickle import dumps
from pickle import loads
from typing import Any
from typing import Mapping

from enumclasses import enumclass


class TestEnumclass:
    @enumclass()
    class TYPE:
        VALUE_1: 'TestEnumclass.TYPE' = object()
        VALUE_2: 'TestEnumclass.TYPE' = object()
        VALUE_3: 'TestEnumclass.TYPE' = object()

        STRUCT: Mapping[str, Any] = {
            'all_values': frozenset({VALUE_1, VALUE_2, VALUE_3}),
        }

    def test_it_should_convert_enumclass_to_enum(self):
        assert isinstance(self.TYPE.VALUE_1, self.TYPE)
        assert isinstance(self.TYPE.VALUE_2, self.TYPE)
        assert isinstance(self.TYPE.VALUE_3, self.TYPE)
        assert self.TYPE.STRUCT['all_values'] == frozenset({self.TYPE.VALUE_1, self.TYPE.VALUE_2, self.TYPE.VALUE_3})

        value = loads(dumps(self.TYPE.VALUE_1))
        assert value == self.TYPE.VALUE_1

        struct = loads(dumps(self.TYPE.STRUCT))
        assert struct == self.TYPE.STRUCT
