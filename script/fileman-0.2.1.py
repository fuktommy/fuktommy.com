#!/usr/bin/python
#
"""Read FILEMAN page and download flash.

usage: fileman < html-list
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
import sys
from time import sleep
from threading import Thread
from urlparse import urlparse
from os.path import basename, exists

from crawler import crawl, agent


class Reader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.query = []
        self.stopflag = False
        self.setDaemon(True)

    def run(self):
        while True:
            if self.query:
                url = self.query[0]
                self.read(url)
                self.query.pop(0)
            elif self.stopflag:
                return
            sleep(5)

    def download(self, url):
        fname = basename(urlparse(url)[2])
        if exists(fname):
            print "%s: exists" % fname
            return
        print "%s -> %s" % (url, fname)
        rfile = agent.open(url)
        wfile = file(fname, "wb")
        size = int (rfile.info().getheader("Content-Length", 0))
        count = 0
        while True:
            buf = rfile.read(256*1024)
            if buf == "":
                break
            wfile.write(buf)
            count += len(buf)
            if size:
                print "%s %d/%s (%d%%)" % \
                      (fname, count, size, count*100/size)
            else:
                print "%s %d" % (fname, count)
        rfile.close()
        wfile.close()

    def read(self, url):
        urls = crawl(url)
        for u in urls:
            if u.endswith(".swf"):
                self.download(u)

    def append(self, url):
        self.query.append(url)

    def stop(self):
        self.stopflag = True

    def print_query(self):
        if self.query:
            print "----------------------"
            for q in self.query:
                print q

def main():
    reader = Reader()
    try:
        reader.start()
        while True:
            line = sys.stdin.readline()
            if line == "":
                reader.stop()
                break
            line = line.strip()
            if line:
                reader.append(line)
        reader.join()
    finally:
        reader.print_query()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
