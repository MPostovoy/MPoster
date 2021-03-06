import os

import setuptools


with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mposter",
    version="1.6.5",
    author="M.Postovoy",
    author_email="mihan.45rus@ya.ru",
    description="Additional tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MPostovoy/MPoster",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=['requests', 'confluent_kafka', 'zeep', 'loguru'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
# https://proglib.io/p/kak-opublikovat-svoyu-python-biblioteku-na-pypi-2020-01-28
