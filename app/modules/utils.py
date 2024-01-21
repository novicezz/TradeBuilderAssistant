def check_all(source: str, items: list):
    for i in items:
        if source == i:
            return True
    return False

def gen_map(target: dict, level: int = 0, last: bool = False) -> str:
    mapStr = ""
    if level != 0:
        if last: nestLevel = " "
        else: nestLevel = "│"
        for i in range(0, level): nestLevel += "   "
        nestLevel += "└──"

    count = 0
    for i in target:
        count += 1
        if level == 0:
            if count == len(target): nestLevel = "└──"
            else: nestLevel = "├──"

        if type(target[i]) == dict:
            mapStr += f"{nestLevel}{i}\n"
            mapStr += gen_map(target[i], level + 1, count == len(target) if level == 0 else last)
        else:
            mapStr += f"{nestLevel}{i}: {target[i].get_element()}\n"
    return mapStr

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

def fill_table(target: dict) -> dict:
    setupTable = {}
    for key in target:
        if type(target[key]) == dict:
            setupTable[key] = fill_table(target[key])
        else:
            setupTable[key] = target[key].get_element()
    return setupTable

def check_if_full(target: dict) -> bool:
    for val in list(target.values()):
        if type(val) == dict:
            subDict = check_if_full(val)
            if subDict == False:
                return False
        else:
            if val == None: return False
    return True