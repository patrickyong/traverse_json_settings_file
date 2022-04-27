import json


# https://stackoverflow.com/questions/18495098/python-check-if-an-object-is-a-list-of-strings

def is_list_of_strings(lst):
    if lst and isinstance(lst, list):
        from requests.compat import basestring
        return all(isinstance(elem, basestring) for elem in lst)
    else:
        return False


# https://stackoverflow.com/questions/12507206/how-to-completely-traverse-a-complex-dictionary-of-unknown-depth

def walk(d):
    global path

    for k, v in d.items():
        if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
            path.append(k)
            print("{}={}".format("\\".join(path), v))
            path.pop()
        elif v is None:
            path.append(k)
            # do something special
            path.pop()
        elif isinstance(v, list):
            path.append(k)
            if is_list_of_strings(v):
                print("{}={}".format("\\".join(path), v))
            else:
                for v_int in v:
                    walk(v_int)
            path.pop()
        elif isinstance(v, dict):
            path.append(k)
            walk(v)
            path.pop()
        else:
            print("###Type {} not recognized: {}.{}={}".format(type(v), ".".join(path), k, v))


if __name__ == '__main__':
    with open('test.json', encoding="utf-8-sig") as f:
        myjson = json.load(f)

    path = []
    walk(myjson)

    #fh = open('test.json', "r", encoding="utf-8-sig")
    #rawText = fh.read()
    #json_data = rawText[rawText.index("\n", 3) + 1:]
    #path = []
    #walk(json_data)
