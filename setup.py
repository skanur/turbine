from setuptools import setup
from setuptools.command.test import test
from sys import exit
from io import open
from os import path

import Turbine

here = path.abspath(path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read("README.md")

class PyTest(test):
    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)
        self.test_suite = True
        self.test_args = []

    def finalize_options(self):
        test.finalize_options(self)

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        exit(errcode)

required = [
    'networkx >= 1.11',
    'swiglpk >= 1.4',
    'numpy'
]

extras = {
    'solvers': ['gurobipy'],
    'test': ['pytest']
}

setup(
    name='turbine',
    version=Turbine.__version__,
    license='GPL-2.0',
    install_requires=required,
    author_email='youen.lesparre@lip6.fr',
    packages=[
        'Turbine',
        'Turbine.algorithms',
        'Turbine.calc',
        'Turbine.draw',
        'Turbine.examples',
        'Turbine.file_parser',
        'Turbine.generation',
        'Turbine.graph_classe',
        'Turbine.param'
    ],
    include_package_data=True,
    platforms='any',
    extras_require=extras
)