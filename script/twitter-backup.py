#!/usr/bin/python
'''Twitte Backup.

1. download Atom feed
2. insert updates into sqlite DB

usage: twitte-backup username [-o dbpath]
options:
    -o dbpath: sqlite DB file path. default is ./<username>.db
'''
#
# Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
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
# $Id$
#

import os.path
import re
import socket
import sqlite3
import sys
import traceback
import urllib
import xml.dom.minidom
from gzip import GzipFile
from StringIO import StringIO
from time import sleep

__version__ = '$Revision$'

FEED_PARENT_URL = 'http://twitter.com/statuses/user_timeline/'
VERSION = __version__[11:-1].strip()


class TwitterLog:
    '''Twitte Log DB Wrapper.
    '''

    def __init__(self, username, dbpath):
        self.username = username
        if os.path.isfile(dbpath):
            self.db = sqlite3.connect(dbpath)
        else:
            self.db = sqlite3.connect(dbpath)
            self.db.executescript(
                """CREATE TABLE twitterlog (
                   link PRIMARY KEY,
                   pubdate,
                   body
                   );""")
        self.db.isolation_level = None

    def insert_update(self, update):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM twitterlog WHERE link = ?;", (update['link'], ))
        if int(cursor.fetchone()[0]) > 0:
            return
        try:
            cursor.execute("INSERT INTO twitterlog (link, pubdate, body) VALUES (?, ?, ?)",
                           (update['link'],
                            update.get('updated', ''),
                            update.get('title', '')))
        except sqlite3.IntegrityError, err:
            traceback.print_exc()
        cursor.close()

    def __del__(self):
        self.db.close()

    def read_feed(self, data):
        '''Read feed string and insert updates into log DB.
        '''
        dom = xml.dom.minidom.parseString(data)
        for entry in dom.getElementsByTagName('entry'):
            update = {}
            for element in entry.childNodes:
                if element.hasChildNodes():
                    update[element.nodeName] = element.firstChild.nodeValue
                elif element.nodeName == 'link':
                    update['link'] = element.getAttribute('href')
            update['title'] = update.get('title', '').replace(self.username + ': ', '', 1)
            if ('link' in update) and update['link']:
                self.insert_update(update)

# End of TwitterLog


def load_options():
    username = None
    dbpath = None
    feedurl = None

    argv = sys.argv[1:]
    while argv:
        a = argv.pop(0)
        if a == '-o':
            dbpath = argv.pop(0)
        elif a == '--test':
            _test()
            sys.exit()
        else:
            username = a
    if username is None:
        sys.exit('usage: twitte-backup username [-o dbpath]')
    if dbpath is None:
        dbpath = './%s.db' % username
    feedurl = '%s%s.atom' % (FEED_PARENT_URL, username)

    return username, dbpath, feedurl

def get_feed(url):
    agent = urllib.FancyURLopener()
    agent.addheaders = []
    agent.addheaders.append(('User-Agent', 'Twitte-Backup/' + VERSION))
    agent.addheaders.append(('Accept-Encoding', 'gzip'))
    socket.setdefaulttimeout(10)
    for i in range(5):
        try:
            feed = agent.open(url).read()
        except Exception, err:
            sleep(10)
            continue
        break
    try:
       feed = GzipFile(fileobj=StringIO(feed)).read()
    except IOError:
        pass
    return feed

def _test():
    import unittest

    class TestTwitterLog(unittest.TestCase):
        def setUp(self):
            self.log = TwitterLog('test', ':memory:')
            self.xml = \
                '''<?xml version="1.0" encoding="UTF-8"?>
                   <feed xml:lang="en-US" xmlns="http://www.w3.org/2005/Atom">
                     <entry>
                       <title>test: foo</title>
                       <updated>bar</updated>
                       <link rel="alternate" type="text/html" href="hoge"/>
                     </entry>
                   </feed>'''
            self.logdata = [(u'hoge', u'bar', u'foo')]

        def testReadFeed(self):
            self.log.read_feed(self.xml)
            cursor = self.log.db.cursor()
            cursor.execute("SELECT * FROM twitterlog;")
            rows = cursor.fetchall()
            self.assertEqual(self.logdata, rows)

    suite = unittest.makeSuite(TestTwitterLog)
    unittest.TextTestRunner(verbosity=2).run(suite)
# End of _test

def main():
    username, dbpath, feedurl = load_options()
    log = TwitterLog(username, dbpath)
    feed = get_feed(feedurl)
    log.read_feed(feed)

if __name__ == '__main__':
    main()
