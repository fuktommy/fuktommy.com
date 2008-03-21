#!/usr/bin/perl -w
#
# foo.bar.1 のようなファイルを foo.1.bar にリネームする
#
# 使用法: $0 ディレクトリ名
#
# foo.bar.hoge.1 のような形式になるとお手あげ
#
# Copyright (c) 2002 Satoshi Fukutomi <info@fuktommy.com>.
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

sub myRename($$) {
	my($from, $to) = @_;
	$to =~ s/\?/_/;
	my @name = split /[.]/, $to;
	while (-e $to) {
		if (@name == 2) {
			$name[2] = $name[1];
			$name[1] = 0;
		}
		$name[1]++;
		$to = "$name[0].$name[1].$name[2]";
	}
	print "$from --> $to\n";
	rename $from, $to;
}

die "usage: $0 dir\n" unless (@ARGV == 1);
$dir = $ARGV[0];
$dir =~ s|/$||;

chdir $dir or die "$0: $dir: Cannot change directory.\n";
foreach (glob "*") {
	next unless (-f $_);
	@name = split /[.]/;
	if (@name == 1) {
		myRename $_, "$name[0].html";
	} elsif ((@name == 2) && ($name[1] =~ /^\d+$/)) {
		myRename $_, "$name[0].$name[1].html";
	} elsif ((@name == 2) && ($name[1] =~ /cgi|bbs/)) {
		myRename $_, "$name[0].html";
	} elsif ((@name == 3) && ($name[1] =~ /html|htm|cgi|bbs/)) {
		myRename $_, "$name[0].$name[2].html";
	} elsif ((@name == 3) && ($name[2] =~ /^\d+/)) {
		myRename $_, "$name[0].$name[2].$name[1]";
	}
}
