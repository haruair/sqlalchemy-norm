def parse(items):
    items = set(items)

    digested = [item.split('.') for item in items]
    properties = [item[0] for item in digested if len(item) == 1]

    legacy = dict()

    for item in digested:
        if len(item) > 1:
            if item[0] not in legacy:
                legacy[item[0]] = set()
            prop = item[1:] if len(item) < 2 else '.'.join(item[1:])
            legacy[item[0]].add(prop)

    result = {
        'property': set(properties)
    }

    if len(legacy) > 0:
        result['legacy'] = legacy

    return result
