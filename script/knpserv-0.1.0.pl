#!/usr/local/bin/perl
#
# KNPサーバ
# 形態素解析器JUMAN(http://www.kc.t.u-tokyo.ac.jp/nl-resource/)や
# 構文解析器KNP(http://www.kc.t.u-tokyo.ac.jp/nl-resource/knp.html)は
# 起動時にデータを読み込むため、あまり頻繁に起動すると時間がかかります。
# しかしシステムを作るには1文ずつ解析を行なった方がやりやすいこともあります。
# そのためこんなものを作りました。
# 社説記事を1文につき2回ずつ解析したとき、
# 1回ごとにJUMAN, KNPを起動するのに比べ、実行時間が約1/10になりました。
#
# Copyright (c) 2003 Satoshi Fukutomi <info@fuktommy.com>.
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
use Socket;
use IPC::Open2;

$port = 5000;
$SIG{PIPE} = "IGNORE";

socket CLIENT_WAITING, PF_INET, SOCK_STREAM, 0 or die;
setsockopt CLIENT_WAITING, SOL_SOCKET, SO_REUSEADDR, 1 or die;
bind CLIENT_WAITING, pack_sockaddr_in($port, INADDR_ANY) or die;
listen CLIENT_WAITING, SOMAXCONN or die;

open2(JUMAN_IN, JUMAN_OUT, 'juman', '-e', '-B');
open2(KNP_IN,   KNP_OUT,   'knp',   '-sexp');

while (1) {
	accept CLIENT, CLIENT_WAITING;
	select CLIENT; $|=1;

	$_ = <CLIENT>;
	print JUMAN_OUT $_;
	my @juman = ();
	while (<JUMAN_IN>) {
		push @juman, $_;
		last if (/^EOS/);
	}

	print KNP_OUT @juman;
	my @knp = ();
	while (<KNP_IN>) {
		push @knp, $_;
		last if (/^EOS/);
	}

	print CLIENT @knp;
	shutdown CLIENT, 2;
	close CLIENT;
}
