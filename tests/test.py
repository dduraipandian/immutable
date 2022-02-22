import unittest
import copy
from types import MappingProxyType

from immutable.immutable import immutable, immute_dict, immute_list


class TestImmutedData(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
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
            'filters': {
                'special': {
                    '()': 'project.logging.SpecialFilter',
                    'foo': 'bar',
                },
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                },
                'mail_admins': {
                    'level': 'ERROR',
                    'class': 'django.utils.log.AdminEmailHandler',
                    'filters': ['special']
                }
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

    def test_immuted_dict_mapping_proxy(self):
        """Tests dict type is converted to MappingProxyType"""

        config = immutable('LoggingConfig', self.LOGGING, only_const=False, recursive=True)
        result = config.loggers['myproject.custom']
        self.assertIsInstance(result, MappingProxyType)

    def test_immuted_list_tuple(self):
        """Tests list type is converted to tuple"""

        config = immutable('LoggingConfig', self.LOGGING, only_const=False, recursive=True)
        result = config.handlers['console']['filters']
        self.assertIsInstance(result, tuple)

    def test_immuted_set_fset(self):
        """Tests set type is converted to frozenset"""

        config = immutable('LoggingConfig', self.LOGGING, only_const=False, recursive=True)
        handlers = config.loggers['myproject.custom']['handlers']
        self.assertIsInstance(handlers, frozenset)

    def test_immuted_list(self):
        """Tests index is accessible or not"""

        expected = ('require_debug_true',)
        config = immutable('LoggingConfig', self.LOGGING, only_const=False, recursive=True)
        result = config.handlers['console']['filters']
        self.assertEqual(result, expected)

    def test_immuted_list_1(self):
        """Tests list order is preserved or not"""

        expected = ('require_debug_true',)
        config = immutable('LoggingConfig', self.LOGGING, only_const=False, recursive=True)
        result = config.handlers['console']['filters']
        self.assertEqual(result[0], expected[0])

    def test_immuted_dict_modify(self):
        """Test dict can be modified after mutation"""

        config = immutable('LoggingConfig', self.LOGGING, only_const=False, recursive=True)
        result = config.handlers['console']
        with self.assertRaises(TypeError):
            result['level'] = 'DEBUG'

    def test_immuted_set_modify(self):
        """Test set can be modified after mutation"""

        config = immutable('LoggingConfig', self.LOGGING, only_const=False, recursive=True)
        handlers = config.loggers['myproject.custom']['handlers']
        with self.assertRaises(AttributeError):
            handlers.add("DUMMY")

    def test_immuted_list_check(self):
        """Test list mutation"""

        data = ['console', {'mail_admins'}]
        result = immute_list(data)
        self.assertEqual(data, result)

    def test_immuted_dict_check(self):
        """Test dict mutation"""
        data = {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['special']
            }
        }
        result = immute_dict(data)
        admins = result['mail_admins']
        self.assertIsInstance(admins, MappingProxyType)

    def test_immuted_dict_check_1(self):
        """Test dict can be modified after mutation"""

        data = {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['special']
            }
        }
        result = immute_dict(data)
        with self.assertRaises(TypeError):
            result['mail_admins']['level'] = 'DEBUG'

    def test_immuted_data_clone_true(self):
        """Tests source data should not be modified with clone=True option"""

        logging = copy.deepcopy(self.LOGGING)
        immutable('LoggingConfig', logging, only_const=False, recursive=True)
        self.assertTrue(logging == self.LOGGING)

    def test_immuted_data_clone_false(self):
        """Tests source data should be modified with clone=False option"""

        logging = copy.deepcopy(self.LOGGING)
        immutable('LoggingConfig', logging, only_const=False, recursive=True, clone=False)
        self.assertFalse(logging == self.LOGGING)
