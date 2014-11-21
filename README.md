publicsuffixlist
===

[Public Suffix List](https://publicsuffix.org/) parser implementation for Python 2.5+/3.x.

- Support IDN (unicode or punycoded).
- Compliant with [TEST DATA](http://mxr.mozilla.org/mozilla-central/source/netwerk/test/unit/data/test_psl.txt?raw=1)
- Support Python2.5+ and Python 3.x

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

Latest PSL file can be passed as a file like object.
```python

with open("latest_psl.dat", "rb") as f:
    psl = PublicSuffixList(f)
```

Works with both Python 2.x and 3.x.
```
$ python -m publicsuffixlist.test
...............
----------------------------------------------------------------------
Ran 15 tests in 2.898s

OK
$ python3 -m publicsuffixlist.test
...............
----------------------------------------------------------------------
Ran 15 tests in 2.562s

OK
```

Drop-in compat code to replace [publicsuffix](https://pypi.python.org/pypi/publicsuffix/)
```python
# from publicsuffix import PublicSuffixList
from publicsuffixlist.compat import PublicSuffixList

psl = PublicSuffixList()
psl.suffix("www.example.com")   # return "example.com"
psl.suffix("com")               # return ""

```


License
===

- This module is licensed under Mozilla Public License 2.0.
- Public Suffix List maintained by Mozilla Foundation is licensed under Mozilla Public License 2.0.
- PSL testcase dataset is public domain (CC0).

