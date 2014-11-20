#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 ko-zu <causeless@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#


import os,sys,re
from publicsuffixlist import PublicSuffixList as PSL

__all__ = ["PublicSuffixList"]

class PublicSuffixList(PSL):

    def get_public_suffix(self, domain):
        return self.suffix(domain) or ""


class UnsafePublicSuffixList(PSL):

    def get_public_suffix(self, domain):
        return self.suffix(domain) or self.publicsuffix(domain) or ""

