#!/usr/bin/python
"""Update Pinger

Usage: blog-ping your-blog
                 [ping-server...]
                 [-i server-list-file]
                 [-r number-of-servers]
"""
# I read http://coreblog.org/ats/82 for using xmlrpclib.
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
import random
import socket
import urllib
import xmlrpclib
from HTMLParser import HTMLParser

__version__ = "$Revision: $"

socket.setdefaulttimeout(10)

class MyHTMLParser(HTMLParser):
    encoding = "utf-8"
    title = ""
    pointer = ""
    xmlencode = re.compile(r"xml.*encoding=.([^<>\"']+)..*\?$").findall
    htmlencode = re.compile(r"charset=([^<>\"'/]+)").findall

    def dic_attr(self, attrs):
        """Convert attrs list to dictionary."""

        d = {}
        for i in attrs:
            d[i[0]] = i[1]
        return d

    def handle_starttag(self, tag, attrs):
        """Get title tag and meta(charset) tag."""
        attrs = self.dic_attr(attrs)
        if tag == "title":
            self.pointer = "title"
        elif tag == "meta" \
            and "http-equiv" in attrs \
            and "content" in attrs \
            and attrs["http-equiv"].lower() == "content-type":
            encoding = self.htmlencode(attrs["content"])
            if encoding:
                self.encoding = encoding[0]
        else:
            self.pointer = ""

    def handle_data(self, data):
        if self.pointer == "title":
            self.title += data.strip()

    def handle_pi(self, data):
        """Get xml(encoding) tag."""
        encoding = self.xmlencode(data)
        if encoding:
            self.encoding = encoding[0]

def read_list(fp):
    """Read server list file."""
    tmp = []
    for line in fp:
        line = line.strip()
        if line and (not line.startswith("#")):
            tmp.append(line)
    return tmp

def get_title(url):
    """Get HTML and parse it."""
    f = urllib.urlopen(url)
    buf = f.read()
    f.close()
    parser = MyHTMLParser()
    parser.feed(buf)
    parser.close()
    title = unicode(parser.title, parser.encoding).encode("utf-8")
    return title

#
# Main
#

myblog = ""
servers = []
num = 0

argv = sys.argv[1:]
while argv:
    i = argv.pop(0)
    if i == "-i":
        filename = argv.pop(0)
        if filename == "-":
            servers.extend(read_list(sys.stdin))
        else:
            f = file(filename)
            servers.extend(read_list(f))
            f.close()
    elif i == "-r":
        num = int(argv.pop(0))
    elif not myblog:
        myblog = i
    else:
        servers.append(i)

if (not myblog) or (not servers):
    sys.exit("usage: blog-ping your-blog"
             " [ping-server...] [-i server-list-file]"
             " [-r number-of-servers]")
elif num > 0:
     random.shuffle(servers)
     servers = servers[:num-1]

title = get_title(myblog)

for i in servers:
    try:
        print "Ping %s" % i
        svr = xmlrpclib.ServerProxy(i)
        resp = svr.weblogUpdates.ping(title, myblog)
        flerror = resp.get("flerror", False)
        message = resp.get("message", "None")
        if flerror:
            print "    Error: %s" % message
        else:
            print "    %s" % message
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception, err:
        print "    Error: %s" % str(err)
