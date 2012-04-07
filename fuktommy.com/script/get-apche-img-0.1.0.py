#!/usr/bin/python
#
"""Get images from Apache style index.

require: wget

usage: get-apache-img uri
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
import os
import sys
import time
import urllib

agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
pat_anc = re.compile(r'<A HREF="[^"]+">([^<>]+)</A>')
pat_img = re.compile(r"(\.jpg|\.gif|\.png)$", re.I)
pat_ign = re.compile(r"(s\.jpg|s\.gif|s\.png)$", re.I)

wget = ["wget", "--random-wait", "-nv",
    "--header=Accept-Encoding: gzip, compres, bzip, bzip2, deflate",
    "--header=Accept-Language: ja; q=1.0, en;q=0.5",
    "-U", agent, "-w", "2", "-T", "60", "-t", "2", "-nc", "-x"]

class MyURLopener(urllib.FancyURLopener):
    def __init__(self, *args):
        self.version = agent
        urllib.FancyURLopener.__init__(self, *args)

urllib._urlopener = MyURLopener()

try:
    dirs = [sys.argv[1]]
except IndexError:
    sys.exit("usage: get-apache-img uri")

while dirs:
    imgs = []
    d = dirs.pop(0)
    f = urllib.urlopen(d)
    for line in f:
        found = pat_anc.search(line)
        if found:
           anchor = found.group(1)
        else:
            continue
        if anchor.endswith("/"):
            dirs.append(d + anchor)
        elif pat_img.search(anchor) and (not pat_ign.search(anchor)):
            imgs.append(d + anchor)
    f.close()
    time.sleep(2)

    if imgs:
        os.spawnvp(os.P_WAIT, wget[0], wget + imgs)
