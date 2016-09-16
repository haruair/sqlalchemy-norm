from datetime import datetime
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy import inspect


class Normalizable:
    def field_normalize(self, x):
        if isinstance(x, datetime):
            return x.isoformat()
        if isinstance(x, InstrumentedList):
            return [item.vars() for item in x
                if isinstance(item, Normalizable)]
        if isinstance(x, Normalizable):
            return x.vars()
        else:
            return x

    def vars(self, includes=[], excludes=[], includes_only=None):

        original_keys = { c.key for c in inspect(self).mapper.column_attrs }
        keys = set(original_keys)

        if hasattr(self, "__includes__"):
            keys = keys.union(set(self.__includes__))

        if hasattr(self, "__excludes__"):
            keys = keys - set(self.__excludes__)

        keys = keys.union(set(includes))

        if len(excludes) > 0:
            keys = keys - set(excludes)

        if includes_only is not None:
            keys = set(includes_only)

        elif hasattr(self, "__includes_only__"):
            keys = set(self.__includes_only__)

        fields = { key: self.field_normalize(getattr(self, key))
                   for key in keys }

        return fields
