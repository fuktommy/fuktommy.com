#!/usr/bin/python
#
'''Check mixi friends' diary.

When new diary uploaded, mail user.
It should be called by crond.

Diary title lists are ~/mixicheck/<userid>.txt .

Set mixi cookie ~/mixicheck/cookie .
    BF_SESSION=foo
    BF_STAMP=bar
'''
#
# Copyright (c) 2006 Satoshi Fukutomi <info@fuktommy.com>.
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
import urllib

#
# Config
#
cache_dir = os.path.expanduser('~/mixicheck')
cookie_file = os.path.join(cache_dir, 'cookie')

class CachedCookie:
    def __init__(self):
        f = file(cookie_file)
        buf = f.readlines()
        self.cookie = '; '.join([line.strip() for line in buf])

    def __str__(self):
        return self.cookie
# End of CachedCookie


urllib.URLopener.version = 'Mozilla/5.00 (mixichecker/0.1)'
class MixiClient(urllib.FancyURLopener):
    def __init__(self, cookie, *args):
        urllib.FancyURLopener.__init__(self, *args)
        self.addheader('Cookie', str(cookie))
# End of MixiClient


class User:
    '''Mixi user.
    '''

    def __init__(self, uid):
        self.uid = int(uid)
        self.listuri = 'http://mixi.jp/list_diary.pl?id=%d' % self.uid
        self.cachefile = os.path.join(cache_dir, '%d.txt'%self.uid)
        self.load_cache()

    def load_cache(self):
        self.cache = {}
        for line in file(self.cachefile):
            self.cache[line.strip()] = True

    def get_titles(self):
        f = urllib.urlopen(self.listuri)
        buf = f.read()
        self.updated = False
        self.newcache = []
        for line in buf.splitlines():
            line = line.strip()
            if line.find('bgcolor=#F2DDB7') >= 0:
                if line not in self.cache:
                    self.updated = True
                self.newcache.append(line)

    def sync_cache(self):
        f = file(self.cachefile, 'w')
        for line in self.newcache:
            f.write(line + '\n')
# End of User

def main():
    cookie = CachedCookie()
    urllib._urlopener = MixiClient(cookie)
    for c in os.listdir(cache_dir):
        if not c.endswith('.txt'):
            continue
        user = User(c[:-4])     # len('.txt') == 4
        user.get_titles()
        if user.updated:
            print 'Mixi diary updated: %s' % user.listuri
        if user.newcache:
            user.sync_cache()
        else:
            sys.exit('Error in %s' % user.listuri)

if __name__ == '__main__':
    main()
