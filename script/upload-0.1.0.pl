#!/usr/local/bin/perl
#
# 性善説のアップローダ
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

#
# 設定
#
my $SELF_URI		= "/cgi-bin/upload.cgi";	# CGIのURI
my $TITLE		= "性善説のアップローダ";	# 全体のタイトル
my $MAIL_ADDRESS	= 'fuktommy@inter7.jp';		# あなたのメールアドレス
my $DATA_DIR		= "../data";			# データを書き込むところ
my $DATA_URI		= "/data";			# データのURI
my $FILE_SIZE		= 5;				# ファイルの最大サイズ(MB)
my $FILE_SUM		= 45;				# ファイルの合計の最大サイズ(MB)
umask 0000;

#
# 日時
#
sub xlocaltime($) {
	my @buf = localtime($_[0]);
	return sprintf "%d/%02d/%02d %02d:%02d",
		       1900+$buf[5], $buf[4]+1, $buf[3], $buf[2], $buf[1];
}

#
# 表紙
#
sub printHTML() {
	print <<EOF
Content-Type: text/html; charset=EUC-JP,

<?xml version="1.0" encoding="EUC-JP"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja">
<head>
  <meta http-equiv="Content-Language" content="ja" />
  <meta http-equiv="Content-Style-Type" content="text/css" />
  <meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />
  <title>$TITLE</title>
  <link rev="made" href="mailto:$MAIL_ADDRESS" />
  <link rel="contents" href="$SELF_URI" />
</head>
<body>
<h1>$TITLE</h1>
<p>ここで公開できるファイルは、誰であっても改変して、
またはそのままの形で公開できるファイルだけです。</p>
EOF
;

	local $_;
	print "<h2>ファイル</h2>\n<ul>\n";
	foreach (sort {$b <=> $a} glob("$DATA_DIR/*")) {
		my $size = int((-s $_) / 1024);
		m|(\d+)|;	my $base = $1;
		s|$DATA_DIR/||;
		my $date = xlocaltime($base);
		print "<li>$date <a href='$DATA_URI/$_'>$_</a>(${size}KB)</li>\n";
	}
	print "</ul>\n\n";

	print <<EOF
<h2>投稿</h2>
<form method="post" action="$SELF_URI" enctype="multipart/form-data"><p>
  約${FILE_SIZE}MBまでのファイルをアップロードできます。<br />
  <input type="hidden" name="cmd" value="post" />
  ファイル<input type="file" name="file" tabindex="1" accesskey="f" />
  (拡張子: <input name="suffix" value="" tabindex="2" accesskey="s" />)
  <input type="submit" name="submit" value="投稿" tabindex="3" accesskey="w" />
</p></form>

<h2>削除</h2>
<form method="get" action="$SELF_URI"><p>
  <input type="hidden" name="cmd" value="remove" />
  ファイル名<input name="file" value="" tabindex="3" accesskey="f" />
  <input type="submit" name="submit" value="削除" tabindex="3" accesskey="w" />
</p></form>

<p>(c) 2004 <a href="http://fuktommy.s64.xrea.com/">Fuktommy</a></p> 
</body>
</html>
EOF
;
}

#
# ジャンプ
#
sub print302() {
	print <<EOF
Content-Type: text/html; charset=EUC-JP,

<?xml version="1.0" encoding="EUC-JP"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja">
<head>
  <meta http-equiv="Content-Language" content="ja" />
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
  <meta http-equiv="Content-Script-Type" content="text/javascript" />
  <title>moved</title>
  <link rev="made" href="mailto:$MAIL_ADDRESS" />
  <link rel="contents" href="$SELF_URI" />
</head>
<body>
  <p>Click and jump to <a href="$SELF_URI">Title Page</a></p>
  <script type="text/javascript">window.location.href = "$SELF_URI";</script>
</body>
</html>
EOF
;
}

#
# エラー
#
sub printError($) {
	my($msg) = @_;
	print "Content-Type: text/plain; charset=EUC-JP\n\n",
	      "$msg\n";
	exit;
}

#
# ファイルのリスト
#
sub list($) {
	my($dir) = @_;
	local $_;
	my @list = ();
	foreach (glob "$dir/*") {
		s|$dir/||;
		s|\..+||;
		push @list, $_;
	}
	return sort {$a <=> $b} @list;
}

