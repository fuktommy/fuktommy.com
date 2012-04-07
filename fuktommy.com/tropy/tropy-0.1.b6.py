#!/usr/local/bin/python
#
"""A clone of Tropy.

Original Tropy was written by Hiroshi Yuki.
http://www.hyuki.com/tropy/
http://www.hyuki.com/d/200511.html#i20051103183338
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
from random import choice
from time import time
from urlparse import urljoin

#
# config
#
your_site = "http://localhost:8000/"
your_css = "/common.css"
self_url = "/tropy/tropy.cgi"
data_dir = "/tmp/tropy"
page_size = 8192    # Bytes
wait_sec = 5

isid = re.compile(r"[0-9a-f]{32}").search

def header(title="", id="", wait=False):
    print 'Content-Type: text/html; charset=utf-8'
    print
    print '<?xml version="1.0" encoding="utf-8"?>'
    print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"'
    print '  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
    print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja">'
    print '<head>'
    print '<title>%s - FukTropy</title>' % title.strip()
    print '  <link rev="made" href="%s" />' % your_site
    print '  <link rel="contents" href="%s" />' % your_site
    print '  <meta name="robots" content="NOINDEX" />'
    print '  <link rel="stylesheet" type="text/css" href="%s" />' % your_css
    print '</head>'
    if wait:
        print '<script type="text/javascript">'
        print 'function wait(){'
        print '  main = document.getElementById("tropymain")'
        print '  main.style.display = "none";'
        print '  setTimeout("onTimeout()", %d000);' % wait_sec
        print '}'
        print 'function onTimeout(){'
        print '  main = document.getElementById("tropymain")'
        print '  main.style.display = "";'
        print '  info = document.getElementById("tropyinfo")'
        print '  info.style.display = "none";'
        print '}'
        print '</script>'
        print '<body onload="wait()">'
        print '<p id="tropyinfo">Please wait %d seconds.</p>' % wait_sec
    else:
        print '<body>'
    print '<div id="tropymain">'
    print '<p class="head">'
    if id:
        print '  <a href="%s?cmd=edit&amp;id=%s">Edit</a>' % (self_url, id)
    else:
        print '  Edit'
    print '  <a href="%s?cmd=edit">Create</a>' % self_url
    if id:
        print '  <a href="%s?%s">Permalink</a>' % (self_url, id)
    else:
        print '  Permalink'
    print '  <a href="%s">Random</a>' % self_url
    print '</p>'
    print '<h1>%s</h1>' % title

def footer(id=""):
    print '<p>Powered by <a href="http://fuktommy.xrea.jp/tropy/">FukTropy</a>.</p>'
    print '</div>'
    print '</body>'
    print '</html>'


class Page:
    def __init__(self, id="", data=""):
        """Constructor.

        You should send id or data.
        """
        if id:
            self.id = id
            self.read()
            try:
                self.title = self.data[0]
                self.body = self.data[1:]
            except IndexError:
                self.title = ""
                self.body = []
        else:
            self.id = md5.new("%d %s" % (time(), data)).hexdigest()
            self.data = data.splitlines(True)
            self.title = ""
            self.body = []

    def read(self):
        try:
            f = file(os.path.join(data_dir, self.id))
            self.data = f.readlines()
            f.close()
        except IOError:
            self.data = []

    def sync(self):
        f = file(os.path.join(data_dir, self.id), "wb")
        for i in self.data:
            f.write(i)
        f.close()

    def remove(self):
        try:
            os.remove(os.path.join(data_dir, self.id))
        except OSError:
            pass

    def update(self, data):
        if data:
            self.data = data.splitlines(True)
            self.sync()
        else:
            self.remove()

# End of Page


def randompage():
    ids = os.listdir(data_dir)
    if ids:
        return choice(ids)
    else:
        return ""

def view(id="", wait=False):
    if not isid(id):
        id = randompage()
    if id:
        page = Page(id=id)
        if page.title:
            header(cgi.escape(page.title), id=id, wait=wait)
            print '<p>'
            for line in page.body:
                line = cgi.escape(line)
                line = line.replace("\r", "").replace("\n", "<br />")
                print line
            print '</p>'
            footer()
        else:
            error("No such page.")
    else:
        header("FukTropy")
        footer()

def edit(id=""):
    if isid(id):
        page = Page(id=id)
        if page.title:
            title = page.title
            body = page.body
            header(cgi.escape(title), id=id)
        else:
            error("No such page.")
            return
    else:
        title = ""
        id = ""
        body = []
        header("FukTropy")
    print '<form method="post" action="%s"><p>' % self_url
    print '<input type="hidden" name="cmd" value="write" />'
    print '<input type="hidden" name="id" value="%s" />' % id
    if title:
        print '<textarea cols="80" rows="20" name="msg"'
        print 'tabindex="1" accesskey="m">%s' % title,
        for line in body:
            print cgi.escape(line),
        print '</textarea><br />'
    else:
        print '<textarea cols="80" rows="20" name="msg"'
        print 'tabindex="1" accesskey="m"></textarea></br>'
    print '<input type="submit" name="submit" value="Write"'
    print 'tabindex="2" accesskey="w" />'
    print '</p></form>'
    footer()

def error(msg=""):
    if not msg:
        msg = "Something Wrong"
    header("ERROR: %s " % msg)
    print '<p>%s</p>' % msg
    footer()

def write(id="", msg=""):
    if len(msg) > page_size:
        error("Too large page.")
    elif isid(id):
        page = Page(id=id)
        page.update(msg)
        if msg:
            view(id)
        else:
            view()
    elif not id:
        page = Page(data=msg)
        page.sync()
        view(page.id)
    else:
        view()

def main():
    q = os.environ.get("QUERY_STRING", "")
    if isid(q):
        id = q
    else:
        id = ""
    form = cgi.FieldStorage()
    cmd = form.getfirst("cmd")
    id = form.getfirst("id", id)
    msg = form.getfirst("msg", "")

    if cmd == "edit":
        edit(id)
    elif cmd == "write":
        write(id, msg)
    elif id:
        view(id)
    else:
        view(wait=True)

if __name__ == "__main__":
    main()
