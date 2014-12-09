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
from publicsuffixlist import PSLURL, PSLFILE, PublicSuffixList

def updatePSL():
    try:
        import requests
    except ImportError:
        raise Exception("Please install python-requests http(s) library. $ sudo pip install requests")

    from email.utils import parsedate
    import time

    r = requests.get(PSLURL)
    if r.status_code != requests.codes.ok or len(r.content) == 0:
        raise Exception("Could not download PSL from " + PSLURL)

    lastmod = r.headers.get("last-modified", None)

    f = open(PSLFILE + ".swp", "wb")
    f.write(r.content)
    f.close()

    f = open(PSLFILE + ".swp", "rb")
    psl = PublicSuffixList(f)
    f.close()

    os.rename(PSLFILE + ".swp", PSLFILE)
    
    if lastmod:
        t = time.mktime(parsedate(lastmod))
        os.utime(PSLFILE, (t, t))

    print("PSL updated")
    if lastmod:
        print("last-modified: " + lastmod)

if __name__ == "__main__":
    updatePSL()