#
# ファイル全体のサイズ
#
sub size($) {
	my($dir) = @_;
	local $_;
	my $size = 0;
	foreach (glob "$dir/*") {
		$size += (-s $_);
	}
	return $size;
}

#
# ファイルの削除
#
sub remove($) {
	my($file) = @_;
	local $_;
	my $stat = 0;
	foreach (glob "$DATA_DIR/$file.*") {
		$stat |= unlink $_;
	}
	return $stat;
}

#
# 引数
#
sub args() {
	local $_ = $ENV{QUERY_STRING};
	my %arg = ();
	foreach (split /&/) {
		@_ = split /=/;
		if (defined $_[1]) {
			$arg{$_[0]} = $_[1];
		}
	}
	return %arg;
}

#
# 引数(multipart/form-data)
#
sub argsFromMulti() {
	my $date = time;
	my %arg = ();
	$ENV{CONTENT_TYPE} =~ /boundary=(\S+)/i;
	my $boundary = $1;
	local $_;
	while (<STDIN>) {
		if (/$boundary/) {
			$_ = <STDIN>;
			/Content-Disposition: form-data; name="([^"]+)"/i or next;
			my $key = $1;

			if (($key eq "file") && /filename="([^"]+)"/i) {
				$arg{auto_suffix} = $1;
				$arg{auto_suffix} =~ s/.*[\/\\]//;
				if ($arg{auto_suffix} =~ /\.([^.]*)$/) {
					$arg{auto_suffix} = $1;
					$arg{auto_suffix} = lc $arg{auto_suffix};
				} else {
					$arg{auto_suffix} = "";
				}
			}
			$_ = <STDIN> until ((! defined $_) || ($_ eq "\r\n"));

			if ($key eq "file") {
				open OUT, "> $DATA_DIR/$date.tmp" or printError("$DATA_DIR/$date.tmp");
				my $prev = "";
				while (($_ = <STDIN>) !~ /$boundary/) {
					print OUT $prev;
					$prev = $_;
				}
				if ($prev ne "") {
					$prev =~ s/\r\n$//;
					print OUT $prev;
				}
				close OUT;
				if (-s "$DATA_DIR/$date.tmp") {
					$arg{file} = $date;
				} else {
					unlink "$DATA_DIR/$date.tmp";
				}
				redo;
			} else {
				$arg{$key} = <STDIN>;
				$arg{$key} =~ s/[\r\n]+$//;
			}
		}
	}
	return %arg;
}

#
# メイン
#
if (-d $DATA_DIR) {
	# ok
} elsif (mkdir $DATA_DIR, 0777) {
	# ok
} else {
	printError($DATA_DIR);
	exit;
}

my %arg;
if ($ENV{REQUEST_METHOD} ne "POST") {
	%arg = args();
} elsif ($ENV{CONTENT_LENGTH} <= $FILE_SIZE*1024*1024) {
	%arg = argsFromMulti();
} else {
	printError("Too Big File");
}

if (! $arg{cmd}) {
	printHTML();

} elsif ($arg{cmd} eq "post") {
	my @list = list($DATA_DIR);
	until (size($DATA_DIR) <= ($FILE_SUM-$FILE_SIZE)*1024*1024) {
		remove(shift(@list)) or printError("Cannnot Remove");
	}
	my $suffix = "txt";
	if (! $arg{file}) {
		printError("Null File");
	} elsif ((defined $arg{suffix}) && ($arg{suffix} =~ /^[A-Za-z0-9-_.]+$/)) {
		$suffix = $arg{suffix};
	} elsif ((defined $arg{auto_suffix}) && ($arg{auto_suffix} =~ /^[A-Za-z0-9-_.]+$/)) {
		$suffix = $arg{auto_suffix};
	}
	rename "$DATA_DIR/$arg{file}.tmp", "$DATA_DIR/$arg{file}.$suffix";
	print302();

} elsif ($arg{cmd} eq "remove") {
	if ($arg{file} =~ /^(\d+)/) {
		remove($1);
		print302();
	} else {
		printError("Bad File Name");
	}
	
} else {
	printHTML();
}
