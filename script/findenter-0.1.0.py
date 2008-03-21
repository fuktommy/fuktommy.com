#!/usr/bin/python
#
"""Find enter for adult sites.

It require ``clower'' module.
    (Get it from http://fuktommy.s64.xrea.com/script/ )

usage: getenter http://example.com/
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
import sys
from urlparse import urlparse

from crawler import crawl
pat_image = re.compile(r"\.(jpg|jpeg|gif|png)$", re.I)
pat_media = re.compile(r"\.(tar.gz|tgz|zip|lzh|mpg|mp3)$", re.I)

def findenter(url):
    """Find the URLs that are in same hosts."""
    host = urlparse(url)[1]
    urls = crawl(url)
    for u in urls:
        h = urlparse(u)[1]
        if (h == host) and (not pat_image.search(u)) \
                       and (not pat_media.search(u)):
            print u

def main():
    for i in sys.argv[1:]:
        if i.find("://") < 0:
            i = "http://" + i
        findenter(i)

if __name__ == "__main__":
    main()
    sys.exit()











def geturl(url):
    """Get URL and output URLs of images."""
    sys.stderr.write("Reading %s\n" % url)
    loop[url] = True
    host = urlparse(url)[1]
    urls = crawl(url)
    next = []
    protocol = re.compile(r"^(http://|https://|ftp://)")
    for u in urls:
        uhost =  urlparse(u)[1]
        if u in loop:
            pass
        elif not protocol.search(u):
            loop[u] = True
        elif pat_ign.search(u):
            loop[u] = True
        elif pat_img.search(u):
            loop[u] = True
            print u
        elif uhost != host:
            pass
        else:
            sleep(2)
            geturl(u)

def main():
    for i in sys.argv[1:]:
        if i.find("://") < 0:
            i = "http://" + i
        geturl(i)

if __name__ == "__main__":
    main()
