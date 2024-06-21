publicsuffixlist
===

[Public Suffix List](https://publicsuffix.org/) parser implementation for
Python 3.5+.

- Compliant with [TEST DATA](https://raw.githubusercontent.com/publicsuffix/list/master/tests/test_psl.txt)
- Supports IDN (unicode and punycoded).
- Supports Python3.5+
- Shipped with built-in PSL and an updater script.
- Written in Pure Python with no library dependencies.

[![publish package](https://github.com/ko-zu/psl/actions/workflows/autorelease.yml/badge.svg?branch=master)](https://github.com/ko-zu/psl/actions/workflows/autorelease.yml)
[![CI test](https://github.com/ko-zu/psl/actions/workflows/citest.yml/badge.svg?branch=devel)](https://github.com/ko-zu/psl/actions/workflows/citest.yml)
[![PyPI version](https://badge.fury.io/py/publicsuffixlist.svg)](https://badge.fury.io/py/publicsuffixlist)
[![Downloads](http://pepy.tech/badge/publicsuffixlist)](http://pepy.tech/project/publicsuffixlist)

Install
===
`publicsuffixlist` can be installed via `pip`.
```
$ pip install publicsuffixlist
```

Usage
===

Basic Usage:

```python
from publicsuffixlist import PublicSuffixList

psl = PublicSuffixList()
# Uses built-in PSL file

print(psl.publicsuffix("www.example.com"))   # "com"
# the longest public suffix part

print(psl.privatesuffix("www.example.com"))  # "example.com"
# the shortest domain assigned for a registrant

print(psl.privatesuffix("com")) # None
# Returns None if no private (non-public) part found

print(psl.publicsuffix("www.example.unknownnewtld")) # "unknownnewtld"
# New TLDs are valid public suffix by default

print(psl.publicsuffix("www.example.香港")) #"香港"
# Accepts unicode

print(psl.publicsuffix("www.example.xn--j6w193g")) # "xn--j6w193g"
# Accepts Punycode IDNs by default

print(psl.privatesuffix("WWW.EXAMPLE.COM")) # "example.com"
# Returns in lowercase by default

print(psl.privatesuffix("WWW.EXAMPLE.COM", keep_case=True) # "EXAMPLE.COM"
# kwarg `keep_case=True` to disable the case conversion
```

The latest PSL is packaged once a day. If you need to parse your own version,
it can be passed as a file-like iterable object, or just a `str`:

```python
with open("latest_psl.dat", "rb") as f:
    psl = PublicSuffixList(f)
```

The unittest and PSL updater can be invoked as module.
```
$ python -m publicsuffixlist.test
$ python -m publicsuffixlist.update
```

Additional convenient methods:

```python
print(psl.is_private("example.com"))  # True
print(psl.is_public("example.com"))   # False
print(psl.privateparts("aaa.www.example.com")) # ("aaa", "www", "example.com")
print(psl.subdomain("aaa.www.example.com", depth=1)) # "www.example.com"
```

Limitation
===

#### Domain Label Validation

`publicsuffixlist` do NOT provide domain name and label validation.
In the DNS protocol, most 8-bit characters are acceptable as labels of domain
names. While ICANN-compliant registries do not accept domain names containing
underscores (_), hostnames may include them. For example, DMARC records can
contain underscores. Users must confirm that the input domain names are valid
based on their specific context.

#### Punycode Handling
Partially encoded (Unicode-mixed) Punycode is not supported due to very slow
Punycode encoding/decoding and unpredictable encoding results. If you are
unsure whether an input is valid Punycode, you should use:
`unknowndomain.encode("idna").decode("ascii")`. This method, converting to idna
is idempotent.

#### Handling Arbitrary Binary
If you need to accept arbitrary or malicious binary data, it can be passed as a
tuple of bytes. Note that the returned bytes may include byte patterns that
cannot be decoded or represented as a standard domain name.
Example:
```python
psl.privatesuffix((b"a.a", b"a.example\xff", b"com"))  # (b"a.example\xff", b"com")

# Note that IDNs must be punycoded when passed as tuple of bytes.
psl = PublicSuffixList("例.example")
psl.publicsuffix((b"xn--fsq", b"example"))  # (b"xn--fsq", b"example")
# UTF-8 encoded bytes of "例" do not match.
psl.publicsuffix((b"\xe4\xbe\x8b", b"example"))  # (b"example",)
```

License
===

- This module is licensed under Mozilla Public License 2.0.
- The Public Suffix List maintained by the Mozilla Foundation is licensed under
  the Mozilla Public License 2.0.
- The PSL testcase dataset is in the public domain (CC0).


Development / Packaging
===
This module and its packaging workflow are maintained in the author's
repository located at https://github.com/ko-zu/psl.

A new package, which includes the latest PSL file, is automatically generated
and uploaded to PyPI. The last part of the version number represents the
release date. For example, `0.10.1.20230331` indicates a release date of March
31, 2023.

This package dropped support for Python 2.7 and Python 3.4 or prior versions at
the version 1.0.0 release in June 2024. The last version that works on Python
2.x is 0.10.0.x.


Source / Link
===

- GitHub repository: (https://github.com/ko-zu/psl)
- PyPI: (https://pypi.org/project/publicsuffixlist/)

