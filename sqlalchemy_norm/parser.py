def parse(items):
    items = set(items)

    digested = [item.split('.') for item in items]
    legacy = dict()

    for item in digested:
        if len(item) > 1:
            prop = item[1:] if len(item) < 2 else '.'.join(item[1:])
            legacy_item = legacy.setdefault(item[0], set())
            legacy_item.add(prop)

    result = {
        'property': set(item[0] for item in digested if len(item) == 1),
        'legacy': legacy
    }

    return result
