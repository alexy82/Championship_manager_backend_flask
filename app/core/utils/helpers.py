import importlib
import json
import os
from sqlalchemy import inspect


def import_class_by_path(class_path: str):
    """
    Import class by path
    :param class_path: module path of class
    :return: Class

    :example:
        import_class_by_path('core.db.DatabaseClass')
    """
    class_path = class_path.split('.')
    class_name = class_path.pop()
    module_path = '.'.join(class_path)
    module = importlib.import_module(module_path)
    class_ = getattr(module, class_name)
    return class_


def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


def read_firebase_cred(fb_server_acc):
    with open('/tmp/gsa.json', 'w') as outfile:
        json.dump(fb_server_acc, outfile)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gsa.json"


def obj_to_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def intersection(lst1, lst2):
    """
    Find the intersection of 2 given lists
    :param lst1:
    :param lst2:
    :return:
    """
    return [item for item in lst1 if item in lst2]