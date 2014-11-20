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
      classfiers=[
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        ],
      )


