#!/usr/bin/perl -w
#
# ハッシュサーバ
#
# 「キー→データ」のデータベースをメモリ上に読み込んでおき、
# TCP経由で問い合わせに答える、簡易的なデータベースサーバ
#
# 使用法: $0 [-p ポート番号] [-s 区切り文字列] ファイル名...
#
# このフロントエンドがHashServ.pm
# 1つのキーに対して複数の値があってよい
#
# ポート番号のデフォルトは 8000
# 区切り文字列のデフォルトは 1つ以上のタブ文字 (\t+)
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
# 2004-09-29	0.1-beta6	おまじない
# 2004-09-21	0.1-beta5	おまじない
# 2004-08-30	0.1-beta4	シグナルのバグ修正
# 2004-08-30	0.1-beta3	セッションを保つ
# 2004-06-02	0.1-beta2	一般化するため配列を返す
# 2004-06-02	0.1-beta1
#
use strict;
use Socket;

my $port = 5000;
my $separater = "\t+";
$SIG{CHLD} = "IGNORE";

my @file = ();
while (@ARGV) {
	$_ = shift @ARGV;
	if ($_ eq "-p") {
		$port = shift @ARGV;
	} elsif ($_ eq "-s") {
		$separater = shift @ARGV;
	} else {
		push @file, $_;
	}
}
die "usage: $0 [-p port] [-s separater] file...\n" unless (@file);
@ARGV = @file;

socket CLIENT_WAITING, PF_INET, SOCK_STREAM, 0 or die;
setsockopt CLIENT_WAITING, SOL_SOCKET, SO_REUSEADDR, 1 or die;
bind CLIENT_WAITING, pack_sockaddr_in($port, INADDR_ANY) or die;
listen CLIENT_WAITING, SOMAXCONN or die;

my %hash = ();
while (<>) {
	chomp;
	@_ = split /$separater/, $_, 2;
	unless (defined $hash{$_[0]}) {
		$hash{$_[0]} = [];
	}
	push @{$hash{$_[0]}}, $_[1];
}

while (1) {
	accept CLIENT, CLIENT_WAITING;
	select CLIENT; $|=1;

	if (fork) {
		close CLIENT;
		next;

	} else {
		$SIG{ALRM} = sub {kill "TERM", $$; die};
		alarm 600;
		while (<CLIENT>) {
			s/[\r\n]//g;
			if ($_ eq 0xFF) {
				last;
			} elsif (defined $hash{$_}) {
				my $a;
				foreach $a (@{$hash{$_}}) {
					print CLIENT $a, "\n";
				}
			}
			print "\n";
			alarm 600;
		}
		shutdown CLIENT, 2;
		close CLIENT;
		kill "TERM", $$;
		exit;
	}
}
