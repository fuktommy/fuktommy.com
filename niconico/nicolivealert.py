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
        if (event['communityid'] not in my_favorite_communities)
           and (event['userid'] not in my_favorite_users):
            continue
        print event['url'], event['communityname'], event['title']
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
import time
import urllib
import xml.dom.minidom


__version__ = "$Revision$"
__all__ = ['MessageEvent', 'StreamEvent', 'connect']

GET_ALERT_INFO = 'http://live.nicovideo.jp/api/getalertinfo'
GET_STREAM_INFO = 'http://live.nicovideo.jp/api/getstreaminfo/lv'
WATCH_PAGE = 'http://live.nicovideo.jp/watch/lv'
VERSION = __version__[11:-1].strip()

socket.setdefaulttimeout(10)


class Agent:
    """Web XML API client.
    """
    def __init__(self):
        self.agent = urllib.URLopener()
        self.agent.addheaders = [
            ('User-Agent', 'nicolivealert.py/' + VERSION)]
        self.last_fail = 0

    def reset(self):
        self.last_fail = 0

    def is_busy(self):
        return self.last_fail + 60 > time.time()

    def fetch(self, url):
        if self.is_busy():
            return None
        try:
            response = self.agent.open(url).read()
            dom = xml.dom.minidom.parseString(response)
        except:
            self.last_fail = time.time()
            return None
        if dom.getElementsByTagName('error'):
            self.last_fail = time.time()
            return None
        return dom


def xml_get_string(dom, tagname):
    try:
        return dom.getElementsByTagName(tagname)[0].lastChild.nodeValue
    except:
        return ''


class Event:
    """Event includes streaming information or client message.
    """
    is_new_stream = False
    is_message = False
    message = ''


class MessageEvent(Event):
    """Event for system message.

    connect, close, and so on.
    """

    is_message = True

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class StreamEvent(Event):
    """Event for new streaming start.

    Elements:
        without stream Info API:
            streamid, communityid, userid, url
        with stream Info API:
            title, description, provider_type, communityname, thumbnail
    """

    is_new_stream = True

    def __init__(self, comment, stream_info):
        self.info = {}
        self.stream_info = None
        self.comment = comment
        self.stream_info = stream_info

    def __str__(self):
        self.fetch()
        ret = dict(self.comment)
        ret.update(self.info)
        return str(ret)

    def fetch(self):
        if self.info:
            return
        self.info = self.stream_info.get_info(self.comment['streamid'])

    def get(self, key, default = None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        method = 'get_' + key
        if hasattr(self, method):
            return getattr(self, method)()
        if key in self.comment:
            return self.comment[key]
        self.fetch()
        return self.info[key]

    def get_url(self):
        return '%s%d?alert=1' % (WATCH_PAGE, self.comment['streamid'])


class AlertInfoApi:
    """API for information of comment server.
    """

    def __init__(self, agent):
        self.agent = agent

    def get_info(self):
        """Get nformation of comment server as a dictionary.
        """
        dom = self.agent.fetch(GET_ALERT_INFO)
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
        self.socket.settimeout(30)
        self.socket.connect((self.addr, self.port))
        msg = ('<thread thread="%d" version="20061206" res_from="-1"/>\0'
               % self.thread)
        self.socket.sendall(msg)

    def __iter__(self):
        self.close()
        self.connect()
        buf = ''
        while self.processing:
            try:
                buf += self.socket.recv(1024)
            except socket.timeout:
                break
            found = re.search(r'<chat.*?>(\d+),(\w+),(\d+)</chat>', buf)
            if not found:
                continue
            buf = buf[found.end():]
            yield {
                'streamid': int(found.group(1)),
                'communityid': found.group(2),
                'userid': int(found.group(3)),
            }


class StreamInfoApi:
    """API for streaming information.
    """

    def __init__(self, agent):
        self.agent = agent

    def get_info(self, streamid):
        url = '%s%d' % (GET_STREAM_INFO, streamid)
        dom = self.agent.fetch(url)
        return {
            'title': xml_get_string(dom, 'title'),
            'description': xml_get_string(dom, 'description'),
            'provider_type': xml_get_string(dom, 'provider_type'),
            'communityname': xml_get_string(dom, 'name'),
            'thumbnail': xml_get_string(dom, 'thumbnail'),
        }


class Connection:
    """Nico live alert connection.
    """

    def __init__(self):
        self.agent = Agent()
        self.alert_info = AlertInfoApi(self.agent)
        self.stream_info = StreamInfoApi(self.agent)
        self.comment_server = None
        self.processing = False
        self.to_reconnect = False

    def close(self):
        self.processing = False
        self.to_reconnect = False
        if self.comment_server:
            self.comment_server.close()
            self.comment_server = None

    def connect(self):
        self.processing = True
        self.to_reconnect = False
        self.agent.reset()
        info = self.alert_info.get_info()
        self.comment_server = CommentServerApi(info)

    def reconnect(self):
        self.to_reconnect = True

    def __iter__(self):
        self.processing = True
        while self.processing:
            time.sleep(1)
            self.close()
            self.connect()
            yield MessageEvent('[connect]')
            for comment in self.comment_server:
                if self.to_reconnect or self.agent.is_busy():
                    break
                yield StreamEvent(comment, self.stream_info)
            yield MessageEvent('[close]')


def connect():
    """Connect to Nico Live alert API.
    """
    return Connection()


def _print_event(event, encoding):
    """Usage sample.
    """
    if not event.is_new_stream:
        print event
        return
    tmp = []
    for key in ('url', 'communityname', 'title'):
        tmp.append(event[key].encode(encoding, 'replace'))
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
