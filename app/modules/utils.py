def check_all(source: str, items: list):
    for i in items:
        if source == i:
            return True
    return False

def enum_dict(keys: list, target: dict, offset: int = 0):
    if len(keys) <= offset or keys[offset] == '':
        return None, "No property specified"
    for i in target:
        if i == keys[offset]:
            if type(target[keys[offset]]) != dict:
                return target, offset
            if len(keys) <= offset + 1 or keys[offset + 1] == '':
                return None, f"No subproperty specified for category: {keys[offset]}"
            return enum_dict(keys, target[keys[offset]], offset + 1)
    return None, f"Property not found: {keys[offset]}"