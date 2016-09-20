from datetime import datetime
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy import inspect

from .parser import parse


class Normalizable:
    def field_normalize(self, x, legacy=None):
        if isinstance(x, datetime):
            return x.isoformat()
        if isinstance(x, InstrumentedList):
            return [item.vars(**(legacy or {})) for item in x
                    if isinstance(item, Normalizable)]
        if isinstance(x, Normalizable):
            return x.vars(**(legacy or {}))
        else:
            return x

    def vars(self, includes=None, excludes=None, includes_only=None):
        legacy = {
            'includes': {},
            'excludes': {},
            'includes_only': {}
        }

        if includes_only:
            parsed = parse(includes_only)
            if 'legacy' in parsed:
                legacy['includes_only'] = parsed['legacy']
                includes_only = parsed['property']

            keys = set(includes_only)

        elif hasattr(self, "__includes_only__"):
            keys = set(self.__includes_only__)

        else:
            keys = set(c.key for c in inspect(self).mapper.column_attrs).union(
                set(getattr(self, '__includes__', []))
            ) - set(getattr(self, '__excludes__', []))

            if includes:
                parsed = parse(includes)
                if 'legacy' in parsed:
                    legacy['includes'] = parsed['legacy']
                    includes = parsed['property']

                keys = keys.union(set(includes))

            if excludes:
                parsed = parse(excludes)
                if 'legacy' in parsed:
                    legacy['excludes'] = parsed['legacy']
                    excludes = parsed['property']

                keys = keys - set(excludes)

        fields = {
            key: self.field_normalize(getattr(self, key), {
                'includes': legacy['includes'].get(key),
                'excludes': legacy['excludes'].get(key),
                'includes_only': legacy['includes_only'].get(key)
            }) for key in keys
        }

        return fields
