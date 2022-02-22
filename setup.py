import sys
import setuptools
from os import path
from setuptools.command.test import test as TestCommand

import immutable

DIR = path.abspath(path.dirname(__file__))


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setuptools.setup(
    name="immutable-config",
    packages=setuptools.find_packages(exclude=("tests",)),
    version=immutable.__version__,
    author=immutable.__author__,
    author_email=immutable.__contact__,
    description=immutable.__description__,
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/dduraipandian/immutable",
    package_dir={'immutable': 'immutable'},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=immutable.__keywords__,
    python_requires='>=3.6',
    tests_require=['tox'],
    cmdclass={'test': Tox},
    zip_safe=False,
    include_package_data=True
)
