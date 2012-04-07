#!/usr/bin/python
#
'''Decoder for multi-part message in MIME format.

usage: mimedec message-file
'''
#
# _unquote() is from urllib.py in Python2.4.
#
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

import re
import os.path
import base64
from urlparse import urlparse
from fileinput import input

class Message:
    '''E-mail message.
    '''

    def __init__(self, fp):
        self.fp = fp
        self.boundary = None

    def read_head(self):
        while True:
            line = self.fp.readline().strip()
            if line == '':
                break
            found = re.search(r'boundary="(.*)"', line)
            if found:
                self.boundary = '--%s' % found.group(1)

    def skip_description(self):
        while True:
            line = self.fp.readline()
            if line.startswith(self.boundary):
                break

    def read_body(self):
        while True:
            part = Part(self.fp, self.boundary)
            part.read_head()
            yield part

# End of Message


_hextochr = dict(('%02x' % i, chr(i)) for i in range(256))
_hextochr.update(('%02X' % i, chr(i)) for i in range(256))

def _unquote(s):
    """unquote('abc=20def') -> 'abc def'."""
    res = s.split('=')
    for i in xrange(1, len(res)):
        item = res[i]
        if re.search(r'^[\r\n]+$', item):
            res[i] = ''
        else:
            try:
                res[i] = _hextochr[item[:2]] + item[2:]
            except KeyError:
                res[i] = '=' + item
            except UnicodeDecodeError:
                res[i] = unichr(int(item[:2], 16)) + item[2:]
    return ''.join(res)

class Part:
    '''A part of multi-part message.
    '''

    def __init__(self, fp, boundary):
        self.fp = fp
        self.boundary = boundary
        self.quoted_printable = False
        self.base64 = False
        self.filename = None

    def read_head(self):
        while True:
            line = self.fp.readline()
            sline = line.strip()
            if line == '':
                raise StopIteration
            elif (sline == '') or line.startswith(self.boundary):
                break
            elif sline == 'Content-Transfer-Encoding: quoted-printable':
                self.quoted_printable = True
            elif sline == 'Content-Transfer-Encoding: base64':
                self.base64 = True

            found = re.search(r'^Content-Location:(.*)', sline)
            if found:
                self.location = found.group(1)
                buf = urlparse(self.location)
                self.filename = os.path.basename(buf[2])

    def read_body(self):
        buf = []
        while True:
            line = self.fp.readline()
            if line.startswith(self.boundary) or (line == ''):
                break
            else:
                buf.append(line)
        return ''.join(buf)

    def write_quoted_printable(self, buf):
        wfile = file(self.filename, 'wb')
        wfile.write(_unquote(buf))

    def write_base64(self, buf):
        wfile = file(self.filename, 'wb')
        wfile.write(base64.decodestring(buf))

    def write(self, buf):
        wfile = file(self.filename, 'wb')
        wfile.write(buf)

# End of Part


def main():
    message = Message(input())
    message.read_head()
    message.skip_description()

    for part in message.read_body():
        buf = part.read_body()
        if part.quoted_printable:
            print '(quoted)', part.filename
            part.write_quoted_printable(buf)
        elif part.base64:
            print '(base64)', part.filename
            part.write_base64(buf)
        else:
            print '(raw)', part.filename
            part.write(buf)

if __name__ == '__main__':
    main()
