#!/usr/local/bin/python
# -*- coding: euc-jp -*-
#
# csvファイルをテキストまたはHTMLに変換する
#
# 使用法: $0 [-d整数] [-t/-h]
# オプション:
# 	-d整数:	テキスト形式での列幅
# 	-t:	テキスト形式で出力
# 	-h:	HTML形式で出力
#
# Copyright (c) 2004-2005 Satoshi Fukutomi <info@fuktommy.com>.
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

import csv
import fileinput
import re
import sys

block  = 10
mode   = "text"
encode = "euc-jp"
mail   = "fuktommy@inter7.jp"
files  = []

#
# HTML
#
def printHtmlHeader():
	buf = "<?xml version='1.0' encoding='" + encode + "'?>\n" +\
	      "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'\n" +\
	      "  'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n" +\
	      "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='ja'>\n" +\
	      "<head>\n" +\
	      "<title>cvs</title>\n" +\
	      "  <link rev='made' href='mailto:" + mail + "' />\n" +\
	      "  <link rel='contents' href='#' />\n" +\
	      "  <style type='text/css'>\n" +\
	      "     h1 { text-align: center }\n" +\
	      "     a { text-decoration: none }\n" +\
	      "     address { text-align: right; font-style: normal }\n" +\
	      "     p.date { text-align: right }\n" +\
	      "     td { text-align: right; border: thin solid black }\n" +\
	      "     table { border: thin solid black; border-collapse: collapse}\n" +\
	      "  </style>\n" +\
	      "</head>\n" +\
	      "<body>\n" +\
	      "<table summary='cvs'>\n"
	sys.stdout.write(buf)

#
# HTML
#
def printHtmlFooter():
	sys.stdout.write("</table>\n</body>\n</html>\n")

#
# メイン
#

blocksize = re.compile(r"^-d(\d+)")
textmode  = re.compile(r"-t")
htmlmode  = re.compile(r"-h")
sys.argv.pop(0)
for i in sys.argv:
	bs = blocksize.search(i)
	if bs != None:
		block = int(bs.group(1))
	elif textmode.search(i):
		mode = "text"
	elif htmlmode.search(i):
		mode = "html"
	else:
		files.append(i)

reader = csv.reader(fileinput.input(files))

if mode == "html":
	printHtmlHeader()
	rows = []
	max  = 0
	for row in reader:
		rows.append(row)
		if max < len(row):
			max = len(row)
	for row in rows:
		sys.stdout.write("<tr>")
		while len(row) < max:
			row.append("")
		for c in row:
			sys.stdout.write("<td>" + c + "</td>")
		sys.stdout.write("</tr>\n")
	printHtmlFooter()
else:
	for row in reader:
		for c in row:
			sys.stdout.write("% *s" % (block, c))
		print
