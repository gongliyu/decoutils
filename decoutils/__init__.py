# -*- coding: utf-8 -*-

__version__ = '0.0.1'

import functools

def decorator_with_args(func, return_original=False):
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
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 0 and callable(args[0]):
            res = func(*args, **kwargs)
            return args[0] if return_original else res
        else:
            return wrap_with_args(*args, **kwargs)

    def wrap_with_args(*args, **kwargs):
        def wrapped_with_args(target):
            res = func(target, *args, **kwargs)
            return target if return_original else res
        return wrapped_with_args

    return wrapper


# make decorator_with_argument itself a decorator with arguments
decorator_with_args = decorator_with_args(decorator_with_args)
