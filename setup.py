from setuptools import find_packages, setup

setup(
    name="pygear",
    packages=find_packages(exclude=("tests",)),
)