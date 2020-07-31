#!/usr/bin/evn python
#coding=utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tora",
    version="0.0.1",
    author="Orlando Chen",
    author_email="seagochen@hotmail.com",
    description="A similar utility to Makefile, but easier to C/C project management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seagochen/Tora",
    packages=setuptools.find_packages(),
    install_requires=['siki', 'pandas', 'untangle', 'pkgconfig', 'wget'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)