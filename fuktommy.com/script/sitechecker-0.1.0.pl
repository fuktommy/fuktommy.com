#!/usr/bin/perl -w
#
# 記録と異なっているサイトを表示する。
# WWWCの劣化版(WWWCは使ったことないけど)
#
# Copyright (c) Satoshi Fukutomi <info@fuktommy.com>.
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

$AGENT = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)";
$LIST  = "$ENV{HOME}/.site-checker/list";
$CACHE = "$ENV{HOME}/.site-checker/cache";

open IN, $LIST or die "$LIST: open failed. $!";
print "<html><head><title>NEW</title></head><body><ul>\n";
while (<IN>) {
	chomp;
	next if (/^#|^$/);
	($title, $uri) = split /<>/, $_, 2;
	$cache = readHTML($uri);
	system "wget", "-U", $AGENT, "-x", "-T", 10, "-t", 2,
	       "--referer=$uri", 
	       "-Y", "off", "-N", "-P", $CACHE, $uri;
	$new = readHTML($uri);
	if ($cache ne $new) {
		print "<li><a href=\"$uri\">$title</a><\li>\n";
	}
}
print "</ul></body></html>\n";
close IN;

#
# HTMLを読み込む
#
sub readHTML {
	my($uri) = $_;
	my $file = $uri;
	$file =~ s|^.*?://||;
	$file = "$CACHE/$file";
	$file .= "index.html" if ($file =~ m|/$|);
	my $buf = "";
	if (open CACHE, $file) {
		my @buf = <CACHE>;
		close CACHE;
		$buf = join "", @buf;
		$buf =~ s/\s//g;
		$buf =~ s/<[^>]*>//g;
	}
	return $buf;
}
