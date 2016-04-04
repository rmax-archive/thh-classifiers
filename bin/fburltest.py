# -*- coding: utf-8 -*-
from urlparse import urlparse, ParseResult, urljoin


o = urlparse('https://www.facebook.com/distero?fref=ts')
o2 = ParseResult(o.scheme, o.netloc, o.path, params="", query="", fragment="")
print o.geturl()
print o2.geturl()
print urljoin(o2.geturl(), "info")