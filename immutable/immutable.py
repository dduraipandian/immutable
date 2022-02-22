import copy
from types import MappingProxyType
from collections import namedtuple

immutable_mapping = {
    list: tuple,
    set: frozenset,
    dict: MappingProxyType
}

mutable_traverse = {
    list: lambda value: immute_list(value),
    dict: lambda value: immute_dict(value)
}


def immute_list(lst):
    """Traverse all list values and immutes them

    :param lst: List data structure
    :return: immuted list
    """
    for idx, value in enumerate(lst):
        if type(value) in mutable_traverse:
            mutable_traverse_function = mutable_traverse[type(value)]
            value = mutable_traverse_function(value)
        lst[idx] = immute(value)
    return lst


def immute_dict(dct):
    """Traverse all dictionary values and immutes them

    :param dct: Dictionary data structure
    :return: immuted dict
    """
    for key, value in dct.items():
        if type(value) in mutable_traverse:
            mutable_traverse_function = mutable_traverse[type(value)]
            value = mutable_traverse_function(value)
        dct[key] = immute(value)
    return dct


def is_upper(val):
    """Checks all upper case in the string"""
    return True if val.upper() == val else False


def immute(val):
    """Immutes the given value recursively using given immutable_mapping

    :param val: Any python data structure
    :return: immutated value
    """
    data_structure = type(val)
    if type(val) in immutable_mapping:
        immutable_function = immutable_mapping[data_structure]
        val = immutable_function(val)
    return val


def immutable(name, dct, properties=None, only_const=False, recursive=False, clone=True):
    """creates namedtuple from dict to make dct immutable. To make set and dict immutable,
    frozenset and MappingProxyType used respectively.

    :param name: name of the namedtuple
    :param dct: Dict to convert to immutable
    :param clone: source data will not be mutated as a side effect of mutation. If this is set to False,
                  source data will be updated with frozenset, MappingProxy and Tuple for set, dict and list
                  respectively.
    :param properties: properties in namedtuple
    :param recursive: recursive applies immutable mapping function in list and dict.
    :param only_const: If this is true, only upper-cased keys are added to the immutable namedtuple.
                       It will be helpful for global configuration.
    :return: namedtuple
    """
    if clone:
        dct = copy.deepcopy(dct)
    for k, val in dct.items():
        if recursive and type(val) in mutable_traverse:
            mutable_traverse_function = mutable_traverse[type(val)]
            val = mutable_traverse_function(val)
        dct[k] = immute(val)

    if properties is None:
        properties = [k for k in dct if (not only_const) or only_const and is_upper(k)]

    immutable_namedtuple = namedtuple(name, " ".join(properties))
    immutable_dct = immutable_namedtuple(**{k: v for k, v in dct.items() if k in properties})
    return immutable_dct
