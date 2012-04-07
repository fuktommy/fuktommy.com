#!/usr/bin/python
#
"""Dynamic DNS Daemon.

Watch Router for WAN IP address.
When the IP address changes, update DDNS entries.
"""
#
# Copyright (c) 2006 Satoshi Fukutomi <info@fuktommy.com>.
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

import os
from time import sleep
from xml.sax import parse

from upnp import UPnPXMLHandler, SOAPAgent

timeout = 10
wait = 60
soapurl = "http://192.168.1.1:2869/upnp/control/WANPPPConn1"
contype = "WANPPPConnection"
updater = "/etc/init.d/ddns start"

def sendmail(msg):
    f = os.popen("/usr/sbin/sendmail root", "w")
    f.write("Subject: ddnsd notice\n")
    f.write("\n")
    f.write("%s\n" % msg)
    f.close()

def getwan():
    agent = SOAPAgent(timeout=timeout)
    xmlobject = agent.open(soapurl, contype, "GetExternalIPAddress", {})
    handler = UPnPXMLHandler(contype)
    parse(xmlobject, handler)
    xmlobject.close()
    if "wanipaddr" in handler.items:
        return handler.items["wanipaddr"]

def main():
    ipaddr = ""
    while True:
        try:
            newaddr = getwan()
            if not ipaddr:
                ipaddr = newaddr
            elif not newaddr:
                pass
            elif ipaddr != newaddr:
                code = os.system(updater)
                sendmail(newaddr)
                if code == 0:
                    ipaddr = newaddr
            print ipaddr
        except Exception, err:
            sendmail(err)
        sleep(wait)

if __name__ == "__main__":
    main()
