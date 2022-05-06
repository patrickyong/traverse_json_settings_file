import getopt
import sys

from pyjson5 import pyjson5

def create_secret(project_id, secret_id):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    project_detail = f"projects/{project_id}"
    response = client.create_secret(
        request={
            "parent": project_detail,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )
    return response

def create_secret_version(project_id, secret_id, data):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    parent = client.secret_path(project_id, secret_id)
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": data.encode("UTF-8")}}
    )
    return response

def get_secret_data(project_id, secret_id, version_id):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    secret_detail = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": secret_detail})
    data = response.payload.data.decode("UTF-8")
    print("Data: {}".format(data))
    return response

def secret(request):
    project_id=''
    secret_id='secret1'
    data='This is the data stored in this secret'
    version_id=1
    create_secret(project_id,secret_id)
    create_secret_version(project_id,secret_id,data)
    get_secret_data(project_id,secret_id,version_id)

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
        detail = ''
        if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
            path.append(k)
            detail = "{}={}".format("\\".join(path), v)
            print(detail)
            path.pop()
        elif v is None:
            path.append(k)
            # do something special
            path.pop()
        elif isinstance(v, list):
            path.append(k)
            if is_list_of_strings(v):
                elements = []
                for elem in v:
                    elements.append(elem)
                detail = "{}={}".format("\\".join(path), "{}".format(",".join(elements)))
                print(detail)
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




