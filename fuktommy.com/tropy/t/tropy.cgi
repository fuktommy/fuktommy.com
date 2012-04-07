#!/usr/local/bin/python
#
"""FukTropy2 - Ajax Tropy
"""
#
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

import re
import os
import cgi
import md5
from time import time
from random import shuffle

#
# config
#
xml_dir = "./xml"
page_size = 8192    # Bytes
list_size = 50      # Pages

isid = re.compile(r"[0-9a-f]{32}").search

def escape(s):
    s = cgi.escape(s, True)
    s = s.replace("\r", "").replace("\n", "<br />")
    s = cgi.escape(s, True)
    return s


class Page:
    def __init__(self, id=""):
        """Constructor."""
        self.id = id

    def read(self):
        f = file(os.path.join(xml_dir, self.id+".xml"))
        buf = f.read()
        f.close()
        return buf

    def sync(self):
        f = file(os.path.join(xml_dir, self.id+".xml"), "wb")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<tropy>\n')
        f.write('<id>%s</id>\n' % self.id)
        f.write('<title>%s</title>\n' % self.title)
        f.write('<body>%s</body>\n' % self.body)
        f.write('</tropy>\n')
        f.close()

    def remove(self):
        try:
            os.remove(os.path.join(xml_dir, self.id+".xml"))
        except OSError:
            pass

    def update(self, title, body):
        if not self.id:
            self.id = md5.new("%d %s %s" % (time(), title, body)).hexdigest()
        if title or body:
            self.title = escape(title)
            self.body = escape(body)
            self.sync()
            update_index()
        else:
            self.remove()
            update_index()

# End of Page


def update_index():
    ids = os.listdir(xml_dir)
    shuffle(ids)
    try:
        f = file(os.path.join(xml_dir, "ids.xml"), "wb")
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<tropy>\n')
        for i in ids[:list_size]:
            i = i.replace(".xml", "")
            if isid(i):
                f.write('<id>%s</id>\n' % i)
        f.write('</tropy>\n')
        f.close()
    except (IOError, OSError):
        pass

def error(msg="Something wrong"):
    print "Content-Type: text/xml; charset=UTF-8"
    print
    print '<?xml version="1.0" encoding="utf-8"?>'
    print '<error>%s</error>' % msg

def write(id="", title="", body=""):
    title = title.strip().replace("<br />", "")
    body = body.strip()
    if len(title)+len(body) > page_size:
        error("Too large page.")
    elif isid(id):
        page = Page(id=id)
        page.update(title, body)
        if title or body:
            view(id)
        else:
            error("Removed")
    elif not id:
        page = Page()
        page.update(title, body)
        if title or body:
            view(page.id)
        else:
            error()
    else:
        error()

def view(id=""):
    """Output XML."""
    if id:
        page = Page(id)
        print "Content-Type: text/xml; charset=UTF-8"
        print
        print page.read()
    else:
        error("Wrong page name")

def main():
    try:
        form = cgi.FieldStorage()
        id = form.getfirst("id", "")
        title = form.getfirst("title", "")
        body = form.getfirst("body", "")
        write(id, title, body)
    except (KeyError, ValueError, IOError), e:
        error(e)

if __name__ == "__main__":
    main()
