#!/usr/bin/python
'''Jump the Last Entry of Masuda (Hatena Anonymous Diary) for Mobile.

Setup:
    echo 0 > ./masuda.last
    echo 0 > ./masuda.stamp
'''
#
# Copyright (c) 2007 Satoshi Fukutomi <info@fuktommy.com>.
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

import cgitb; cgitb.enable()
import urllib
from time import time, strftime, gmtime
from gzip import GzipFile
from StringIO import StringIO
from xml.dom.minidom import parse

#
# Config
#
interval = 600  # Seconds
#lastfile = './masuda.last'
#stampfile = './masuda.stamp'
lastfile = '/srv/data/mobile.fuktommy.com/masuda.last'
stampfile = '/srv/data/mobile.fuktommy.com/masuda.stamp'
feed = 'http://anond.hatelabo.jp/rss'


class Timestamp:
    '''System Timestamp.
    '''
    def __init__(self):
        self.stamp = int(file(stampfile).read())

    def __int__(self):
        return self.stamp

    def accepts_download(self):
        return self.stamp + interval < int(time())

    def update(self):
        file(stampfile, 'w').write('%d' % time())

# End of Timestamp


class LastEntry:
    '''Timestamp of the Last Entry.

    example: 'http://anond.hatelabo.jp/20070309214237'
    '''
    def __init__(self):
        self.entry = file(lastfile).read().strip()

    def __str__(self):
        return self.entry

    def update(self, entry):
        self.entry = entry
        file(lastfile, 'w').write(entry)

# End of LastEntry


class Masuda:
    '''Masuda RSS feed.
    '''
    def get_last(self, stamp=0):
        agent = urllib.FancyURLopener()
        agent.addheader('Accept-Encoding', 'gzip')
        #if stamp:
        #    mtime = strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime(int(stamp)))
        #    agent.addheader("If-Modified-Since", mtime)
        buf = agent.open(feed).read()
        gf = GzipFile(fileobj=StringIO(buf))
        dom = parse(gf)
        links = dom.getElementsByTagName('rdf:li')
        lastentry = links[0].attributes.item(0).value
        return lastentry

# End of Masuda


def main():
    lastentry = LastEntry()
    stamp = Timestamp()
    if stamp.accepts_download():
        masuda = Masuda()
        newlast = masuda.get_last(stamp=stamp)
        lastentry.update(newlast)
        stamp.update()
    print 'Location: http://mgw.hatena.ne.jp/?%s' % \
          urllib.quote(str(lastentry), '')
    print

if __name__ == '__main__':
    main()
