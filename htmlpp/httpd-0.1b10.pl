#!/usr/bin/perl -w
#
# Perlで書かれた簡易的なHTTPD
#
# 使用法: $0 [-p ポート番号] [-d 公開ディレクトリ]
#
# 公開ディレクトリの下にはサブディレクトリを作ることができます。
# 拡張子がcgiのファイルがあればPerlで書かれたCGIと見なして実行します。
# ActivePerlでCGIを使うときにはCGI側に次のようなコードを入れてください。
#
# #-- ここから --#
# my %env = @ARGV;
# foreach (keys %env) {
#	$ENV{$_} = $env{$_} unless (defined $ENV{$_});
# }
# #-- ここまで --#
#
#
# 2004-06-27	0.1-beta10	HRADメソッドの処理
# 2004-06-21	0.1-beta{8,9}	パスのデコードの修正
# 2004-06-20	0.1-beta{2..7}	パスのデコードの修正
# 2004-06-12	0.1-beta1
#
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
use Socket;
use IPC::Open2;

#
# 設定
#
my $port	= 8080;
my $timeout	= 30;		# 秒
my $bufsize	= 8192;		# バイト
my $docroot	= ".";
my $resolv	= 0;
my $version	= "0.1-beta10";
my $childrenLimit = 10;

#
# 引数の処理
#
while (@ARGV) {
	$_ = shift @ARGV;
	if ($_ eq "-d") {
		$docroot = shift @ARGV;
	} elsif ($_ eq "-p") {
		$port = shift @ARGV;
	}
}

#
# 環境変数
#
$ENV{SERVER_SOFTWARE}	= "httpd.pl/$version";
$ENV{GATEWAY_INTERFACE} = "CGI/1.1";
$ENV{SERVER_PROTOCOL}	= "HTTP/1.0";
$ENV{SERVER_PORT}	= $port;
$ENV{HTTP_PORT}		= $port;
$ENV{SERVER_NAME}	= "";
$ENV{HTTP_HOST}		= "";

#
# 設定(リスト系)
#
my @index = qw (index.html index.htm index.cgi index.txt);

my %encoding = qw (
	gz	gzip
	bz2	bzip2
);

my %mimeType = qw (
	avi	video/x-msvideo
	bin	application/octet-stream
	bmp	image/bmp
	cpio	application/x-cpio
	css	text/css
	csv	text/comma-separated-values
	dvi	application/x-dvi
	gif	image/gif
	html	text/html
	ico	image/x-icon
	jar	application/x-java-archive
	jpg	image/jpeg
	lzh	application/x-lzh
	mid	audio/midi
	mov	video/quicktime
	mp3	audio/mpeg
	mpg	video/mpeg
	ogg	application/x-ogg
	pdf	application/pdf
	pgp	application/pgp-signature
	png	image/png
	ps	application/postscript
	ra	audio/x-realaudio
	rpm	application/x-redhat-package-manager
	swf	application/x-shockwave-flash
	tar	application/x-tar
	tex	application/x-tex
	tif	image/tiff
	txt	text/plain
	tgz	application/x-gtar
	wav	audio/x-wav
	xml	text/xml
	zip	application/zip
);


#----------------------------------------------------------------#
use vars qw($range);

#
# URLデコード
#
sub decode($) {
	local($_) = @_;
	s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
	return $_;
}

#
# HTTPヘッダ
#
sub printHeader($) {
	my ($stat) = @_;
	alarm $timeout;
	print "HTTP/1.0 $stat\r\n",
	      "Server: $ENV{SERVER_SOFTWARE}\r\n",
	      "Connection: Close\r\n";
	alarm 0;
}

#
# エラーメッセージ
#
sub printError($) {
	my ($stat) = @_;
	my $len = length($stat) + 1;
	printHeader($stat);
	alarm $timeout;
	print "Content-Type: text/plain\r\n",
	      "Content-Length: $len\r\n",
	      "\r\n",
	      "$stat\n";
	alarm 0;
}

