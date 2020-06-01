#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from setuptools import setup

description = codecs.open('README.md', encoding='utf-8').read()

setup(name="publicsuffixlist",
      version="0.7.2",
      packages=["publicsuffixlist"],
      package_data={
          "publicsuffixlist": [
              "public_suffix_list.dat",
              "test_psl.txt",
          ]},
      author="ko-zu",
      author_email="causeless@gmail.com",
      description="publicsuffixlist implement",
      long_description=description,
      long_description_content_type="text/markdown",
      url="https://github.com/ko-zu/psl",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
          "Topic :: Internet :: Name Service (DNS)",
          "Topic :: Text Processing :: Filters",
          "Operating System :: OS Independent",

        ],
      python_requires=">=2.6",
      extras_require={
          "update": ["requests"],
          "readme": ["pandoc"],
        },
      entry_points={
          "console_scripts": [
              "publicsuffixlist-download = publicsuffixlist.update:updatePSL",
          ]},
      test_suite="publicsuffixlist.test",
      license='MPL-2.0',
      )
