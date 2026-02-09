# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='osint-storm',
    version="2",
    packages=find_packages(where="."),
    author="megadose (Modified for StormOS)",
    install_requires=[
        "termcolor",
        "bs4",
        "httpx",
        "trio",
        "colorama",
        "tqdm"
    ],
    description="This OSINT is just a separate module from Storm Framework.",
    include_package_data=True,
    url=[
        "http://github.com/megadose/holehe",
        "http://github.com/storm-os/OSINT",
        "http://github.com/storm-os/Cyber-Pentest"
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
)
