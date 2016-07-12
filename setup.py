from setuptools import setup

setup(name='chainsmoke',
      version='0.1',
      description='A collection of tools for chains of functions. Strives to be simple, practical and well-documented.',
      url='https://github.com/bielenah/chainsmoke',
      author='Alex Bielen',
      author_email='alexhendriebielen@gmail.com',
      license='MIT',
      packages=['chainsmoke'],
      install_requires=[
            'pytest',
      ],
      zip_safe=False
      )

