from setuptools import setup, find_packages
import sys


setup(
    name='converge',
    version='1.1.0',
    url='http://pypi.python.org/pypi/converge/',
    classifiers=[
        'Programming Language :: Python :: 3'
        ],
    python_requires='>=3.5',
    include_package_data=True,
    description='Ultra simple settings management for (only) Python apps',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    author='Shekhar Tiwatne',
    author_email='pythonic@gmail.com',
    license="http://www.opensource.org/licenses/mit-license.php",
    )
