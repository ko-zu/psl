# -*- coding: utf-8 -*-
#
# Copyright 2014 ko-zu <causeless@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os
from collections.abc import Iterable as iterable, ByteString as bytestring
from typing import Optional, Tuple, Union, Iterable, ByteString

__all__ = ["PublicSuffixList"]

ENCODING = "utf8"
ERRORMODE = "surrogateescape"

PSLURL = "https://publicsuffix.org/list/public_suffix_list.dat"

PSLFILE = os.path.join(os.path.dirname(__file__), "public_suffix_list.dat")

BytesTuple = Tuple[bytes, ...]
Domain = Union[str, BytesTuple]
RelaxDomain = Union[str, BytesTuple, Iterable[ByteString]]
RelaxFileSource = Union[Iterable[Union[str, ByteString]], str, ByteString]

Labels = Tuple[str, ...]
AnyStr = Union[str, ByteString]


def u(s: AnyStr) -> str:
    return s if isinstance(s, str) else s.decode(ENCODING, ERRORMODE)


def b(s: AnyStr) -> bytes:
    return bytes(s) if isinstance(s, bytestring) else s.encode(ENCODING, ERRORMODE)


def encode_idn(domain: AnyStr) -> str:
    return u(domain).encode("idna").decode("ascii")


def decode_idn(domain: AnyStr) -> str:
    return b(domain).decode("idna")


