#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 ko-zu <causeless@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os,sys

__all__ = ["PublicSuffixList"]

ENCODING = "utf-8"

PSLURL = "https://publicsuffix.org/list/public_suffix_list.dat"

PSLFILE = os.path.join(os.path.dirname(__file__), "public_suffix_list.dat")

if sys.version_info >= (3, ):
    # python3.x
    def u(s):
        return s if isinstance(s, str)     else s.decode(ENCODING)
    def b(s):
        return s if isinstance(s, bytes)   else s.encode(ENCODING)
    basestr = str
    decodablestr = (str, bytes)

else:
    # python 2.x
    def u(s):
        return s if isinstance(s, unicode) else s.decode(ENCODING)
    def b(s):
        return s if isinstance(s, str)     else s.encode(ENCODING)
    basestr = basestring
    decodablestr = basestring


def encode_idn(domain):
    return u(domain).encode("idna").decode("ascii")


def decode_idn(domain):
    return b(domain).decode("idna")




class PublicSuffixList(object):

    def __init__(self, source=None, accept_unknown=True, accept_encoded_idn=True):

        self.accept_unknown = accept_unknown

        if source == None:
            try:
                source = open(PSLFILE, "rb")
                self._parse(source, accept_encoded_idn)
            finally:
                if source:
                    source.close()
        else:    
            self._parse(source, accept_encoded_idn)



    def _parse(self, source, accept_encoded_idn):
        
        publicsuffix = set()
        maxlabel = 0

        if isinstance(source, decodablestr):
            source = source.splitlines()

        ln = 0
        for line in source:
            ln += 1
            s = u(line).lower().split(" ")[0].rstrip()
            if s == "" or s.startswith("//"):
                continue

            maxlabel = max(maxlabel, s.count(".") + 1)
            publicsuffix.add(s)
            if accept_encoded_idn:
                e = encode_idn(s.lstrip("!"))
                if s[0] == "!":
                    publicsuffix.add("!" + e)
                else:
                    publicsuffix.add(e)

        self._publicsuffix = frozenset(publicsuffix)
        self._maxlabel = maxlabel


    def suffix(self, domain, accept_unknown=None):
        """ alias for privatesuffix """
        return self.privatesuffix(domain, accept_unknown)


    def privatesuffix(self, domain, accept_unknown=None):
        """ return shortest suffix assigned for an individual """

        if accept_unknown == None:
            accept_unknown = self.accept_unknown

        if not isinstance(domain, basestr):
            raise TypeError()

        labels = domain.lower().rsplit(".", self._maxlabel + 2)
        ll = len(labels)

        if "\0" in domain or "" in labels:
            # not a valid domain
            return None
        
        if ll < 2:
            # is TLD
            return None

        # skip longer match
        for i in range(max(0, ll - self._maxlabel), ll):
            s = ".".join(labels[i:])

            if i > 0 and ("!*." + s) in self._publicsuffix:
                return ".".join(labels[i-1:])

            if ("!" + s) in self._publicsuffix:
                # exact match
                return s

            if i > 0 and ("*." + s) in self._publicsuffix:
                if i <= 1:
                    # domain is publicsuffix
                    return None
                else:
                    return ".".join(labels[i-2:])

            if s in self._publicsuffix:
                if i > 0:
                    return ".".join(labels[i-1:])
                else:
                    # domain is publicsuffix
                    return None

        else:
            # no match found
            if self.accept_unknown and ll >= 2:
                return ".".join(labels[-2:])
            else:
                return None



    def publicsuffix(self, domain, accept_unknown=None):
        """ return longest public suffix """

        if accept_unknown == None:
            accept_unknown = self.accept_unknown

        if not isinstance(domain, basestr):
            raise TypeError()

        labels = domain.lower().rsplit(".", self._maxlabel + 2)
        ll = len(labels)

        if "\0" in domain or "" in labels:
            # not a valid domain
            return None

        # shortcut for tld
        if ll == 1:
            if accept_unknown:
                return domain
            else:
                return None

        # skip longer match
        for i in range(max(0, ll - self._maxlabel), ll):
            s = ".".join(labels[i:])

            if i > 0 and ("!*." + s) in self._publicsuffix:
                return s
    
            if ("!" + s) in self._publicsuffix:
                # exact exclude
                if i + 1 < ll:
                    return ".".join(labels[i+1:])
                else:
                    return None
            
            if i > 0 and ("*." + s) in self._publicsuffix:
                return ".".join(labels[i-1:])

            if s in self._publicsuffix:
                return s

        else:
            # no match found
            if accept_unknown:
                return labels[-1]
            else:
                return None


    def is_private(self, domain):
        return self.suffix(domain) != None


    def is_public(self, domain):
        return self.publicsuffix(domain) == domain


