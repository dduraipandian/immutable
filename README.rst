===========
Readme File
===========

.. image:: https://app.travis-ci.com/dduraipandian/immutable.svg?token=HYyTsSU9ynxiqecjxoc5&branch=main
    :target: https://travis-ci.com/dduraipandian/immutable
    :alt: Travis CI

.. image:: https://codecov.io/gh/dduraipandian/immutable/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/dduraipandian/immutable
  :alt: codecov test coverage

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
  :target: https://opensource.org/licenses/MIT
  :alt: MIT License



Immutable
----------
.. inclusion-marker-do-not-remove-start

Immutable library helps to convert python dictionary to namedtuples and converting values to immutable datastructure
recursively. Namedtuples, by default, are immutable.
You can't modify them. But If you have nested data structures, you can still modify them.

Immutable library tries to provides a function to convert them immutable and creates namedtuple from the converted dict.

Dict    -> MappingProxyType

List    -> Tuple

Set     -> Frozenset

UseCase
=======
When "global variables as configuration" should be shared across the project, library will help to make
config immutable.

.. inclusion-marker-do-not-remove-end


.. topic:: **How to install**

    .. code-block:: html

        pip install immutable

.. topic:: **Requirements**

    Python 3.6 and above


Code Example
============

.. code-block:: python

    from immutable.immutable import immutable

    LOGGING = {
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'myproject.custom': {
                'handlers': {'console', 'mail_admins'},
                'level': 'INFO',
                'filters': ['special']
            }
        }
    }

    config = immutable('LoggingConfig', LOGGING, only_const=False, recursive=True)


Options
=======
only_const (default = False)
----------
It will create namedtuple from all dictionary keys. When it is set to :code:`True`,
it will only create namedtuple from :code:`constants` (all caps variables).

recursive (default = False)
---------
Only first level of key-vales are immuted, when it is set to :code:`False`. When it is set to :code:`True`,
all the key-values are traversed and converted to immutable.

clone (default = True)
-----
Clone the given dictionary and mutates it. deepcopy is a costly operation when dictionary is to
many levels of nested with basic python data structure (list, tuple, set, dict).

Setting it to :code:`False` will improve the performance, but it will mutate the data given to immutable function.
So use :code:`False`, when you do not need to access the data after making it immutable.

properties
----------
Immutable function takes all the key from data given and creates namedtuple from that. If you want to create namedtuple
with selected keys, you can pass properties :code:`iterable` to filter from data.

License
=======

This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details