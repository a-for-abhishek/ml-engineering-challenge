from distutils.core import setup

from setuptools import find_packages

setup(
    # Application name:
    name="EGL-ML-CHALLENGE",

    packages=find_packages(),
    
    # Version number (initial):
    version="0.1.0",
    
    # Application author details:
    author="Abi",
    author_email="aforabhishek@hotmail.com",
    
    # Include additional files into the package
    include_package_data=True,
    
    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",
    
    #
    # license="LICENSE.txt",
    description="Useful stuff",
    
    # long_description=open("README.txt").read(),
    
    # Dependent packages (distributions)
    install_requires=[],
)