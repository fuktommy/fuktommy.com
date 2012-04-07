#!/usr/bin/perl -w
#
# 自宅サーバをやってる人を探す
#
# 使用法: $0 list...
# listまたは標準入力から、1行1項目の、ホスト名のリストを入力する
#
# Copyright (c) 2003-2004 Satoshi Fukutomi <info@fuktommy.com>.
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
use Socket;

my $timeout = 10;
my $limit_children = 128;
my $port = 80;

select STDERR;
$| = 1;
$SIG{CHLD} = "IGNORE";

my $i = 0;
while (my $host = <>) {
	chomp $host;
	if ($i++ == $limit_children) {
		$i = 0;
		sleep $timeout;
	}
	if (fork == 0) {
		local $SIG{ALRM} = sub { print "$host ... ng\n"; exit; };
		alarm $timeout;
		my $addr = inet_aton $host;
		my $sockaddr = pack_sockaddr_in($port, $addr);
		socket SOCKET, PF_INET, SOCK_STREAM, 0;
		if (connect SOCKET, $sockaddr) {
			close SOCKET;
			print "$host ... ok\n";
			print STDOUT "http://$host:$port/\n";
		} else {
			print "$host ... ng\n";
		}
		exit;
	}
}

sleep $timeout+1;
