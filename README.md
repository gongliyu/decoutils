*decoutils*: Utilities for writing decorators

[![Build Status](https://travis-ci.com/gongliyu/decoutils.svg?branch=master)](https://travis-ci.com/gongliyu/decoutils)
[![Documentation Status](https://readthedocs.org/projects/decoutils/badge/?version=latest)](https://decoutils.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/gongliyu/decoutils/badge.svg)](https://coveralls.io/github/gongliyu/decoutils)

## Rationale

Python *decorator*s are very useful. However, writing decorators with
arguments is not straightforward. Take the following function as an
example:

``` python
register_plugin(plugin, arg1=1):
    print('registering ', plugin.__name__, ' with arg1=', arg1)
```
This function registers a input function somewhere in the system. If this function could work as a decorator, that will be convinient. In order to make it a decorator, we just need it to return the input plugin trivially:
``` python
register_plugin(plugin, arg1=1):
    print('registering ', plugin.__name__, ' with arg1=', arg1)
    return plugin
    
@register_plugin
def plugin1(): pass
```
It is pretty easy so far. What if we want *register_plugin* works as a decorator with arguments? That's to say, we want to use it as:

``` python
@register_plugin(arg1=2)
def plugin2(): pass
```

In order to accomplish this goal, we need to wrap the function
*register_plugin* so that it return a decorated plugin if the first
input is a callable object, otherwise return a decorator with
arguments. The *decoutils.decorator_with_args* is intend to abstract that wrapping, so that we can reuse it.


## Installation

### Install from PyPI

``` shell
pip install decoutils
```

### Install from Anaconda

``` shell
conda install -c liyugong decoutils
```

## Simple example
Basically, *decorator_with_args* enables a ordinary decorator function to be a decorator with arguments.
``` python
@decorator_with_args
def register_plugin(plugin, arg1=1):
    print('registering ', plugin.__name__, ' with arg1=', arg1)
    return plugin
    
@register_plugin(arg1=10)
def plugin1(): pass
```

Moreover, *decorator_with_args* itself is also a decorator with arguments: one argument *return_original* which can be used to convert a non-decorator function to be a decorator
``` python
@decorator_with_args
def register_plugin(plugin, arg1=1):
    print('registering ', plugin.__name__, ' with arg1=', arg1)
    # Note here the function does not return the plugin, so it cannot work as a decorator originally
    
@register_plugin(arg1=10)
def plugin1(): pass
```

*decorator_with_args* can also convert a function to decorator whose decorating target is not its first argument, e.g.

``` python
decorator_with_args(target_pos=1)
def register_plugin(arg1, plugin):
    return plugin
    
@register_plugin(100) # plugin2 will be registered with arg1=100
def plugin2(): pass
```

*return_original* control whether the resultant decorator return the original plugin, or the result of function *register_plugin*.


## License

The *decoutils* package is released under the [MIT License](LICENSE)

## Documentation

https://decoutils.readthedocs.io
