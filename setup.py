# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='osint-storm', # Beri nama unik agar tidak bentrok dengan holehe asli
    version="1.61",
    packages=find_packages(),
    author="megadose (Modified for StormOS)",
    install_requires=[
        "termcolor",
        "bs4",
        "httpx",
        "trio",
        "colorama"
        # "tqdm" bisa dihapus jika StormOS punya progress bar sendiri
    ],
    description="OSINT module for StormOS Framework",
    include_package_data=True,
    # HAPUS entry_points agar tidak membuat file 'holehe' di /usr/bin/
    # Dengan begini, dia tidak bisa dijalankan mandiri, hanya bisa dipanggil StormOS
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
