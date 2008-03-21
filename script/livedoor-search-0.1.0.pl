#!/usr/bin/perl -w
#
# 乱数で語句を生成してlivedoorで検索する
#
# 1行1項目の辞書ファイルを用意し$DICで設定すること
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
use IPC::Open2;

use vars qw($GOOGLE_URI $JCODE $DIC);
$GOOGLE_URI = "http://www.google.co.jp/search";
$JCODE	    = "EUC-JP";					# 辞書の文字コード
$DIC	    = "$ENV{HOME}/work/dic.txt";		# 辞書

sub encode($) {
	my($s) = @_;
        $s =~ s|[^\w]|'%' . uc(unpack('H2', $&))|eg;
        return $s;
}

sub jump($) {
	my($str) = @_;
	$str = encode($str);
	my($IN, $OUT);
	open2($IN, $OUT, "wget", "-q", "-O", "-",
	"http://sf.livedoor.com/search?os=rss&q=$str&sf=update_date&start=0");
	close $OUT;
	print "Content-Type: text/html\n\n",
	      "<html><head><title>livedoor</title></head><body><ul>\n";
	while (<$IN>) {
		if (/rdf:resource="([^"]+)"/) {
			print "<li><a href='$1'>$1</li>\n";
		}
	}
	close $IN;
	wait;
	print "</ul></body></html>\n";
}

sub readDic() {
	open IN, $DIC or die;
	seek IN, rand(-s $DIC), 0;
	local $_ = <IN>;
	$_ = <IN>;
	chomp;
	return $_;
}

#
# メイン
#
my $str = readDic();
jump($str);
