from datetime import datetime
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy import inspect

from .parser import parse


class Normalizable:
    def field_normalize(self, x, legacy=None):
        if isinstance(x, datetime):
            return x.isoformat()
        if isinstance(x, InstrumentedList):
            if legacy is not None:
                return [item.vars(**legacy) for item in x
                    if isinstance(item, Normalizable)]
            else:
                return [item.vars() for item in x
                    if isinstance(item, Normalizable)]
        if isinstance(x, Normalizable):
            if legacy is not None:
                return x.vars(**legacy)
            else:
                return x.vars()
        else:
            return x

    def vars(self, includes=[], excludes=[], includes_only=None):

        original_keys = { c.key for c in inspect(self).mapper.column_attrs }
        keys = set(original_keys)

        legacy = {
            'includes': [],
            'excludes': [],
            'includes_only': []
        }

        if len(includes) > 0:
            parsed = parse(includes)
            if 'legacy' in parsed:
                legacy['includes'] = parsed['legacy']
                includes = parsed['property']
        if len(excludes) > 0:
            parsed = parse(excludes)
            if 'legacy' in parsed:
                legacy['excludes'] = parsed['legacy']
                excludes = parsed['property']
        if includes_only is not None and len(includes_only) > 0:
            parsed = parse(includes_only)
            if 'legacy' in parsed:
                legacy['includes_only'] = parsed['legacy']
                includes_only = parsed['property']

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

        fields = { key: self.field_normalize(getattr(self, key), {
                        'includes': legacy['includes'][key]
                                    if key in legacy['includes']
                                    else [],
                        'excludes': legacy['excludes'][key]
                                    if key in legacy['excludes']
                                    else [],
                        'includes_only': legacy['includes_only'][key]
                                    if key in legacy['includes_only']
                                    else None
                }) for key in keys }

        return fields
