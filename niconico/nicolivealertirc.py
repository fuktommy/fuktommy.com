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
    encoding = 'utf8'
    filter = None
    recommend = None
    alert = None
    actions = [
        'add',
        'delete',
        'list',
        'rate_set',
        'rate_show',
        'reconnect',
        'help',
    ]

    def on_welcome(self, irc, e):
        irc.join(self.channel)
        self.post("Hi. I'm Nico Live Alert Bot.")

    def on_pubmsg(self, irc, e):
        try:
            msg = e.arguments()[0]
            for act in self.actions:
                if getattr(self, 'do_' + act)(msg):
                    return
        except:
            self.post('[error]')
            traceback.print_exc()

    def do_add(self, msg):
        found = re.search(r'^add\s+(c[ho]\d+)', msg)
        if not found:
            return False
        self.filter.add(found.group(1))
        return True

    def do_delete(self, msg):
        found = re.search(r'^delete\s+(c[ho]\d+)', msg)
        if not found:
            return False
        self.filter.delete(found.group(1))
        return True

    def do_list(self, msg):
        found = re.search(r'^list', msg)
        if not found:
            return False
        self.filter.list()
        return True

    def do_rate_set(self, msg):
        found = re.search(r'^rate\s+(\d+[.]\d+)', msg)
        if not found:
            return False
        self.recommend.set_random_rate(float(found.group(1)))
        return True

    def do_rate_show(self, msg):
        if msg != 'rate':
            return False
        self.post('[rate] %f' % self.recommend.random_rate)

    def do_reconnect(self, msg):
        if msg != 'reconnect':
            return False
        self.alert.reconnect()

    def do_help(self, msg):
        if msg != 'help':
            return False
        self.post('[help begin]')
        self.post('[help] random recommend rate is %f'
                  % self.recommend.random_rate)
        self.post('[help] "list" to list community id filter')
        self.post('[help] "add co123" to add community id to filter')
        self.post('[help] "delete co123" to delete community id from filter')
        self.post('[help] "rate 0.5" to set random recommend rate')
        self.post('[help] "reconnect" to reconnect')
        self.post('[help end]')

    def post(self, message):
        """Post message.
        """
        self.connection.notice(
            self.channel,
            message.encode(self.encoding, 'replace'))
        time.sleep(0.5)

    def post_event(self, event):
        """Post Nico Live Alert event.
        """
        if not event.is_new_stream:
            self.post(str(event))
            return
        self.post('%s %s from %s' %
                  (event['url'], event['title'], event['communityname']))


def table_exists(db, table):
    cursor = db.cursor()
    cursor.execute(
        '''SELECT COUNT(*) FROM `sqlite_master`
             WHERE `type` = 'table' AND `name` = ?;''',
        (table,))
    return int(cursor.fetchone()[0]) > 0


class Filter:
    """Commmunity ID filter using SQLite DB.
    """

    def __init__(self, db):
        self.db = db
        self.add_queue = []
        self.delete_queue = []
        self.list_queue = False

    def open(self):
        if table_exists(self.db, 'filter'):
            return self
        self.db.executescript(
            '''CREATE TABLE `filter` (
                 `id` PRIMARY KEY,
                 `update_time`
               );''')
        return self

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
                list_thread = Thread(target=self.post_list,
                                     args=(bot, self.list_table()))
                list_thread.setDaemon(True)
                list_thread.start()
        except:
            bot.post('[error]')
            traceback.print_exc()

    def post_list(self, bot, lines):
        bot.post('[list begin]')
        for line in lines:
            bot.post(line)
        bot.post('[list end]')

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

    def list_table(self):
        ret = []
        cursor = self.db.cursor()
        cursor.execute("SELECT `id` FROM `filter`")
        for row in cursor:
            communityid = row[0]
            if communityid.startswith('ch'):
                url = 'http://ch.nicovideo.jp/channel/'
            else:
                url = 'http://ch.nicovideo.jp/community/'
            ret.append('[list] %s %s%s' % (communityid, url, communityid))
        return ret


class Recommend:
    """Recommend rule.
    """

    def __init__(self, db):
        self.db = db
        self.new_rate = None
        self.random_rate = None

    def open(self):
        self.create_table()
        self.read_random_rate()
        if self.random_rate is None:
            self.create_random_rate()
        return self

    def create_table(self):
        if table_exists(self.db, 'recommend'):
            return
        self.db.executescript(
            '''CREATE TABLE `recommend` (
                 `key` PRIMARY KEY,
                 `value`
               );''')

    def create_random_rate(self):
        self.random_rate = 0.1
        self.db.cursor().execute(
            '''INSERT INTO `recommend` (`key`, `value`)
                 VALUES ('random', ?)''',
            (self.random_rate, ))

    def read_random_rate(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT `value` FROM `recommend` WHERE `key` = 'random';")
        rows = cursor.fetchall()
        if rows:
            self.random_rate = float(rows[0][0])
        else:
            self.random_rate = None

    def set_random_rate(self, rate):
        self.new_rate = rate

    def flush_queue(self, bot):
        try:
            if self.new_rate is not None:
                self.store_rate(self.new_rate)
                self.random_rate = self.new_rate
                bot.post('[rate] %f' % self.new_rate)
                self.new_rate = None
        except:
            bot.post('[error]')
            traceback.print_exc()

    def store_rate(self, rate):
        self.db.cursor().execute(
            "UPDATE `recommend` SET `value` = ? WHERE `key` = 'random'",
            (rate,))


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
    parser.add_option('-d', '--db', dest='dbpath', metavar='PATH',
                      default=':memory:', help='sqlite db')
    return parser.parse_args()


def event_is_to_post(event, filter, rate):
    if not event.is_new_stream:
        return True
    if event['communityid'] == 'official':
        return True
    if filter.includes(event['communityid']):
        return True
    if random.random() <= rate:
        return True
    return False


def main():
    options, argv = parse_args()

    db = sqlite3.connect(options.dbpath)
    db.isolation_level = None

    filter = Filter(db)
    filter.open()

    recommend = Recommend(db)
    recommend.open()

    bot = NicoAlertIRCBot(
            [(options.server, options.port)],
            options.nick,
            options.real)
    bot.channel = options.channel
    bot.encoding = options.encoding
    bot.filter = filter
    bot.recommend = recommend

    bot_thread = Thread(target=bot.start)
    bot_thread.setDaemon(True)
    bot_thread.start()

    time.sleep(1)
    alert = nicolivealert.connect()
    bot.alert = alert
    try:
        for event in alert:
            filter.flush_queue(bot)
            recommend.flush_queue(bot)
            if event_is_to_post(event, filter, recommend.random_rate):
                post_thread = Thread(target=bot.post_event, args=(event,))
                post_thread.setDaemon(True)
                post_thread.start()
    except KeyboardInterrupt:
        pass

    alert.close()
    bot.disconnect('bye')


if __name__ == '__main__':
    main()
