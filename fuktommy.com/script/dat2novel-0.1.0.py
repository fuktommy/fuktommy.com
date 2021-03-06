#!/usr/bin/python
#
"""2ch dat - HTML converter.
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
import sys
import fileinput

def res_anchor(id):
    return ('<a href="#r%s" onmouseover="popupAnchor(event, \'%s\')"' + \
            ' onmouseout="hidePopup()">') % (id, id)

def escape(msg):
    msg = msg.replace("<br>", "\n")
    msg = msg.replace("&", "&amp;")
    msg = re.sub(r"&amp;(#\d+|#[Xx][0-9A-Fa-f]+|[A-Za-z0-9]+);",
                 r"&\1;",
                 msg)
    msg = msg.replace("<", "&lt;")
    msg = msg.replace(">", "&gt;")
    msg = msg.replace("\r", "")
    return msg

def format(s):
    s = s.replace("\n", "<br />\n")
    s = re.sub(r"<a.*?>|<\/a>", "", s)
    s = re.sub(r"(&gt;&gt;|>>|\201\204|\201\164|\201\342|&gt;)(\d+)",
               "%s%s</a>" % (res_anchor(r"\2"), r"\g<0>"), s)
    s = re.sub(r"https?://[\041-\073\075-\177]{2,}",
               r'<a href="\g<0>">\g<0></a>', s)
    s = re.sub(r"([^h])(ttps?://[\041-\073\075-\177]{2,})",
               r'\1<a href="h\2">\2</a>', s)
    return s


isdt = re.compile(r"^(\d+)").search
i = 0
buf = ""
sys.stdout.write('<dl>\n')
for line in fileinput.input():
    tmp = line.strip().split("<>")
    if len(tmp) >= 4:
        i += 1
        name, mail, date, message = tmp[:4]
        name = escape(name)
        mail = escape(mail)
        message = format(escape(message.strip()))
        print '  <dt id="r%d">%d :%s [%s] %s</dt>' % (i, i, name, mail, date)
        print '  <dd id="b%d">%s</dd>' % (i, message)
sys.stdout.write('</dl>\n')
