# -*- coding: utf-8 -*-

__version__ = '0.0.4'

import functools
import inspect
import sys

def decorator_with_args(func, return_original=False, target_pos=0):
    """Enable a function to work with a decorator with arguments

    Args:

      func (callable): The input function.

      return_original (bool): Whether the resultant decorator returns
        the decorating target unchanged. If True, will return the
        target unchanged. Otherwise, return the returned value from
        *func*. Default to False. This is useful for converting a
        non-decorator function to a decorator. See examples below.

    Return:

      callable: a decorator with arguments.

    Examples:

    >>> @decorator_with_args
    ... def register_plugin(plugin, arg1=1):
    ...     print('Registering '+plugin.__name__+' with arg1='+str(arg1))
    ...     return plugin  # note register_plugin is an ordinary decorator
    >>> @register_plugin(arg1=10)
    ... def plugin1(): pass
    Registering plugin1 with arg1=10

    >>> @decorator_with_args(return_original=True)
    ... def register_plugin_xx(plugin, arg1=1):
    ...     print('Registering '+plugin.__name__+' with arg1='+str(arg1))
    ...     # Note register_plugin_xxx does not return plugin, so it cannot
    ...     # be used as a decorator directly before applying
    ...     # decorator_with_args. 
    >>> @register_plugin_xx(arg1=10)
    ... def plugin1(): pass
    Registering plugin1 with arg1=10
    >>> plugin1()

    >>> @decorator_with_args(return_original=True)
    ... def register_plugin_xxx(plugin, arg1=1): pass

    >>> # use result decorator as a function
    >>> register_plugin_xxx(plugin=plugin1, arg1=10)
    <function plugin1...>

    >>> @decorator_with_args(return_original=True, target_pos=1)
    ... def register_plugin_xxxx(arg1, plugin, arg2=10):
    ...     print('Registering '+plugin.__name__+' with arg1='+str(arg1))
    >>> @register_plugin_xxxx(100)
    ... def plugin2(): pass
    Registering plugin2 with arg1=100
    """
    if sys.version_info[0] >= 3:
        target_name = inspect.getfullargspec(func).args[target_pos]
    else:
        target_name = inspect.getargspec(func).args[target_pos]
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if  len(args) > target_pos:
            res = func(*args, **kwargs)
            return args[target_pos] if return_original else res
        elif len(args) <= 0 and target_name in kwargs:
            res = func(*args, **kwargs)
            return kwargs[target_name] if return_original else res
        else:
            return wrap_with_args(*args, **kwargs)

    def wrap_with_args(*args, **kwargs):
        def wrapped_with_args(target):
            kwargs2 = dict()
            kwargs2[target_name] = target
            kwargs2.update(kwargs)
            res = func(*args,  **kwargs2)
            return target if return_original else res
        return wrapped_with_args

    return wrapper


# make decorator_with_argument itself a decorator with arguments
decorator_with_args = decorator_with_args(decorator_with_args)
