#!/usr/bin/perl
#
# トラックバックを送る
#
# Copyright (c) 2004 Satoshi Fukutomi <info@fuktommy.com>.
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
use strict;

sub decode($) {
	my($s) = @_;
	$s =~ s/\+/ /g;
	$s =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
	return $s;
}


print "Content-Type: text/html; charset=utf-8\n\n",
      "<html><head><title>TrackBack</title></head><body>\n",
      "<form method='get' action='$ENV{SCRIPT_NAME}'><p>\n",
      "\xE3\x83\x88\xE3\x83\xA9\xE3\x83\x83\xE3\x82",
      "\xAF\xE3\x83\x90\xE3\x83\x83\xE3\x82\xAF: ",
      "<input name='url'>",
      "<input type='submit' value='SET' name='set'>",
      "</p></form>\n";

if ($ENV{QUERY_STRING} =~ /url=([^&]+)/) {
	my $url = decode($1);
	print "<form method='post' action='$url'><p>\n",
	      "$url<br>",
	      "Title: <input name='title'><br>\n",
	      "myURL: <input name='url'><br>\n",
	      "Excerpt: <input name='excerpt'><br>\n",
	      "BlogName: <input name='blog_name'><br>\n",
	      "<input type='hidden' name='charset' value='UTF-8'>",
	      "<input type='submit' value='TrackBack'>\n",
	      "</p></form>\n";
}
print "</body></html>\n";