#
# リクエストを解釈する
# POSTされたエンティティを返す
#
sub readRequest() {
	local $_;
	# ヘッダ
	my $str_request = "";
	alarm $timeout;
	while (<CLIENT>) {
		s/[\n|\r]//g;
		if ($_ eq "") {
			last;

		} elsif (/^(\S+)\s+(\S+)/ && (!defined $ENV{REQUEST_METHOD})) {
			$str_request = $_;
			$ENV{REQUEST_METHOD} = $1;
			$ENV{REQUEST_URI} = $2;

		} elsif (/^Host:\s+/i) {
			$ENV{HTTP_HOST} = $';

		} elsif (/^Range:\s*bytes\s*=\s*(\d+)\s*-/) {
			$range = $1;

		} elsif (/^Content-length:\s+(\d+)/i) {
			$ENV{CONTENT_LENGTH} = $1;

		} elsif (/^Content-Type:\s+([^;]+)/i) {
			$ENV{CONTENT_TYPE} = $1;
		}

		if (/^([^:]+):\s+/) {
			my $key = uc $1;
			my $val = $';
			$key =~ s/-/_/g;
			$ENV{"HTTP_$key"} = $val;
		}
	}
	alarm 0;

	# POSTのときのエンティティ
	my $buf = "";
	if (defined $ENV{CONTENT_LENGTH}) {
		alarm $timeout;
		my($i, $buf2);
		for ($i=0; $i<int($ENV{CONTENT_LENGTH}/$bufsize); $i++) {
			read CLIENT, $buf2, $bufsize;
			$buf .= $buf2;
			alarm $timeout;
		}
		if ($ENV{CONTENT_LENGTH} % $bufsize) {
			read CLIENT, $buf2, $ENV{CONTENT_LENGTH} % $bufsize;
			$buf .= $buf2;
		}
		alarm 0;
	}

	# パスの解釈
	if ($ENV{REQUEST_URI} =~ m|^[a-z]+://([^/]+)|) {
		$ENV{HTTP_HOST}   = $1;
		$ENV{REQUEST_URI} = $';
	}
	my $uri = $ENV{REQUEST_URI};
	if ($uri =~ /\?/) {
		$uri = $`;
		$ENV{QUERY_STRING} = $';
	} else {
		$ENV{QUERY_STRING} = "";
	}

	$uri = decode($uri);
	$uri = "/$uri" if ($uri !~ m|^/|);
	$uri =~ s|/\.\./||g;
	$uri =~ s|^/||;
	my @path = split /\//, $uri, -1;
	$ENV{SCRIPT_NAME} = "";
	$ENV{PATH_INFO}	  = "";
	$ENV{SCRIPT_FILENAME} = $docroot;
	while (@path) {
		$_ = shift @path;
		$ENV{SCRIPT_NAME} .= "/$_";
		$ENV{SCRIPT_FILENAME} .= "/$_";
		if (-f $ENV{SCRIPT_FILENAME}) {
			if (@path) {
				$ENV{PATH_INFO} = "/" . join "/", @path;
			}
			last;
		}
	}

	if (-d $ENV{SCRIPT_FILENAME}) {
		foreach (@index) {
			if (-f "$ENV{SCRIPT_FILENAME}/$_") {
				$ENV{SCRIPT_FILENAME} .= "/$_";
				$ENV{SCRIPT_NAME} .= "/$_";
				last;
			}
		}
	}

	# ログの出力
	{ local $^W = 0;
		my $date = localtime;
		print STDOUT "$ENV{REMOTE_HOST}<>$date<>$str_request<>$ENV{HTTP_REFERER}<>$ENV{HTTP_USER_AGENT}\n";
	}
	return $buf;
}

#
# ファイルの出力
#
sub printFile($) {
	my($file) = @_;
	$file =~ s|^/+||;
	my $encoding;
	my $base = $file;
	$base =~ /\.([^.]+)$/;
	if ((defined $1) && $encoding{$1}) {
		$encoding = $encoding{$1};
		$base = $`;
	}
	$base =~ /\.([^.]+)$/;
	my $suffix = $1;
	$suffix = "txt" unless (defined $suffix);
	my $type = $mimeType{$suffix};
	$type = "text/plain" unless (defined $type);
	if ((-f $file)&&(open IN, $file)) {
		printHeader("200 OK");
		alarm $timeout;
		print "Content-Type: $type\r\n";
		if ($range) {
			my $all = (-s $file);
			my $len = $all - $range;
			seek IN, $range, 00;
			print "Content-Range: bytes $range-" . ($all-1)  . "/$all\r\n",
			      "Content-Length: $len\r\n";
		} else {
			print "Content-Length: ", (-s $file), "\r\n";
		}
		print "Content-Encoding: $encoding\r\n" if (defined $encoding);
		print "\r\n";
		if ($ENV{REQUEST_METHOD} ne "HEAD") {
			alarm $timeout;
			my $buf;
			while (read IN, $buf, $bufsize) {
				print $buf;
				alarm $timeout;
			}
			alarm 0;
		}
		close IN;
	} else {
		printError("404 Not Found");
	}
}

