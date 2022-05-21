from sklearn.externals import joblib
import pandas as pd
import os


def __init(**kwargs):
    """
    :initial
    :param kwargs: 初始化参数 k=v
    :return:
    """
    global _globals_dict
    _globals_dict = kwargs if kwargs else {}
    print( "start movie config" )
    # need to write the local
    currentDir = os.path.dirname(os.path.dirname(__file__))
    dirH5 = os.path.join(currentDir, 'moviePivot.h5')
    modelDir = os.path.join(currentDir, 'model_knn.m')
    h5_store = pd.HDFStore( dirH5, mode='r' )
    _globals_dict['dataset'] = h5_store['moviePivot']
    _globals_dict['knn_model'] = joblib.load( modelDir )
    h5_store.close()
    print( "loaded" )


def set_value(key, value):
    """
    :param key: Key
    :param value: Value
    :return:
    """
    _globals_dict[key] = value


def get_value(key, default=None):
    """
    :param key: Key
    :param default: None
    :return:
    """
    try:
        return _globals_dict[key]
    except KeyError:
        return default


def get_all(default=None):
    """
    :param default: None
    :return:
    """
    try:
        return _globals_dict
    except Exception:
        return default


def pop_value(key, default=None):
    """
    :param key: Key
    :param default: None
    :return:
    """
    try:
        return _globals_dict.pop( key )
    except KeyError:
        return default


def clear():
    _globals_dict.clear()