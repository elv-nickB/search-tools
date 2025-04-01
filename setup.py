from setuptools import setup, find_packages

setup(
    name='search_utils',
    version='0.1',
    install_requires=['loguru',
                      'tqdm'],
    packages=find_packages(),
)