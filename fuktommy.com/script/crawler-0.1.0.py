#!/usr/bin/python
#
"""Web Crawler.

This library gets HTML from the web and gets URLs from the HTML.

usage (as library):
    from crawler import crawl
    urls = crawl("http://example.com/")

usage (as command):
    crawler url1 url2... > list
"""
#
# Copyright (c) 2005 Satoshi Fukutomi <info@fuktommy.com>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

import re
import urllib
from socket import getdefaulttimeout, setdefaulttimeout
from urlparse import urljoin, urldefrag

__all__ = ["ceawl"]

agent = None

class Agent(urllib.FancyURLopener): pass

def _initialize():
    if getdefaulttimeout() is None:
        setdefaulttimeout(20)

    agent_version = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
    ua = urllib.URLopener.version
    urllib.URLopener.version = agent_version
    global agent
    agent = Agent()
    urllib.URLopener.version = ua

_initialize()

def crawl(url):
    """Get URL and return URLs."""
    urls = []
    haslink = re.compile(r"(href|src)=[\"']?([^\"'<> ]+)", re.I)
    f = agent.open(url)
    for line in f:
        while True:
            found = haslink.search(line)
            if found:
                u = found.group(2)
                u = u.replace("&amp;", "&")
                u = urldefrag(u)[0]
                u = urljoin(url, u)
                urls.append(u)
                line = line[found.end():]
            else:
                break
    urls.sort()
    buf = []
    prev = ""
    for i in urls:
        if prev != i:
            buf.append(i)
            prev = i
    return buf


def main():
    import sys
    for i in sys.argv[1:]:
        if i.find("://") < 0:
            i = "http://" + i
        for j in crawl(i):
            print j

if __name__ == "__main__":
    main()
