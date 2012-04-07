#!/usr/bin/python
#
# save logs to /PATH/TO/LOG_DIR/%Y-%m-%d
#
# usage: your_program | this_script log_dir
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

import os
#import os.path
import sys
import time

# args
log_dir = ""
if len(sys.argv) == 2:
	log_dir = sys.argv[1]
else:
	sys.exit("usage: " + sys.argv[0] + " log_dir")

# log directody
if not os.path.isdir(log_dir):
	ok = os.mkdir(log_dir)
if not (os.path.isdir(log_dir) and os.access(log_dir, os.W_OK)):
	sys.exit(log_dir + ": not writable")

sys.stdout.close()
sys.stderr.close()

# main loop
log = ""
opened = False
while True:
	line = sys.stdin.readline()
	if line == "":
		break
	new_log = log_dir + "/" + time.strftime("%Y-%m-%d", time.localtime())
	if log != new_log:
		if opened:
			f.close()
		else:
			opened = True
		log = new_log
		f = open(log, "a")
	f.write(line)
	f.flush()
f.close()
