#!/usr/bin/python
"""Nico Live Alert to IRC.

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
import time
from threading import Thread

import ircbot

import nicolivealert


__version__ = "$Revision$"
__all__ = []
VERSION = __version__[11:-1].strip()


class NicoAlertIRCBot(ircbot.SingleServerIRCBot):
    """Nico Live Alert to IRC Bot.
    """
    channel = None
    encoding = 'utf8'

    def on_welcome(self, irc, e):
        irc.join(self.channel)
        self.post("Hi. I'm Nico Live Alert Bot.")

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


class IRCBotThread(Thread):
    """IRC Connection Thread.
    """
    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run(self):
        self.bot.start()


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
    return parser.parse_args()


def main():
    options, argv = parse_args()

    bot = NicoAlertIRCBot(
            [(options.server, options.port)],
            options.nick,
            options.real)
    bot.channel = options.channel

    bot_thread = IRCBotThread(bot)
    bot_thread.setDaemon(True)
    bot_thread.start()

    time.sleep(1)
    alert = nicolivealert.connect()
    try:
        for event in alert:
            bot.post_event(event)
    except KeyboardInterrupt:
        pass

    alert.close()
    bot.disconnect('bye')


if __name__ == '__main__':
    main()
