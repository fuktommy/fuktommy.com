#!/usr/local/bin/python
# -*- coding: euc-jp -*-
#
"""�֤��äĤ��֥���

����CGI�����֤�������Ǥ��ʤ��Υ����Ȥ��֥��ˤʤ�ޤ���
�ɤΥڡ�������ƤӽФ��줿�����ե����Ȥäƴ�������
���Υڡ����ؤΥ����Ȥ�ȥ�å��Хå�������դ��ޤ���

���ּ��:
    ���Υ�����ץȤ�������ܤ��ѹ����롣
    CGI�򥵡��Ф����֤��롣
    data_path�ǻ��ꤷ���ǥ��쥯�ȥ�˽񤭹����褦�ˤ��롣
    ��HTML����CGI�˥�󥯤�ĥ�롣
    �����ԥ⡼��(�ѥ���ɤ϶�)�ǿ������ѥ���ɤ����ꤹ�롣
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
from Cookie import SimpleCookie
from time import time, localtime, gmtime, strftime
from urllib import quote, unquote
from urlparse import urljoin
try:
    import fcntl
except ImportError:
    fcntl = None

#
# ����
#
your_site = "http://localhost:8000/"        # ���ʤ��Υ�����
self_url = "/blog/"                         # ����CGI�Υѥ�
your_css = "/common.css"                    # "" �ʤ�Ȥ�ʤ�
your_rss = "/rss.rdf"                       # "" �ʤ�Ȥ�ʤ�
data_dir = "/tmp/data"                      # �ǡ�������¸������

def header(title="", url="", cookie=None):
    """�إå�����ϡ�

    title��url�Τɤ��餫����ꡣ
    """
    print 'Content-Type: text/html; charset=euc-jp'
    if cookie:
        print cookie
    print
    print '<?xml version="1.0" encoding="euc-jp"?>'
    print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"'
    print '  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
    print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja">'
    print '<head>'
    if title:
        print '<title>%s</title>' % title
    elif url:
        print '<title>%s �ؤΥ�����</title>' % url
    else:
        print '<title>���äĤ��֥�</title>'
    print '  <link rev="made" href="%s" />' % your_site
    print '  <link rel="contents" href="%s" />' % your_site
    print '  <meta name="robots" content="NOINDEX" />'
    if your_css:
        print '  <link rel="stylesheet" type="text/css" href="%s" />' % \
              your_css
    if your_rss:
        print '  <link rel="alternate" type="application/rss+xml"', \
              'title="RSS" href="%s" />' % your_rss
    print '</head>'
    print '<body>'
    if title:
        print '<h1>%s</h1>' % title
    elif url:
        print '<h1><a href="%s">%s</a> �ؤΥ�����</h1>' % (url, url)
    else:
        print '<h1>���äĤ��֥�</h1>'

def footer(cookie=None, url=""):
    if not cookie:
        cookie = readcookie()
    sid = cookie.get("sid", "")
    if sid:
        passwd = Password()
        sid_ok = passwd.check(sid=sid)
    else:
        sid_ok = False
    print '<form method="post" action="%s"><p>' % self_url
    if not sid_ok:
        print '<input type="password" name="passwd" value=""', \
              'tabindex="3" accesskey="p">'
    print '<input type="submit" name="admin" value="�����ԥ⡼��"', \
          'tabindex="4" accesskey="a" />'
    print '<input type="hidden" name="mode" value="list" />'
    print '</p></form>'
    if url:
        print '<form method="post" action="%s"><p>' % self_url
        if not sid_ok:
            print '<input type="password" name="passwd" value=""', \
                  'tabindex="3" accesskey="p">'
        print '<input type="submit" name="admin" value="���Υڡ��������"', \
              'tabindex="4" accesskey="a" />'
        print '<input type="hidden" name="url" value="%s" />' % url
        print '<input type="hidden" name="mode" value="list" />'
        print '</p></form>'
    print '<p>Powered by <a href="http://fuktommy.xrea.jp/quickblog/">���äĤ��֥�</a>.</p>'
    print '</body>'
    print '</html>'

def jump(url):
    header("jump")
    next = "%s?%s" % (self_url, url)
    print '<p>Click and jump to <a href="%s">%s</a></p>' % (next, next)
    print '<script type="text/javascript">'
    print '  window.location.href = "%s";</script>' % next
    footer()

def xmlresponce(ok):
    print 'Content-Type: text/xml; encoding=utf-8'
    print
    print '<?xml version="1.0"?>',
    print '<response>';
    if ok:
        print '  <error>0</error>'
    else:
        print '  <error>1</error>'
        print '  <message>Error</message>'
    print '</response>'


class Lock:
    def __init__(self):
        self.fp = None
        if fcntl:
            self.fp = file(os.path.join(data_dir, "lock"), "w")
            fcntl.lockf(self.fp, fcntl.LOCK_EX)

    def unlock(self):
        if self.fp:
            fcntl.lockf(self.fp, fcntl.LOCK_UN)
            self.fp.close()
            self.fp = None


class Comment:
    """�����Ȥ���¸���Ƥ���ե����롣"""

    def __init__(self, id="", url=""):
        """���󥹥ȥ饯����

        id��url�ΰ�������ꤹ�롣
        id�ʤ�ե�������ɤ߹��ࡣ
        """
        if id:
            self.id = id
            self.path = os.path.join(data_dir, self.id)
            self.read()
        elif url:
            self.id = md5.new(url).hexdigest()
            self.path = os.path.join(data_dir, self.id)
            if os.path.exists(self.path):
                self.read()
            else:
                self.url = url
                self.data = [url+"\n"]

    def read(self):
        try:
            f = file(self.path)
            self.data = f.readlines()
            f.close()
            self.url = self.data[0].strip()
        except IOError, IndexError:
            self.data = []
            self.url = ""

    def sync(self):
        """�ǡ�������¸��"""
        lock = Lock()
        f = file(self.path, "wb")
        for line in self.data:
            f.write(line)
        f.close()
        lock.unlock()

    def remove(self):
        try:
            os.remove(self.path)
        except OSError:
            pass


class Password:
    """�ѥ���ɡ�"""

    def __init__(self, passwd=""):
        self.path = os.path.join(data_dir, "passwd")
        if passwd:
            self.hash = md5.new(passwd).hexdigest()
        else:
            self.read()

    def read(self):
        try:
            f = file(self.path)
            self.hash = f.readline().strip()
        except IOError:
            self.hash = None

    def sync(self):
        try:
            lock = Lock()
            f = file(self.path, "w")
            f.write(self.hash + "\n")
            f.close()
            lock.unlock()
        except IOError:
            pass

    def sid(self):
        """���å����ID��

        �ѥ���ɤΥϥå�������դ������롣
        """
        date = strftime('%Y-%m-%d', localtime(time()))
        return md5.new("%s %s" % (time, self.hash)).hexdigest()

    def check(self, passwd="", sid=""):
        """�ѥ���ɤȥ��å����ID�Τɤ��餬����äƤ����OK��"""
        if not self.hash:
            return True
        elif passwd:
            newpasswd = Password(passwd)
            return newpasswd.hash == self.hash
        elif sid:
            return sid == self.sid()
        else:
            return False


def html_format(plain):
    """�ƥ����Ȣ�HTML�Ѵ���"""
    buf = plain.replace("<br>", "<br />\n")
    buf = re.sub(r"https?://[^\x00-\x20\"'()<>\[\]\x7F-\xFF]{2,}",
                 r'<a href="\g<0>">\g<0></a>',
                 buf)
    return buf

def readcookie():
    buf = os.environ.get("HTTP_COOKIE", "")
    cookie = {}
    for pair in buf.split(";"):
        try:
            key, val = pair.split("=")
            cookie[key.strip()] = unquote(val.strip())
        except ValueError:
            pass
    return cookie

def view(url):
    """�����Ȥ��ɤ���̡�"""
    url = cgi.escape(url, True)
    comment = Comment(url=url)
    header(url=url)
    for line in comment.data[1:]:
        try:
            date, message = line.strip().split("<>")
            print '<h2>%s</h2>' % \
                  strftime('%Y-%m-%d %H:%M', localtime(int(date)))
            print "<p>%s</p>" % html_format(message)
        except ValueError:
            pass
    print '<form method="post" action="%s"><p>' % self_url
    print '<textarea name="message" rows="15" cols="100"', \
          'tabindex="1" accesskey="m"></textarea><br />'
    print '<input type="submit" name="submit" value="������"', \
          'tabindex="2" accesskey="s" />'
    print '<input type="hidden" name="comment" value="%s" />' % url
    print '</p></form>'
    print '<p>�ȥ�å��Хå�URL: %s?tb=%s</p>' % \
          (urljoin(your_site, self_url), quote(url))
    print '<form method="post" action="%s"><p>' % self_url
    footer(url=url)

def post(url, form):
    """�����Ȥ�����դ��롣"""
    url = cgi.escape(url, True)
    comment = Comment(url=url)
    message = form.getfirst("message", "")
    message = cgi.escape(message, True)
    message = message.replace("\r", "").replace("\n", "<br>")
    if message:
        comment.data.append("%d<>%s\n" % (time(), message))
        comment.sync()
    jump(url)

def trackback(url, form):
    """�ȥ�å��Хå�������դ��롣"""
    url = cgi.escape(url, True)
    comment = Comment(url=url)
    blog_title = form.getfirst("title", "")
    blog_name = form.getfirst("blog_name", "")
    blog_url = form.getfirst("url", "")
    blog_excerpt = form.getfirst("excerpt", "")
    blog_charset = form.getfirst("charset", "utf-8")
    message = "%s - %s\n%s\n%s" % \
              (blog_title, blog_name, blog_url , blog_excerpt)
    message = unicode(message, blog_charset).encode("euc-jp")
    message = cgi.escape(message, True)
    message = message.replace("\r", "").replace("\n", "<br>")
    if blog_url:
        comment.data.append("%d<>%s\n" % (time(), message))
        comment.sync()
        xmlresponce(True)
    else:
        xmlresponce(False)

def listcomment():
    """�Ǽ��Ĥΰ�����"""
    comment = []
    for i in os.listdir(data_dir):
        if len(i) == 32:
            try:
                f = file(os.path.join(data_dir, i))
                url = f.readline().strip()
                import sys; sys.stderr.write(url+"\n")
                comment.append(url)
            except IOError:
                pass
    comment.sort()
    print '<ul>'
    for i in comment:
        print '  <li><a href="%s?admin=1&amp;url=%s">%s</a></li>' % \
              (self_url, i, i)
    print '</ul>'

def editcomment(url):
    """�Ǽ��Ĥ��Խ����̡�"""
    url = cgi.escape(url)
    comment = Comment(url=url)
    print '<form method="post" action="%s"><p>' % self_url
    print '<textarea name="message" rows="15" cols="100"', \
          'tabindex="1" accesskey="m">'
    for line in comment.data[1:]:
        print cgi.escape(line),
    print '</textarea><br />'
    print '<input type="submit" name="admin" value="�Խ�"', \
          'tabindex="2" accesskey="s" />'
    print '<input type="hidden" name="edit" value="%s" />' % url
    print '</p></form>'

def updatecomment(url, form):
    """�����Ȥι�����"""
    url = cgi.escape(url)
    comment = Comment(url=url)
    message = form.getfirst("message", "")
    message = message.replace("&amp;", "&")
    if message:
        comment.data = [comment.data[0]] + [message]
        comment.sync()
    else:
        comment.remove()
    jump(url)

def editpasswd():
    """�ѥ���ɹ������̡�"""
    print '<form method="post" action="%s"><p>' % self_url
    print '���ߤΥѥ����: ', \
          '<input type="password" name="passwd" value=""', \
          'tabindex="1" accesskey="p"><br />'
    print '�������ѥ����: ', \
          '<input type="password" name="newpasswd1" value=""', \
          'tabindex="2" accesskey="n"><br />'
    print '�������ѥ����(��ǧ): ', \
          '<input type="password" name="newpasswd2" value=""', \
          'tabindex="3" accesskey="m"><br />'
    print '<input type="submit" name="admin" value="�ѥ�����ѹ�"', \
          'tabindex="4" accesskey="s" />'
    print '</p></form>'

def updatepasswd(newpasswd):
    """�ѥ���ɤι�����"""
    passwd = Password(newpasswd)
    passwd.sync()
    header("�ѥ���ɤι������������ޤ�����")
    print '<p>���ä����������ѥ���ɤǴ����ԥ⡼�ɤˤʤäƤ���������</p>'
    footer()

def admin(form):
    """�����ԥ⡼�ɡ�"""
    cookie = readcookie()
    testpasswd = form.getfirst("passwd", "")
    newpasswd1 = form.getfirst("newpasswd1", "")
    newpasswd2 = form.getfirst("newpasswd1", "")
    sid = cookie.get("sid", "")
    passwd = Password()
    passwd_ok = passwd.check(passwd=testpasswd)
    sid_ok = passwd.check(sid=sid)
    if not (passwd_ok or sid_ok):
        header("�ѥ���ɤ��㤤�ޤ���")
        print '<p>�褯�Τ���Ƥ���������</p>'
        footer()
        return
    elif sid_ok:
        newcookie = None
    else:
        newcookie = SimpleCookie()
        expires = strftime("%a, %d %b %Y %H:%M:%S GMT",
                           gmtime(time() + 12*60*60))
        newcookie["sid"] = passwd.sid()
        newcookie["sid"]["expires"] = expires
    mode = form.getfirst("mode", "page")
    url = form.getfirst("url", "")
    edit = form.getfirst("edit", "")
    if edit:
        updatecomment(edit, form)
    elif url:
        header(url=url)
        print "<p>�����ԥ⡼��</p>"
        editcomment(url)
        footer()
    elif newpasswd1 and (newpasswd1 == newpasswd2):
        if passwd_ok:
            updatepasswd(newpasswd1)
        else:
            header("�ѥ���ɤ��㤤�ޤ���")
            print '<p>�褯�Τ���Ƥ���������</p>'
            footer()
    else:
        header(title="�����ԥ⡼��", cookie=newcookie)
        listcomment()
        editpasswd()
        footer(cookie=cookie)

def main():
    cmd = os.environ.get("QUERY_STRING", "")
    referer = os.environ.get("HTTP_REFERER", "")
    form = cgi.FieldStorage()
    comment = form.getfirst("comment", "")
    adminmode = form.getfirst("admin", "")
    form2 = cgi.parse_qs(cmd)
    tb = form2.get("tb", [""])[0]

    if adminmode:
        admin(form)
    elif cmd.find("://") > 0:
        view(cmd)
    elif comment:
        post(comment, form)
    elif tb:
        trackback(tb, form)
    elif referer:
        view(referer)
    else:
        header()
        print "<p>��ե��������褦�����ꤷ�Ƥ���������</p>"
        footer()

if __name__ == "__main__":
    main()
