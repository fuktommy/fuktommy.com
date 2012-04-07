#!/usr/bin/python
#
"""Data structure of RSS and useful functions.

It generates RSS 1.0 and/or RSS 2.0.
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

import re

__version__ = "$Revision: $"

class Item:
    """One item."""

    title = ""
    link  = ""
    description = ""
    date  = 0           # Seconds from 1970-01-01T00:00

    def __init__(self, link="", title="", date=0, description=""):
        """Constructor."""

        from xml.sax.saxutils import escape
        del_eos = re.compile(r'[\r\n]*')
        self.link  = link
        self.date  = date
        self.title = escape(del_eos.sub('', title, 0))
        self.description = escape(del_eos.sub('', description, 0))

class RSS(dict):
    """RSS.

    It is the dictionary which key is URI.
    """

    encode = "utf-8"
    lang   = "ja-jp"
    title  = ""
    parent = ""         # Place where is documents or RSS
    link   = ""         # URI of main page
    uri    = ""         # URI of RSS
    description = ""

    def __init__(self, encode="utf-8", lang="ja-jp", title="",
            parent="", link="", uri="", description="", xsl=""):
        """Constructor."""

        self.encode = encode
        self.lang   = lang
        self.title  = title
        self.description = description
        self.parent = parent
        self.xsl = xsl

        if parent and parent[-1] != "/":
            parent += "/"
            self.parent += "/"

        if link != "":
            self.link = link
        else:
            self.link = parent
        if uri != "":
            self.uri = uri
        else:
            self.uri = parent + "rss.xml"

    def append(self, link, title="", date=0, description="", abs=False):
        """Add an item."""

        if not abs:
            link = self.parent + link
        item = Item(link, title=title, date=date, description=description)
        self[link] = item

    def keys(self):
        """List of links sorted by date."""

        links = dict.keys(self)
        links.sort(lambda x,y: cmp(self[y].date, self[x].date))
        return links

    def __iter__(self):
        return iter(self.keys())

def make_rss1(rss):
    """Generate RSS 1.0."""

    buf = ""
    buf += '<?xml version="1.0" encoding="' + rss.encode + '"?>\n'
    if rss.xsl:
        buf += '<?xml-stylesheet href="%s" type="text/xsl"?>\n' % rss.xsl
    buf += '<rdf:RDF\n'
    buf += '  xmlns="http://purl.org/rss/1.0/"\n'
    buf += '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    buf += '  xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
    buf += '  xml:lang="' + rss.lang + '">\n'
    buf += '<channel rdf:about="' + rss.uri + '">\n'
    buf += '  <title>' + rss.title + '</title>\n'
    buf += '  <link>' + rss.link + '</link>\n'
    buf += '  <description>' + rss.description + '</description>\n'
    buf += '  <items><rdf:Seq>\n'

    for f in rss:
        buf += '    <rdf:li rdf:resource="' + f + '"/>\n'
    buf += '  </rdf:Seq></items>\n'
    buf += '</channel>\n'

    for uri in rss:
        f = rss[uri]
        from time import strftime, gmtime
        w3cdate = strftime('%Y-%m-%dT%H:%M:%SZ', gmtime(f.date))
        buf += '<item rdf:about="' + f.link + '">\n'
        buf += '  <title>' + f.title + '</title>\n'
        buf += '  <link>' + f.link + '</link>\n'
        buf += '  <dc:date>' + w3cdate + '</dc:date>\n'
        if f.description:
          buf += '  <description>' + f.description + '</description>\n'
        buf += '</item>\n'

    buf += '</rdf:RDF>\n'
    return buf

def make_rss2(rss):
    """Generate RSS 2.0."""

    buf = ""
    buf += '<?xml version="1.0" encoding="'+ rss.encode + '"?>\n'
    if rss.xsl:
        buf += '<?xml-stylesheet href="%s" type="text/xsl"?>\n' % rss.xsl
    buf += '<rss version="2.0">\n'
    buf += '<channel>\n'
    buf += '  <title>' + rss.title + '</title>\n'
    buf += '  <link>' + rss.uri + '</link>\n'
    buf += '  <description>' + rss.description + '</description>\n'
    buf += '  <language>' + rss.lang + '</language>\n'

    for uri in rss:
        f = rss[uri]
        from time import gmtime, strftime
        rfc822_date = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(f.date))
        buf += '  <item>\n'
        buf += '    <title>' + f.title + '</title>\n'
        buf += '    <link>'  + f.link  + '</link>\n'
        buf += '    <pubDate>' + rfc822_date + '</pubDate>\n'
        buf += '  </item>\n'

    buf += '</channel>\n'
    buf += '</rss>\n'

    return buf    

def example():
    """Example for usage."""

    # import rss
    # list = rss.RSS()
    list = RSS(encode="euc-jp", title="Example",
        parent="http://example.com/",
        uri="http://example.com/rss.xml",
        description="Example")
    list.append("a.html", title="Document", date=1108121871)
    list.append("b.txt", title="Text", date=1108121771)
    list.append("c.jpg", title="Image", date=1108111871)
    #print rss.make_rss1(list)
    print make_rss1(list)

if __name__ == "__main__":
    example()
