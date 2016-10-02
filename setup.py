from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='chainsmoke',
      version='0.0.1',
      description='A collection of tools for chains of functions. Strives to be simple, practical and well-documented.',
      url='https://github.com/alexbielen/chainsmoke',
      author='Alex Bielen',
      author_email='alexhendriebielen@gmail.com',
      license='MIT',
      packages=['chainsmoke'],
      install_requires=[
          'pytest',
      ],
      cmdclass={'test': PyTest}
      )
