#!/usr/bin/python
#
"""Output OGG title list.

usage: ogglist oggfiles
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

import sys
from ogg.vorbis import VorbisFile, VorbisError

def mklist(hash, key):
    try:
        val = vc[key]
        if not val:
            val = [""]
    except KeyError:
        val = [""]
    return val

def decode(u, filename):
    try:
        return u.encode("utf-8")
    except UnicodeDecodeError:
        try:
            return unicode(u, "sjis").encode("utf-8")
        except UnicodeDecodeError:
            sys.stderr.write("UnicodeError in %s\n" % filename)
            return ""

for i in sys.argv[1:]:
    try:
        vf = VorbisFile(i)
        vc = vf.comment()
    except VorbisError:
        continue
    artist = mklist(vc, "ARTIST")
    title = mklist(vc, "TITLE")
    for j in artist:
        j = decode(j, i)
        for k in title:
            k = decode(k, i)
            try:
                print "%s\t%s\t%s" % (i, j, k)
            except UnicodeDecodeError:
                sys.stderr.write("UnicodeError in %s\n" % i)
