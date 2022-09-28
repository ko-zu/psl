# -*- coding: utf-8 -*-
#
# Copyright 2014 ko-zu <causeless@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os
import re
import unittest

from publicsuffixlist import PublicSuffixList, b, encode_idn, u


class TestPSL(unittest.TestCase):

    def setUp(self):

        self.psl = PublicSuffixList()

    def test_typesafe(self):
        self.assertEqual(self.psl.suffix("www.example.co.jp").__class__, "example.co.jp".__class__)
        self.assertEqual(self.psl.suffix(u("www.example.co.jp")).__class__, u("example.co.jp").__class__)

        self.assertEqual(self.psl.publicsuffix("www.example.co.jp").__class__, "co.jp".__class__)
        self.assertEqual(self.psl.publicsuffix(u("www.example.co.jp")).__class__, u("co.jp").__class__)

    def test_uppercase(self):
        self.assertEqual(self.psl.suffix("Jp"), None)
        self.assertEqual(self.psl.suffix("cO.Jp"), None)
        self.assertEqual(self.psl.suffix("eXaMpLe.cO.Jp"), "example.co.jp")
        self.assertEqual(self.psl.suffix("wWw.eXaMpLe.cO.Jp"), "example.co.jp")
        self.assertEqual(self.psl.publicsuffix("Jp"), "jp")
        self.assertEqual(self.psl.publicsuffix("cO.Jp"), "co.jp")
        self.assertEqual(self.psl.publicsuffix("eXaMpLe.cO.Jp"), "co.jp")
        self.assertEqual(self.psl.publicsuffix("wWw.eXaMpLe.cO.Jp"), "co.jp")

    def test_invaliddomain(self):
        self.assertEqual(self.psl.suffix("www..invalid"), None)
        self.assertEqual(self.psl.suffix(".example.com"), None)
        self.assertEqual(self.psl.suffix("example.com."), None)
        self.assertEqual(self.psl.suffix(""), None)

        self.assertEqual(self.psl.publicsuffix("www..invalid"), None)
        self.assertEqual(self.psl.publicsuffix(".example.com"), None)
        self.assertEqual(self.psl.publicsuffix("example.com."), None)
        self.assertEqual(self.psl.publicsuffix(""), None)

    def test_idn(self):
        tld = u("香港")
        self.assertEqual(self.psl.suffix(u("www.example.") + tld), u("example.") + tld)
        self.assertEqual(self.psl.publicsuffix(u("www.example.") + tld), tld)

    def test_punycoded(self):
        tld = encode_idn(u("香港"))
        self.assertEqual(self.psl.suffix(u("www.example.") + tld), u("example.") + tld)
        self.assertEqual(self.psl.publicsuffix(u("www.example.") + tld), tld)

    def test_suffix_deny_public(self):
        self.assertEqual(self.psl.suffix("com"), None)
        self.assertEqual(self.psl.suffix("co.jp"), None)
        self.assertEqual(self.psl.suffix("example.nagoya.jp"), None)

    def test_unknown(self):
        self.assertEqual(self.psl.suffix("www.example.unknowntld"), "example.unknowntld")
        self.assertEqual(self.psl.suffix("unknowntld"), None)

        self.assertEqual(self.psl.suffix("www.example.unknowntld", accept_unknown=True), "example.unknowntld")
        self.assertEqual(self.psl.suffix("unknowntld", accept_unknown=True), None)
        self.assertEqual(self.psl.suffix("www.example.unknowntld", accept_unknown=False), None)
        self.assertEqual(self.psl.suffix("unknowntld", accept_unknown=False), None)

        self.assertEqual(self.psl.publicsuffix("www.example.unknowntld"), "unknowntld")
        self.assertEqual(self.psl.publicsuffix("unknowntld"), "unknowntld")

        self.assertEqual(self.psl.publicsuffix("www.example.unknowntld", accept_unknown=True), "unknowntld")
        self.assertEqual(self.psl.publicsuffix("unknowntld", accept_unknown=True), "unknowntld")
        self.assertEqual(self.psl.publicsuffix("www.example.unknowntld", accept_unknown=False), None)
        self.assertEqual(self.psl.publicsuffix("unknowntld", accept_unknown=False), None)

    def test_deny_unknown(self):
        source = """
known
"""
        psl = PublicSuffixList(source.splitlines(), accept_unknown=False)

        self.assertEqual(psl.suffix("www.example.unknowntld"), None)

    def test_custom_psl(self):
        source = """
invalid
*.invalid
!test.invalid
"""
        psl = PublicSuffixList(source.splitlines())

        self.assertEqual(psl.suffix("example.invalid"), None)
        self.assertEqual(psl.suffix("test.invalid"), "test.invalid")
        self.assertEqual(psl.suffix("some.test.invalid"), "test.invalid")
        self.assertEqual(psl.suffix("aaa.bbb.ccc.invalid"), "bbb.ccc.invalid")

        self.assertEqual(psl.publicsuffix("example.invalid"), "example.invalid")
        self.assertEqual(psl.publicsuffix("test.invalid"), "invalid")

    def test_publicsuffix(self):
        self.assertEqual(self.psl.publicsuffix("www.example.com"), "com")
        self.assertEqual(self.psl.publicsuffix("unknowntld"), "unknowntld")

    def test_wildcard(self):
        self.assertEqual(self.psl.suffix("test.example.nagoya.jp"), "test.example.nagoya.jp")
        self.assertEqual(self.psl.suffix("example.nagoya.jp"), None)
        self.assertEqual(self.psl.publicsuffix("example.nagoya.jp"), "example.nagoya.jp")
        self.assertEqual(self.psl.publicsuffix("test.example.nagoya.jp"), "example.nagoya.jp")

    def test_checkpublicsuffix_script(self):
        regex = re.compile(r"^checkPublicSuffix\(('[^']+'), (null|'[^']+')\);")
        with open(os.path.join(os.path.dirname(__file__), "test_psl.txt"), "rb") as f:
            ln = 0

            for line in f:
                ln += 1
                l = line.decode("utf-8")
                m = regex.match(l)
                if not m:
                    continue

                arg = m.group(1).strip("'")
                res = None if m.group(2) == "null" else m.group(2).strip("'")

                self.assertEqual(self.psl.suffix(arg), res, "in line {0}: {1}".format(ln, line.strip()))

    def test_typeerror(self):

        self.assertRaises(TypeError, lambda: self.psl.suffix(None))
        self.assertRaises(TypeError, lambda: self.psl.suffix(1))
        if b("") != "":
            # python3
            self.assertRaises(TypeError, lambda: self.psl.suffix(b("www.example.com")))

    def test_compatclass(self):

        from publicsuffixlist.compat import PublicSuffixList
        psl = PublicSuffixList()

        self.assertEqual(psl.get_public_suffix("test.example.com"), "example.com")
        self.assertEqual(psl.get_public_suffix("com"), "")
        self.assertEqual(psl.get_public_suffix(""), "")

    def test_unsafecompatclass(self):

        from publicsuffixlist.compat import UnsafePublicSuffixList
        psl = UnsafePublicSuffixList()

        self.assertEqual(psl.get_public_suffix("test.example.com"), "example.com")
        self.assertEqual(psl.get_public_suffix("com"), "com")
        self.assertEqual(psl.get_public_suffix(""), "")

    def test_toomanylabels(self):
        d = "a." * 1000000 + "example.com"

        self.assertEqual(self.psl.publicsuffix(d), "com")
        self.assertEqual(self.psl.privatesuffix(d), "example.com")

    def test_flatstring(self):
        psl = PublicSuffixList(u("com\nnet\n"))
        self.assertEqual(psl.publicsuffix("example.com"), "com")

    def test_flatbytestring(self):
        psl = PublicSuffixList(b("com\nnet\n"))
        self.assertEqual(psl.publicsuffix("example.com"), "com")

    def test_privateparts(self):
        psl = self.psl
        self.assertEqual(psl.privateparts("Jp"), None)
        self.assertEqual(psl.privateparts("Co.Jp"), None)
        self.assertEqual(psl.privateparts("Example.Co.Jp"), ("example.co.jp",))
        self.assertEqual(psl.privateparts("Www.Example.Co.Jp"), ("www", "example.co.jp"))
        self.assertEqual(psl.privateparts("Aaa.Www.Example.Co.Jp"), ("aaa", "www", "example.co.jp"))

    def test_noprivateparts(self):
        psl = self.psl
        self.assertEqual(psl.privateparts("com"), None)  # no private part

    def test_reconstructparts(self):
        psl = self.psl
        self.assertEqual(".".join(psl.privateparts("aaa.www.example.com")), "aaa.www.example.com")

    def test_subdomain(self):
        psl = self.psl
        self.assertEqual(psl.subdomain("Aaa.Www.Example.Co.Jp", depth=0), "example.co.jp")
        self.assertEqual(psl.subdomain("Aaa.Www.Example.Co.Jp", depth=1), "www.example.co.jp")
        self.assertEqual(psl.subdomain("Aaa.Www.Example.Co.Jp", depth=2), "aaa.www.example.co.jp")
        self.assertEqual(psl.subdomain("Aaa.Www.Example.Co.Jp", depth=3), None)  # no sufficient depth

        # not private suffix
        self.assertEqual(psl.subdomain("Com", depth=0), None)
        self.assertEqual(psl.subdomain("Com", depth=1), None)

    def test_longwildcard(self):
        source = """
com
*.compute.example.com
"""
        psl = PublicSuffixList(source.splitlines())

        self.assertEqual(psl.publicsuffix("com"), "com")
        self.assertEqual(psl.privatesuffix("com"), None)

        self.assertEqual(psl.publicsuffix("example.com"), "com")
        self.assertEqual(psl.privatesuffix("example.com"), "example.com")

        self.assertEqual(psl.publicsuffix("compute.example.com"), "com")
        self.assertEqual(psl.privatesuffix("compute.example.com"), "example.com")

        self.assertEqual(psl.publicsuffix("region.compute.example.com"), "region.compute.example.com")
        self.assertEqual(psl.privatesuffix("region.compute.example.com"), None)

        self.assertEqual(psl.publicsuffix("user.region.compute.example.com"), "region.compute.example.com")
        self.assertEqual(psl.privatesuffix("user.region.compute.example.com"), "user.region.compute.example.com")

        self.assertEqual(psl.publicsuffix("sub.user.region.compute.example.com"), "region.compute.example.com")
        self.assertEqual(psl.privatesuffix("sub.user.region.compute.example.com"), "user.region.compute.example.com")

        # mismatch in the middle
        self.assertEqual(psl.publicsuffix("user.region.not-compute.example.com"), "com")
        self.assertEqual(psl.privatesuffix("user.region.not-compute.example.com"), "example.com")

    def test_is_utilities_mixcase(self):
        psl = self.psl
        self.assertEqual(psl.is_private("Jp"), False)
        self.assertEqual(psl.is_private("Co.Jp"), False)
        self.assertEqual(psl.is_private("Example.Co.Jp"), True)
        self.assertEqual(psl.is_private("Www.Example.Co.Jp"), True)
        self.assertEqual(psl.is_public("Jp"), True)
        self.assertEqual(psl.is_public("Co.Jp"), True)
        self.assertEqual(psl.is_public("Example.Co.Jp"), False)
        self.assertEqual(psl.is_public("Www.Example.Co.Jp"), False)


class TestPSLSections(unittest.TestCase):

    def test_icann(self):
        psl = PublicSuffixList(only_icann=True)
        self.assertEqual(psl.publicsuffix("www.example.com"), 'com')
        self.assertEqual(psl.publicsuffix("example.priv.at"), 'at')


if __name__ == "__main__":
    unittest.main()
