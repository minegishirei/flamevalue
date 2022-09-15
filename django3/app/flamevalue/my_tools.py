import json

def del_dub_dict_list(dict_list):
    return list(map(json.loads, set(map(json.dumps, dict_list))))