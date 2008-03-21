#!/usr/bin/python
#
"""Referer Images GETer.

Make referer, image list and call wget.

usage: riget img-url
example: mget http://example.com/foo/bar_030.jpg
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

wget = ["wget", "-nv", "-nc", "--random-wait",
        "--header=Accept-Encoding: gzip, compres, bzip, bzip2, deflate",
        "--header=Accept-Language: ja; q=1.0, en;q=0.5",
        "-U", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "-t", "2", "-T", "20", "-w", "2"]

def getimg(url):
    found = re.search(r"^(.+?)([^/]*?)(\d+)(\D+)$", url)
    if found:
        dir, pre, num, post = found.groups()
        length = len(num)
        urls = []
        for i in range(1, int(num)+1):
            u = "%s%s%0*d%s" % (dir, pre, length, i, post)
            urls.append(u)
        os.spawnvp(os.P_WAIT, wget[0], wget +
                              urls +
                              ["--referer=%s" % dir])

def main():
    if not sys.argv[1:]:
        sys.exit("usage: riget img-url")
    for i in sys.argv[1:]:
        getimg(i)

if __name__ == "__main__":
    main()
