#
# ハッシュサーバフロントエンド
#
# 「キー→データ」のデータベースをメモリ上に読み込んでおき、
# TCP経由で問い合わせに答える、簡易的なデータベースサーバ
#
# 使用例:
#	$h = new HashServ("localhost", 5000);
#	@v =  $h->get("foo");
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
# 2004-08-30	0.1-beta4	キャッシュで高速化
# 2004-08-30	0.1-beta3	セッションを保つ
# 2004-06-02	0.1-beta2	一般化するため配列を返す
# 2004-06-02	0.1-beta1
#
package NLP::HashServ;
use strict;
use Socket;

#
# コンストラクタ
#
sub new($$$) {
	my($this, $host, $port) = @_;
	my $addr = inet_aton $host;
	my $sockaddr = pack_sockaddr_in($port, $addr);
	my $SOCKET;
	socket $SOCKET, PF_INET, SOCK_STREAM, 0;
	connect $SOCKET, $sockaddr;
	return bless {host=>$host, port=>$port, socket=>$SOCKET, cache=>{}};
}

#
# ディストラクタ
#
sub DESTORY($) {
	my($this, $key) = @_;
	my $SOCKET = $$this{socket};
	my $fd = select $SOCKET; $| = 1; select $fd;
	print $SOCKET "\xFF\n";
	close $SOCKET;
}

#
# 検索
#
sub get($$) {
	my($this, $key) = @_;
	if ($$this{cache}{$key}) {
		return @{$$this{cache}{$key}};
	}
	my $SOCKET = $$this{socket};
	my $fd = select $SOCKET; $| = 1; select $fd;
	print $SOCKET $key, "\n";
	my @buf = ();
	local $_;
	while (($_ = <$SOCKET>) ne "\n") {
		push @buf, $_;
	}
	s/[\r\n]//g foreach @buf;
	$$this{cache}{$key} = [@buf];
	return @buf;
}

1;