#
# CGIの実行
#
sub execCGI($) {
	my($input) = @_;
	my($IN, $OUT);
	my $cgi = $ENV{SCRIPT_FILENAME};
	$cgi =~ m|/([^/]*)$|;
	$cgi = $1;
	my $dir = $`;
	unless (chdir($dir) && (-f $cgi) && open2($IN, $OUT, "perl", "-w", $cgi, %ENV)) {
		printError("404 Not Found");
		return;
	}

	binmode $IN; binmode $OUT;
	if ($ENV{CONTENT_LENGTH}) {
		print $OUT $input;
	}
	close $OUT;
	my @buf = <$IN>;
	close $IN;
	wait;
	my $cgi_result = $?;

	my @head = ();
	while ($buf[0] !~ /^\s*$/) {
		push @head, shift(@buf);
	}
	shift @buf;
	my $buf = join "", @buf;
	my $len = length $buf;

	if (($cgi_result != 0)||(! ((grep /^Location/i, @head)||(grep /^Content-Type/i, @head)))) {
		printError("500 Internal Server Error");
		return;
	}

	if (grep /^Location/i, @head) {
		printHeader("302 Moved Temporarily");

	} elsif ($range) {
		my $all = length $buf;
		$buf = substr $buf, $range;
		$len = length $buf;
		printHeader("206 Partial content");
		print "Content-Range: bytes $range-" . ($all-1)  . "/$all\r\n",
		      "Content-Length: $len\r\n";

	} else {
		printHeader("200 OK");
		print "Content-Length: $len\r\n";
	}
	print @head;
	print "\r\n";

	if ($ENV{REQUEST_METHOD} ne "HEAD") {
		my $i;
		alarm $timeout;
		for ($i=0; $i<$len; $i+=$bufsize) {
			print substr $buf, $i, $bufsize;
			alarm $timeout;
		}
		alarm 0;
	}
}

#
# 結果の出力
#
sub printResult($) {
	my($buf) = @_;
	if ($ENV{REQUEST_METHOD} eq "OPTIONS") {
		printHeader("200 OK");
		alarm $timeout;
		print "Allow: GET, HEAD, POST, OPTIONS\n",
		      "Content-Length: 0\n\n";
		alarm 0;

	} elsif ($ENV{REQUEST_METHOD} !~ /^(GET|HEAD|POST)$/) {
		printError("501 Not Implemented");

	} elsif ((! defined $ENV{SCRIPT_FILENAME})||(! -f $ENV{SCRIPT_FILENAME})) {
		printError("404 Not Found");

	} elsif ($ENV{SCRIPT_FILENAME} !~ /\.cgi$/i) {
		printFile($ENV{SCRIPT_FILENAME});

	} elsif (defined $ENV{SCRIPT_FILENAME}) {
		execCGI($buf);
	}
}

#
# HTTPD本体
#
use vars qw($children);
sub httpd() {
	local $children = 0;

	# 準備
	socket CLIENT_WAITING, PF_INET, SOCK_STREAM, 0 or die "failed to open socket. $!\n";
	setsockopt CLIENT_WAITING, SOL_SOCKET, SO_REUSEADDR, 1 or die "failed to setsockopt. $!\n";
	bind CLIENT_WAITING, pack_sockaddr_in($port, INADDR_ANY) or die "failed to bind. $!\n";
	listen CLIENT_WAITING, SOMAXCONN or die "failed to listen: $!\n";

	# メインループ
	while (1) {
		my $paddr;
		unless ($paddr = accept(CLIENT, CLIENT_WAITING)) {
			sleep 1;
			next;
		}
		my ($client_port, $client_iaddr) = unpack_sockaddr_in $paddr;
		my $client_ip = inet_ntoa $client_iaddr;
		my $client_hostname;
		if ($resolv) {
			$client_hostname = gethostbyaddr($client_iaddr, AF_INET) || $client_ip;
		} else {
			$client_hostname = $client_ip;
		}

		select CLIENT; $|=1;

		my $pid;
		if (! defined($pid = fork)) {
			warn "server process: fork failed.";
			close CLIENT;
			next;

		} elsif ($pid) {
			$children++;
			close CLIENT;
			if ($children > $childrenLimit) {
				wait;
				$children--;
			}
			next;

		} else {
			binmode CLIENT;
			$SIG{ALRM} = sub { die "server timeout" };
			$ENV{REMOTE_HOST} = $client_hostname;
			$ENV{REMOTE_ADDR} = $client_ip;
			$ENV{REMOTE_PORT} = $client_port;
			my $buf = readRequest();
			printResult($buf);
			shutdown CLIENT, 2;
			close CLIENT;
			exit;
		}
	}
}

#
# メインルーチン
#
httpd();
