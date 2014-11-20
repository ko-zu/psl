#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="publicsuffixlist",
      version="0.1.0",
      packages=["publicsuffixlist",],
      package_data = {
          "publicsuffixlist": [
              "effective_tld_names.dat",
              "test_psl.txt",
          ]},
      author="ko-zu",
      author_email="causeless@gmail.com",
      description="publicsuffixlist implement",
      url="https://github.com/ko-zu/psl",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
          "Topic :: Internet :: Name Service (DNS)",
        ],
      )


