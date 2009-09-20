#!/usr/bin/python
"""Nico Live Alert to IRC.

Help:
    nicolivealertirc.py --help

Require:
    nicolivealert.py
    python-irclib
"""
#
# Copyright (c) 2009 Satoshi Fukutomi <info@fuktommy.com>.
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

import optparse
import os.path
import random
import re
import sqlite3
import time
import traceback
from threading import Thread

import ircbot
import irclib

import nicolivealert


__version__ = "$Revision$"
__all__ = []
VERSION = __version__[11:-1].strip()


class NicoAlertIRCBot(ircbot.SingleServerIRCBot):
    """Nico Live Alert to IRC Bot.
    """
    channel = None
    filter = None
    encoding = 'utf8'

    def on_welcome(self, irc, e):
        irc.join(self.channel)
        self.post("Hi. I'm Nico Live Alert Bot.")

    def on_pubmsg(self, irc, e):
        try:
            msg = e.arguments()[0]
            if self.do_add(msg):
                return
            if self.do_delete(msg):
                return
            if self.do_list(msg):
                return
            self.do_help(msg)
        except:
            self.post('[error]')
            traceback.print_exc()

    def do_add(self, msg):
        found = re.search(r'^add\s+(c[ho]\d+)', msg)
        if not found:
            return False
        if not self.filter:
            self.post('[error] filter is disabled')
            return True
        self.filter.add(found.group(1))
        return True

    def do_delete(self, msg):
        found = re.search(r'^delete\s+(c[ho]\d+)', msg)
        if not found:
            return False
        if not self.filter:
            self.post('[error] filter is disabled')
            return True
        self.filter.delete(found.group(1))
        return True

    def do_list(self, msg):
        found = re.search(r'^list', msg)
        if not found:
            return False
        if not self.filter:
            self.post('[error] filter is disabled')
            return True
        self.filter.list()
        return True

    def do_help(self, msg):
        if msg != 'help':
            return False
        if self.filter:
            filter_status = 'enable'
        else:
            filter_status = 'disable'
        self.post('[help] now filter is %s' % filter_status)
        self.post('[help] "list" to list community id to filter')
        self.post('[help] "add co123" to add community id to filter')
        self.post('[help] "delete co123" to delete community id from filter')

    def post(self, message):
        """Post message.
        """
        self.connection.notice(
            self.channel,
            message.encode(self.encoding, 'replace'))

    def post_event(self, event):
        """Post Nico Live Alert event.
        """
        if not event.is_new_stream:
            self.post(str(event))
            return
        self.post('%s %s from %s' %
                  (event['url'], event['title'], event['communityname']))


class Filter:
    """Commmunity ID filter using SQLite DB.
    """

    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.add_queue = []
        self.delete_queue = []
        self.list_queue = False

    def open(self):
        dbexists = os.path.isfile(self.dbpath)
        self.db = sqlite3.connect(self.dbpath)
        if not dbexists:
            self.create_table()
        self.db.isolation_level = None

    def create_table(self):
        self.db.executescript(
            '''CREATE TABLE `filter` (
                 `id` PRIMARY KEY,
                 `update_time`
               );''')

    def includes(self, id):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM `filter` WHERE `id` = ?;", (id, ))
        return int(cursor.fetchone()[0]) > 0

    def list(self):
        self.list_queue = True

    def add(self, id):
        self.add_queue.append(id)

    def delete(self, id):
        self.delete_queue.append(id)

    def flush_queue(self, bot):
        try:
            while self.delete_queue:
                id = self.delete_queue.pop(0)
                self.delet_from_table(id)
                bot.post('[delete] %s' % id)
            while self.add_queue:
                id = self.add_queue.pop(0)
                if not self.includes(id):
                    self.add_to_table(id)
                bot.post('[add] %s' % id)
            if self.list_queue:
                self.list_queue = False
                bot.post('[list begin]')
                self.list_table(bot)
                bot.post('[list end]')
        except:
            bot.post('[error]')
            traceback.print_exc()

    def add_to_table(self, id):
        cursor = self.db.cursor()
        cursor.execute(
            '''INSERT INTO `filter`
                 (`id`, `update_time`)
                 VALUES (?, DATETIME())''',
            (id, ))

    def delet_from_table(self, id):
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM `filter` WHERE `id` = ?;", (id, ))

    def list_table(self, bot):
        cursor = self.db.cursor()
        cursor.execute("SELECT `id` FROM `filter`")
        for row in cursor:
            communityid = row[0]
            if communityid.startswith('ch'):
                url = 'http://ch.nicovideo.jp/channel/'
            else:
                url = 'http://ch.nicovideo.jp/community/'
            bot.post('[list] %s %s%s' % (communityid, url, communityid))


def parse_args():
    """Parse command line argments.
    """
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-s', '--server', dest='server', default='localhost',
                      help='irc server host name')
    parser.add_option('-p', '--port', dest='port', type='int', default=6667,
                      help='irc server port')
    parser.add_option('-c', '--channel', dest='channel', default='#nicolive',
                      help='irc channel')
    parser.add_option('-n', '--nick', dest='nick', default='nicolive',
                      help='irc nickname')
    parser.add_option('-r', '--realname', dest='real',
                      default='Nico Live Alert Bot',
                      help='irc realname')
    parser.add_option('-e', '--encoding', dest='encoding', default='utf8',
                      help='irc encoding')
    parser.add_option('-f', '--filter', dest='filter',
                      help='community id filter (SQLite db)')
    parser.add_option('-R', '--random', dest='random', type='float',
                      metavar='RATE', default=0.0, help='random recommend rate')
    return parser.parse_args()


def event_is_to_post(event, filter, rate):
    if not event.is_new_stream:
        return True
    if filter and filter.includes(event['communityid']):
        return True
    if random.random() <= rate:
        return True
    return False


def main():
    options, argv = parse_args()

    filter = None
    if options.filter:
        filter = Filter(options.filter)
        filter.open()

    bot = NicoAlertIRCBot(
            [(options.server, options.port)],
            options.nick,
            options.real)
    bot.channel = options.channel
    bot.filter = filter

    bot_thread = Thread(target=bot.start)
    bot_thread.setDaemon(True)
    bot_thread.start()

    time.sleep(1)
    alert = nicolivealert.connect()
    try:
        for event in alert:
            if filter:
                filter.flush_queue(bot)
            if event_is_to_post(event, filter, options.random):
                bot.post_event(event)
    except KeyboardInterrupt:
        pass

    alert.close()
    bot.disconnect('bye')


if __name__ == '__main__':
    main()
