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
        else:
            return x

    def vars(self, includes=[], excludes=[], includes_only=None):

        if hasattr(self, "__includes__"):
            includes = includes + self.__includes__

        if hasattr(self, "__includes_only__"):
            if includes_only is None:
                includes_only = []
            includes_only = includes_only + self.__includes_only__

        if hasattr(self, "__excludes__"):
            excludes = excludes + self.__excludes__

        includes = set(includes)

        if includes_only is not None:
            includes_only = set(includes_only)
            includes = includes.union(includes_only)

        excludes = set(excludes) - includes

        keys = {c.key for c in inspect(self).mapper.column_attrs}
        keys = keys.union(includes) - excludes

        if includes_only is not None:
            keys = keys.intersection(includes_only)

        fields = { key: self.field_normalize(getattr(self, key))
                   for key in keys }

        return fields
