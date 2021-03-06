#!/usr/bin/python
#
"""Multi Wget.

If URL list has n hosts, the script exec n processes.

usage: multiwget [wget-options] [url-list-files]
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
import os
import sys
import fileinput

__version__ = "$Revision: $"

wget = ["wget", "--random-wait", "-nv",
    "--header=Accept-Encoding: gzip, compres, bzip, bzip2, deflate",
    "--header=Accept-Language: ja; q=1.0, en;q=0.5",
    "-U", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "-w", "2", "-T", "60", "-t", "2"]


class Table(dict):
    """Split URL list to hosts."""

    def append(self, url):
        found = re.search(r"([^:]+://[^:/]+(:\d+)?)", url)
        if found:
            host = found.group(1)
            if host not in self:
                self[host] = [url]
            elif url not in self[host]:
                self[host].append(url)


def main():
    opt = []
    files = []
    for i in range(1, len(sys.argv)):
        c = sys.argv[i]
        if c == "--":
            files.extend(sys.argv[i+1:])
            break
        elif c == "--help":
            sys.exit("usage: multiwget [wget-options] [url-list-files]")
        elif c.startswith("-"):
            opt.append(c)
        else:
            files.append(c)

    table = Table()
    for line in fileinput.input(files):
        table.append(line.strip())

    for host in table:
        os.spawnvp(os.P_NOWAIT,
                   wget[0],
                   wget + opt + ["--referer=%s/" % host] + table[host])


if __name__ == "__main__":
    main()
