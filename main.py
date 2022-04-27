import getopt
import sys

from pyjson5 import pyjson5


# https://stackoverflow.com/questions/18495098/python-check-if-an-object-is-a-list-of-strings

def is_list_of_strings(lst):
    if lst and isinstance(lst, list):
        from requests.compat import basestring
        return all(isinstance(elem, basestring) for elem in lst)
    else:
        return False


# https://stackoverflow.com/questions/12507206/how-to-completely-traverse-a-complex-dictionary-of-unknown-depth



def walk(d, pf):
    global path

    if len(pf) > 0:
        path.append(pf)
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

                    walk(v_int, '')
            path.pop()
        elif isinstance(v, dict):
            path.append(k)
            walk(v, prefix)
            path.pop()
        else:
            print("###Type {} not recognized: {}.{}={}".format(type(v), ".".join(path), k, v))


if __name__ == '__main__':
    project_id = ''
    setting_file = 'test.json'
    prefix = 'Local'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:s:p:", ["projectid=", "settingFile=", "prefix="])

        for opt, arg in opts:
            if opt == '-h':
                print('test.py -p <project_id> -s <setting_file>')
                sys.exit()
            elif opt in ("-p", "--projectid"):
                project_id = arg
            elif opt in ("-s", "--settingfile"):
                setting_file = arg
            elif opt in ("-p", "--prefix"):
                prefix = arg

        with open(setting_file, encoding="utf-8-sig") as f:
            j = pyjson5.load(f)
        path = []
        walk(j, prefix)

    except getopt.GetoptError:
        print('test.py -p <project_id> -s <setting_file>')
        sys.exit(2)




