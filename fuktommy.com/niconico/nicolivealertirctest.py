#!/usr/bin/python
"""Unit Tests for Nico Live Alert to IRC.
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

import sqlite3
import sys
import unittest

from nicolivealertirc import Filter, Recommend


class BotMock:
    def __init__(self):
        self.queue = []

    def post(self, msg):
        self.queue.append(msg)


class FilterTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.isolation_level = None
        self.botmock = BotMock()

    def test_includes(self):
        filter = Filter(self.db).open()
        self.assertEquals(False, filter.includes('co123'))

    def test_add(self):
        filter = Filter(self.db).open()
        filter.add('co123')
        self.assertEquals(False, filter.includes('co123'))

        filter.flush_queue(self.botmock)
        self.assertEquals(True, filter.includes('co123'))
        self.assertEquals(['[add] co123'], self.botmock.queue)

    def test_open(self):
        filter = Filter(self.db).open()
        filter.add('co123')
        filter.flush_queue(self.botmock)
        self.assertEquals(True, filter.includes('co123'))

        filter = Filter(self.db).open()
        self.assertEquals(True, filter.includes('co123'))

    def test_delete(self):
        filter = Filter(self.db).open()
        filter.add('co123')
        filter.flush_queue(BotMock())
        self.assertEquals(True, filter.includes('co123'))

        filter.delete('co123')
        self.assertEquals(True, filter.includes('co123'))

        filter.flush_queue(self.botmock)
        self.assertEquals(False, filter.includes('co123'))
        self.assertEquals(['[delete] co123'], self.botmock.queue)

    def test_list(self):
        filter = Filter(self.db).open()
        filter.add('co123')
        filter.add('ch456')
        filter.flush_queue(BotMock())

        filter.list()
        filter.flush_queue(self.botmock)

        expected = [
            '[list begin]',
            '[list] co123 http://ch.nicovideo.jp/community/co123',
            '[list] ch456 http://ch.nicovideo.jp/channel/ch456',
            '[list end]',
        ]
        self.assertEquals(expected, self.botmock.queue)


class RecommendTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.isolation_level = None
        self.botmock = BotMock()

    def test_default_random_rate(self):
        recommend = Recommend(self.db).open()
        self.assertEquals(0.1, recommend.random_rate)

    def test_set_random_rate(self):
        recommend = Recommend(self.db).open()
        recommend.set_random_rate(0.5)
        self.assertEquals(0.1, recommend.random_rate)

        recommend.flush_queue(self.botmock)
        self.assertEquals(0.5, recommend.random_rate)
        self.assertEquals(['[rate] 0.500000'], self.botmock.queue)

    def test_open(self):
        recommend = Recommend(self.db).open()
        recommend.set_random_rate(0.5)
        recommend.flush_queue(self.botmock)
        self.assertEquals(0.5, recommend.random_rate)

        recommend = Recommend(self.db).open()
        self.assertEquals(0.5, recommend.random_rate)


def _main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FilterTest))
    suite.addTest(unittest.makeSuite(RecommendTest))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.errors or result.failures:
        sys.exit(1)
    else:
        sys.exit()


if __name__ == '__main__':
    _main()