class PublicSuffixList(object):
    """ PublicSuffixList parser.

    After __init__(), all instance methods become thread-safe.
    Most methods accept str (not bytes) or tuple of bytes.
    """

    def __init__(self, source: Optional[RelaxFileSource] = None,
                 accept_unknown: bool = True,
                 accept_encoded_idn: bool = True,
                 only_icann: bool = False):
        """ Parse PSL source file and Return PSL object

        source: file (line iterable) object, or flat str to parse. (Default: built-in PSL file)
        accept_unknown: bool, assume unknown TLDs to be public suffix. (Default: True)
        accept_encoded_idn: bool, if False, do not generate punycoded version of PSL.
            Without punycoded PSL object, parsing punycoded IDN cause incorrect results. (Default: True)
        only_icann: bool, if True, only ICANN suffixes are honored, not private ones.
            The markers '// ===BEGIN ICANN DOMAINS===' and '// ===END ICANN DOMAINS==='
            are needed for ICANN section detection. (Default: False)
        """

        self.accept_unknown = accept_unknown

        if source is None:
            with open(PSLFILE, "rb") as source:
                self._parse(source, accept_encoded_idn, only_icann=only_icann)
        else:
            self._parse(source, accept_encoded_idn, only_icann=only_icann)

    def _parse(self, source, accept_encoded_idn, only_icann=False):
        """ PSL parser core """

        publicsuffix = set()
        maxlabel = 0
        section_is_icann = None

        if isinstance(source, (str, bytestring)):
            source = source.splitlines()

        ln = 0
        for line in source:
            ln += 1
            if only_icann:
                ul = u(line).rstrip()
                if ul == "// ===BEGIN ICANN DOMAINS===":
                    section_is_icann = True
                    continue
                elif ul == "// ===END ICANN DOMAINS===":
                    section_is_icann = False
                    continue
                if not section_is_icann:
                    continue

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

    def _joinlabels(self, domain, labels, start, *, keep_case=False):
        if isinstance(domain, str):
            if keep_case:
                return ".".join(domain.split(".")[start:])
            else:
                return ".".join(labels[start:])

        else:
            if keep_case:
                return domain[start:]
            else:
                return tuple(x.lower() for x in domain[start:])

    def _preparedomain(self, domain) -> Union[Tuple[str, Labels], Tuple[BytesTuple, Labels]]:

        if isinstance(domain, str):
            # From PSL definition,
            # Empty labels are not permitted, meaning that leading and trailing
            # dots are ignored.
            if domain.endswith("."):
                domain = domain[:-1]
            labels = domain.lower().split(".")

        elif isinstance(domain, bytestring):
            raise TypeError("Only str, Iter[ByteString] are supported.")

        elif isinstance(domain, iterable):
            domain = tuple(bytes(x) for x in domain)
            labels = tuple(str(x, ENCODING, ERRORMODE).lower()
                           for x in domain)
        else:
            raise TypeError("Only str, Iter[ByteString] are supported.")

        if "" in labels:
            # not a valid domain
            return None, None
        return domain, labels

    def _countpublic(self, labels, accept_unknown=None) -> int:

        if accept_unknown is None:
            accept_unknown = self.accept_unknown

        if not labels:
            return 0

        ll = len(labels)

        # shortcut for tld
        if ll == 1 and accept_unknown:
            return 1

        # There is the PSL algorithm definition,
        # https://github.com/publicsuffix/list/wiki/Format
        #
        # A domain is said to match a rule if and only if all of the following
        # conditions are met:
        # 1. When the domain and rule are split into corresponding labels, that
        # the domain contains as many or more labels than the rule.
        # 2. Beginning with the right-most labels of both the domain and the
        # rule, and continuing for all labels in the rule, one finds that for
        # every pair, either they are identical, or that the label from the
        # rule is "*".
        #
        # Bacause of rule 1, `foo.com` does not match `*.foo.com`.
        #
        # However, there is some confusion in rule evaluation.
        # test_psl.txt states that city.kobe.jp -> city.kobe.jp
        # so kobe.jp is public, although kobe.jp is not listed.  That means
        # test_psl.txt assumes !city.example.com or *.example.com implicitly
        # declares example.com as also public.
        #
        # This module dropped support for the conflicting test case.

        # We start from longest to shortcircuit
        startfrom = max(0, ll - (self._maxlabel + 1))

        excluded = True
        for i in range(startfrom, ll):
            depth = ll - i
            s = ".".join(labels[-depth:])

            # the check order must be wild > exact > exception
            # this is required to backtrack subdomain wildcard

            # wildcard match
            if ("*." + s) in self._publicsuffix:
                # if we have subdomain, that must be checked against exception
                # rule.
                if i > startfrom and not excluded:
                    return depth + 1

                # If this is entire match, it is not public from the PSL example.
                # ignore it.

            # exact match
            if s in self._publicsuffix:
                return depth

            # exception rule
            if ("!" + s) in self._publicsuffix:
                # exception rule has wildcard sibiling.
                # Although the test case assumes it has implicit public domain on the root,
                # in the PSL definition, the next is not always public.
                excluded = True
            else:
                excluded = False

        if accept_unknown:
            return 1
        return 0

    def suffix(self,
               domain: RelaxDomain,
               accept_unknown: Optional[bool] = None,
               *,
               keep_case: bool = False) -> Optional[Domain]:
        """ Alias for privatesuffix """
        return self.privatesuffix(domain, accept_unknown=accept_unknown, keep_case=keep_case)

    def privatesuffix(self,
                      domain: RelaxDomain,
                      accept_unknown: Optional[bool] = None,
                      *,
                      keep_case: bool = False) -> Optional[Domain]:
        """ Return shortest suffix assigned for an individual.

        domain: str or unicode to parse. (Required)
        accept_unknown: bool, assume unknown TLDs to be public suffix. (Default: object default)
        keep_case: bool, when False, returns the domain in lowercase. (Default: False)

        Return None if domain has invalid format.
        Return None if domain has no private part.
        Return in tuple of bytes if domain is tuple (or list) of bytes.
        """

        domain, labels = self._preparedomain(domain)
        publen = self._countpublic(labels, accept_unknown)

        if not publen or len(labels) < publen + 1:
            return None

        return self._joinlabels(domain, labels, -(publen + 1), keep_case=keep_case)

    def publicsuffix(self,
                     domain: RelaxDomain,
                     accept_unknown: Optional[bool] = None,
                     *,
                     keep_case: bool = False) -> Optional[Domain]:
        """ Return longest publically shared suffix.

        domain: str or unicode to parse. (Required)
        accept_unknown: bool, assume unknown TLDs to be public suffix. (Default: object default)
        keep_case: bool, when False, returns the domain in lowercase. (Default: False)

        Return None if domain has invalid format.
        Return None if domain is not listed in PSL and accept_unknown is False.
        Return in tuple of bytes if domain is tuple (or list) of bytes.
        """

        domain, labels = self._preparedomain(domain)
        publen = self._countpublic(labels, accept_unknown)

        if not publen or len(labels) < publen:
            return None

        return self._joinlabels(domain, labels, -publen, keep_case=keep_case)

    def is_private(self, domain: RelaxDomain) -> bool:
        """ Return True if domain is private suffix or sub-domain. """
        domain, labels = self._preparedomain(domain)
        publen = self._countpublic(labels)
        return bool(publen and publen < len(labels))

    def is_public(self, domain: RelaxDomain) -> bool:
        """ Return True if domain is publix suffix. """
        domain, labels = self._preparedomain(domain)
        publen = self._countpublic(labels)
        return bool(publen and publen == len(labels))

    def privateparts(self,
                     domain: RelaxDomain,
                     *,
                     accept_unknown: Optional[bool] = None,
                     keep_case: bool = False) -> Optional[Tuple[Domain, ...]]:
        """ Return tuple of subdomain labels and the private suffix. """
        domain, labels = self._preparedomain(domain)
        publen = self._countpublic(labels, accept_unknown)
        if not publen or len(labels) < publen + 1:
            return None

        priv = self._joinlabels(
            domain, labels, -(publen+1), keep_case=keep_case)
        if isinstance(domain, str):
            if keep_case:
                return tuple(domain.split(".")[:-(publen+1)]) + (priv,)
            else:
                return tuple(labels[:-(publen+1)]) + (priv,)
        else:
            if keep_case:
                return tuple(domain[:-(publen+1)]) + (priv,)
            else:
                return tuple(x.lower() for x in domain[:-(publen+1)]) + (priv,)

    def subdomain(self,
                  domain: RelaxDomain,
                  depth: int,
                  *,
                  accept_unknown: Optional[bool] = None,
                  keep_case: bool = False) -> Optional[Domain]:
        """ Return so-called subdomain of specified depth in the private suffix. """
        domain, labels = self._preparedomain(domain)
        publen = self._countpublic(labels)
        if len(labels) < publen + 1 + depth:
            return None
        else:
            return self._joinlabels(domain, labels, -(publen + 1 + depth), keep_case=keep_case)
