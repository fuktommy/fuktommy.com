#!/usr/bin/python
'''Report or omit repeated files.

usage: filediet [-n] directory...
options: -n: show what would have been removed
'''
#
# Copyright (c) 2006,2007 Satoshi Fukutomi <info@fuktommy.com>.
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
import md5
import os
from shutil import move

#
# Config
#
TRASH = os.path.expanduser('~/Trash')
CACHE = 'MD5CACHE'

class MD5Cache:
    '''MD5 Cache File.

    One file par one directory.
    '''

    def __init__(self, dirname):
        self.hash = {}
        self.dirname = dirname
        self.cachefile = os.path.join(dirname, CACHE)
        if os.path.isfile(self.cachefile):
            for line in file(self.cachefile):
                line = line.strip()
                self.hash[line[34:]] = line[:32]

    def sync(self):
        fp = file(self.cachefile, 'w')
        for key, value in self.hash.iteritems():
            fp.write('%s  %s\n' % (value, key))

    def update(self, files):
        '''Read files and cache MD5 digest.

        Files is a list of file basenames.
        '''
        for key in self.hash.keys():
            if not os.path.isfile(os.path.join(self.dirname, key)):
                del self.hash[key]
        for f in files:
            if (f != CACHE) and (f not in self.hash):
                path = os.path.join(self.dirname, f)
                self.hash[f] = md5.new(file(path, 'rb').read()).hexdigest()

    def __iter__(self):
        for key, value in self.hash.iteritems():
            yield os.path.join(self.dirname, key), value

# End of MD5Cache


class SortFunc:
    def __init__(self, hash):
        self.hash = hash

    def cmp(self, a, b):
        buf = cmp(self.hash[a], self.hash[b])
        if buf:
            return buf
        buf = cmp(os.path.dirname(a), os.path.dirname(b))
        if buf:
            return buf
        ba = os.path.basename(a)
        bb = os.path.basename(b)
        buf = cmp(len(ba), len(bb))
        if buf:
            return buf
        buf = cmp(ba, bb)
        return buf

# End of SortFunc


def samefile(a, b):
    if os.path.getsize(a) != os.path.getsize(b):
        return False
    fa = file(a, 'rb')
    fb = file(b, 'rb')
    while True:
        ba = fa.read(1)
        bb = fb.read(1)
        if (not ba) and (not bb):
            return True
        elif ba != bb:
            return False

def main():
    hash = {}       # hash[filename] == md5digest
    if not os.path.isdir(TRASH):
        os.makedirs(TRASH)
    targets = []
    dry_run = False
    buf = sys.argv[1:]
    while buf:
        i = buf.pop()
        if i == '-n':
            dry_run = True
        elif i == '--':
            targets.extend(buf)
        else:
            targets.append(i)
    if not targets:
        sys.exit('usage: filediet [-n] directorys')

    # update caches.
    for i in targets:
        for dirpath, dirnames, filenames in os.walk(i):
            cache = MD5Cache(dirpath)
            cache.update(filenames)
            cache.sync()
            for key, value in cache:
                hash[key] = value

    filenames = hash.keys()
    filenames.sort(SortFunc(hash).cmp)

    # remove files.
    if filenames:
        last = filenames.pop(0)
    for f in filenames:
        if (hash[last] == hash[f]) and samefile(last, f):
            print f
            if not dry_run:
                move(f, TRASH)
        else:
            last = f


if __name__ == '__main__':
    main()
