#!/usr/local/bin/python
#
"""i-bbs reader.

This downloads images from i-bbs.
It require ``crawler'' module.
    (Get it from http://fuktommy.s64.xrea.com/script/ )

usage: i-bbs bbstitle
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

import os
import re
import sys
from time import sleep
from urlparse import urlparse

from crawler import agent, crawl

loop = {}

def getimg(url, fn):
    try:
        fr = agent.open(url)
    except IOError:
        sleep(10)
        getimg(url, fn)
        return
    fw = file(fn, "wb")
    fw.write(fr.read())
    fr.close()
    fw.close()

def readbbs(title, url=None):
    if not url:
        url = "http://i-bbs.sijex.net/imageBoard.jsp?id=%s" % title
    if url in loop:
        return
    else:
        print url
        loop[url] = True
    try:
        urls = crawl(url)
    except IOError:
        loop.remove(url)
        sleep(10)
        crawl(url)
        return
    urls.reverse()
    for u in urls:
        host = urlparse(u)[1]
        if host != "i-bbs.sijex.net":
            pass
        elif re.search(r"count=\d+", u):
            readbbs(title, url=u)
        else:
            found = re.search(r"file=(\d+o[^&]*)", u)
            if found:
                fn = found.group(1)
                img = "http://image.i-bbs.sijex.net/bbs/%s/%s" % (title, fn)
                if img in loop:
                    pass
                elif not os.path.exists(fn):
                    print "   ", img
                    loop[img] = True
                    getimg(img, fn)
                    sleep(2)
    return

def main():
    try:
        title = sys.argv[1]
        if not os.path.isdir(title):
            os.mkdir(title)
        os.chdir(title)
    except IndexError, OSError:
        sys.exit("usage:i-bbs bbstitle")
    readbbs(title)

if __name__ == "__main__":
    main()
