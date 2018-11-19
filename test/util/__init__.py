# coding: utf-8

from __future__ import unicode_literals, absolute_import

from operator import attrgetter
import os
import os.path
from contextlib import contextmanager
import shutil

from modulegraph.find_modules import find_modules
from six.moves import filter, map, zip

import boxsdk


boxsdk_dirname, boxsdk_basename = os.path.split(boxsdk.__file__)
assert boxsdk_basename in ['__init__.py', '__init__.pyc']
assert os.path.abspath(boxsdk_dirname) == boxsdk_dirname
boxsdk_parent_dirname = os.path.dirname(boxsdk_dirname)


module1 = module1_name, module1_path = 'boxsdk.foobar', os.path.join(boxsdk_dirname, 'foobar.py')
subpackage = subpackage_name, subpackage_path = 'boxsdk.foobarbaz', os.path.join(boxsdk_dirname, 'foobarbaz')
subpackage_init_path = os.path.join(subpackage_path, '__init__.py')
module2 = module2_name, module2_path = 'boxsdk.foobarbaz.foobarbaz', os.path.join(subpackage_path, 'foobarbaz.py')


@contextmanager
def mock_modules_in_package():
    try:
        with open(module1_path, 'w'):
            pass
        os.mkdir(subpackage_path)
        with open(subpackage_init_path, 'w'), open(module2_path, 'w'):
            pass
        yield module1, subpackage, module2
    finally:
        os.remove(module1_path)
        shutil.rmtree(subpackage_path)


def is_boxsdk_node(node):
    return node.graphident[:6] == 'boxsdk'


def getReferers(module_graph, *args, **kwargs):
    return list(filter(None, module_graph.getReferers(*args, **kwargs)))


with mock_modules_in_package() as f:
    print(f)
    module_graph = find_modules(packages=['boxsdk'])
    boxsdk_nodes = list(module_graph.flatten(condition=is_boxsdk_node))
    boxsdk_names = list(map(attrgetter('graphident'), boxsdk_nodes))
    for name in list(zip(*f))[0]:
        assert name in module_graph, "{} not in {}".format(name, module_graph)
        assert name in boxsdk_names, "{} not in known boxsdk submodules".format(name)
    for name in [module1_name, module2_name]:
        referers = getReferers(module_graph, name)
        assert not referers, "Referers of {} are {}".format(name, referers)
    referers = getReferers(module_graph, subpackage_name)
    assert list(map(attrgetter('graphident'), referers)) == [module2_name]
    print(module_graph)
    pass


# list(filter(lambda name: (list(mg.getReferers(name)) == [None]), sorted(list(filter(lambda k: (isinstance(k, str) and 'boxsdk' in k), mg.graph.nodes.keys())))))
