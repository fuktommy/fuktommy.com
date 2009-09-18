"""Nico Live Alert.

A client for Nico Live new streaming alert API.

See:
    http://live.nicovideo.jp/alert/
    http://dic.nicovideo.jp/a/%E3%83%8B%E3%82%B3%E7%94%9F%E3%82%A2%E3%83%A9%E3%83%BC%E3%83%88(%E6%9C%AC%E5%AE%B6)%E3%81%AE%E4%BB%95%E6%A7%98

Usage:
    alert = nicolivealert.connect()
    for event in alert:
        if not event.is_new_stream:
            continue
        info = event.stream_info
        print info['url'], info['communityname'], info['title']
        if some_condition:
            alert.close()
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

import re
import socket
import urllib
import xml.dom.minidom


__version__ = "$Revision$"
__all__ = ['connect']

GET_ALERT_INFO = 'http://live.nicovideo.jp/api/getalertinfo'
GET_STREAM_INFO = 'http://live.nicovideo.jp/api/getstreaminfo/lv'
WATCH_PAGE = 'http://live.nicovideo.jp/watch/lv'
VERSION = __version__[11:-1].strip()


def get_url_opener():
    agent = urllib.URLopener()
    agent.addheaders = []
    agent.addheaders.append(('User-Agent', 'nicolivealert.py/' + VERSION))
    return agent


def xml_get_string(dom, tagname):
    array = dom.getElementsByTagName(tagname)
    if len(array) > 0:
        return array[0].lastChild.nodeValue
    else:
        return ''


class Event:
    """Event includes streaming information or client message.
    """
    is_new_stream = False
    is_message = False
    stream_info = {}
    client_message = ''

    def __str__(self):
        if self.is_new_stream:
            return self.stream_info
        else:
            return self.client_message


def get_client_event(message):
    event = Event()
    event.is_message = True
    event.client_message = message
    return event


def get_stream_event(info):
    event = Event()
    event.is_new_stream = True
    event.stream_info = info
    return event


class AlertInfoApi:
    """API for information of comment server.
    """

    def __init__(self, agent):
        self.agent = agent

    def get_info(self):
        """Get nformation of comment server as a dictionary.
        """
        response = self.agent.open(GET_ALERT_INFO).read()
        dom = xml.dom.minidom.parseString(response)
        return {
            'addr': xml_get_string(dom, 'addr'),
            'port': int(xml_get_string(dom, 'port')),
            'thread': int(xml_get_string(dom, 'thread')),
        }


class CommentServerApi:
    """XMLSocket server pushing new streaming alert.
    """

    def __init__(self, options):
        self.addr = options['addr']
        self.port = options['port']
        self.thread = options['thread']
        self.socket = None
        self.processing = False

    def close(self):
        self.processing = False
        if self.socket:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = None

    def connect(self):
        self.processing = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.addr, self.port))
        msg = ('<thread thread="%d" version="20061206" res_from="-1"/>\0'
               % self.thread)
        self.socket.sendall(msg)

    def __iter__(self):
        self.close()
        self.connect()
        buf = ''
        while self.processing:
            buf += self.socket.recv(1024)
            found = re.search(r'<chat.*?>(\d+),.*?</chat>', buf)
            if not found:
                continue
            buf = buf[found.end():]
            yield int(found.group(1))


class StreamInfoApi:
    """API for streaming information.
    """

    def __init__(self, agent):
        self.agent = agent

    def get_info(self, streamid):
        url = '%s%d' % (GET_STREAM_INFO, streamid)
        response = self.agent.open(url).read()
        dom = xml.dom.minidom.parseString(response)
        return {
            'url': '%s%d' % (WATCH_PAGE, streamid),
            'title': xml_get_string(dom, 'title'),
            'communityname': xml_get_string(dom, 'name'),
        }


class Connection:
    """Nico live alert connection.
    """

    def __init__(self):
        self.agent = get_url_opener()
        self.alert_info = AlertInfoApi(self.agent)
        self.stream_info = StreamInfoApi(self.agent)
        self.comment_server = None
        self.processing = False

    def close(self):
        self.processing = False
        if self.comment_server:
            self.comment_server.close()
            self.comment_server = None

    def connect(self):
        self.processing = True
        info = self.alert_info.get_info()
        self.comment_server = CommentServerApi(info)

    def __iter__(self):
        self.close()
        self.connect()
        while self.processing:
            self.connect()
            yield get_client_event('[connect]')
            for streamid in self.comment_server:
                info = self.stream_info.get_info(streamid)
                yield get_stream_event(info)
            self.close()
            yield get_client_event('[close]')


def connect():
    """Connect to Nico Live alert API.
    """
    return Connection()


def _print_event(event, encoding):
    if not event.is_new_stream:
        print event
        return
    info = event.stream_info
    tmp = []
    for key in ('url', 'communityname', 'title'):
        tmp.append(info.get(key, '').encode(encoding, 'replace'))
    print ' || '.join(tmp)


def _main():
    """Usage sample.
    """
    alert = connect()
    try:
        for event in alert:
            _print_event(event, 'shift_jis')
    except KeyboardInterrupt:
        alert.close()


if __name__ == '__main__':
    _main()
