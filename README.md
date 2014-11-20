publicsuffixlist
===

[Public Suffix List](https://publicsuffix.org/) parser implementation for Python 2.5+.

- Support IDN (unicode or punycoded).
- Compliant with [TEST DATA](http://mxr.mozilla.org/mozilla-central/source/netwerk/test/unit/data/test_psl.txt?raw=1)


Usage
===

```python

from publicsuffixlist import PublicSuffixList

psl = PublicSuffixList()

psl.publicusffix("www.example.com")   # com
# longest public suffix part

psl.privatesuffix("www.example.com")  # example.com
# shortest domain assigned for a registrant

psl.privatesuffix("com") # None
# None if no private (non-public) part found


psl.publicsuffix("www.example.unknownnewtld") # unkownnewtld
# new TLDs are valid public suffix by default

psl.publicsuffix(u"www.example.香港")   # 香港
# accept unicode

psl.publicsuffix("www.example.xn--j6w193g") # xn--j6w193g
# accept punycoded IDNs by default

```

License
===

This module is licensed under Mozilla Public License 2.0.
Public Suffix List maintained by Mozilla Foundation is licensed under Mozilla Public License 2.0.
PSL testcase dataset is public domain (CC0).

