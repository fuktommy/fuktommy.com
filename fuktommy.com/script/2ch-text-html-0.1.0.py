#!/usr/bin/python

"""Tag 2ch style text.

Input:
1: foo 2005/01/02 12:34 ID:XXXXXXXX
    abc
    def

Output:
<dl>
  <dt>1: foo 2005/01/02 12:34 ID:XXXXXXXX</dt>
  <dd>bar<br />def</dd>
</dl>
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

import fileinput
import re

__version__ = "$Revision: $"

def main():
    print "<dl>"
    istitle = re.compile(r"^\d+").search
    stat = 0
    data = []
    for line in fileinput.input():
        if istitle(line):
            if data:
                print "  <dd>%s<br /><br /></dd>" % "<br />".join(data)
            data = []
            print "  <dt>%s</dt>" % line.strip()
        else:
            data.append(line.strip())
    if data:
        print "  <dd>%s</dd>" % "<br />".join(data)
    print "</dl>"

if __name__ == "__main__":
    main()
