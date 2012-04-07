#!/usr/local/bin/python
"""Text Uploader.

Save posted text to <md5>.txt
"""
# Copyright (c) 2005 Satoshi Fukutomi <fuktommy@inter7.jp>.
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
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# $Id: $
#

import cgi
import md5

__version__ = "$Revision: $"

LIMIT = 8192
DIR = "."
MYSELF = "textup.cgi"

def message(msg):
    print "Content-Type: text/html"
    print
    print "<html><head><title>TextUp</title><body>"
    print msg
    print "</body></html>"

def printform():
    message('<form method="post" action="%s">' % MYSELF +
            '<input type="submit" name="post" value="POST"><br>' +
            '<textarea name="text" rows="5" cols="70"></textarea></form>')

def save(text):
    id = md5.new(text).hexdigest()
    f = file("%s/%s.txt" % (DIR, id), "wb")
    f.write(text)
    f.close()
    return id

def main():
    form = cgi.FieldStorage()
    text = form.getfirst("text", "")
    if len(text) > LIMIT:
        message("<p>Too Big</p>")
    elif text:
        id = save(text)
        message('<p>OK: <a href="%s.txt">%s</a></p>' % (id, id))
    else:
        printform()

if __name__ == "__main__":
    main()
