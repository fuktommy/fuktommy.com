#!/usr/bin/perl -w
#
# ローカルに保存したHTMLファイルから頻出単語を調べる
#
# Jcode.pm, 茶筅(ChaSen)が必要
#
# 使用法: $0 [-r] [-l] [-d] [-n #] [-l [-u #]] [-j 文字コード] [-s 検索エンジン] ファイルまたはディレクトリ...
#
# オプション:
#		-r: HTMLの代わりに単語統計ファイルを読み込む
#		-d: 単語を含む文書の数で計算する
#		-n: Nグラム
#		-l: 単語統計ファイルを出力する
#		-u: 表示する頻度の下限
#		-j: 文字コードの指定
#		-s: 検索エンジンの指定(<KEY>が文字列に置換される)
#
# 文字コード指定
#		utf8, sjis, euc, jis
#
# 2004-07-29	0.1-beta9	検索エンジンの指定
# 2004-07-23	0.1-beta8	文書の点数に、文書のサイズを加味する
# 2004-07-23	0.1-beta7	文書の点数に、文書のサイズを加味する
# 2004-07-18	0.1-beta6	文字コード変換の修正
# 2004-07-18	0.1-beta5	自分の興味に近い文書を表示する機能
# 2004-07-11	0.1-beta4	バイグラム
# 2004-07-11	0.1-beta3	単語を含む文書の数で計算する
# 2004-07-11	0.1-beta2	再帰オプションなど
# 2004-07-10	0.1-beta1
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
use Jcode;

use vars qw($JCODE $SEARCH $NGRAM $LIMIT_STRING);
$JCODE	= "";
$NGRAM	= 1;
$LIMIT_STRING = 7*1024;
$SEARCH	= "http://www.google.co.jp/search?q=<KEY>&ie=EUC-JP&oe=EUC-JP&hl=ja&btnG=Google+%8C%9F%8D%F5&lr=lang_ja&num=100";
my $TYPE	= "名詞|未知語";
my $IGNORE	= '^.$|^..$|^&|[=<>]|' . "^[\0-\100\133-\140\176-\177]*\$";
my $IGNORE_TYPE = "代名詞|非自立|接尾";
my $UNDER	= 1;
my $DOCS_MODE	= 0;
my $READ_LIST	= 0;
my $WRITE_LIST	= 0;
my @file = ();

while (@ARGV) {
	$_ = shift @ARGV;
	if ($_ eq "-u") {
		$UNDER = shift @ARGV;
	} elsif ($_ eq "-r") {
		$READ_LIST = 1;
	} elsif ($_ eq "-l") {
		$WRITE_LIST = 1;
	} elsif ($_ eq "-d") {
		$DOCS_MODE = 1;
	} elsif ($_ eq "-n") {
		$NGRAM = shift @ARGV;
	} elsif ($_ eq "-j") {
		$JCODE = shift @ARGV;
	} elsif ($_ eq "-s") {
		$SEARCH = shift @ARGV;
	} else {
		push @file, $_;
	}
}
die "usage: $0 [-r] [-d] [-n #] [-l [-u #]] [-j code] file...\n" unless (@file);
use vars qw($CHASEN_IN $CHASEN_OUT);
open2($CHASEN_IN, $CHASEN_OUT, "chasen");

#
# ファイルのリスト
#
sub files($);
sub files($) {
	my($file) = @_;
	if (-f $file) {
		return $file;
	} elsif (-d $file) {
		local $_;
		my @file = ();
		foreach (glob "$file/*") {
			push @file, files($_);
		}
		return @file;
	}
}

#
# HTMLをテキストに変換(タグは飛ばす)
#
sub html2text($@) {
	my($xjcode, @buf) = @_;
	my $jcode = "";
	local $_;
	my @buf2 = ();
	foreach (@buf) {
		if (($jcode eq "") && $_ && (/charset=([^"'\s]+)/i)) {
			$jcode = $1;
		}
		s/<[^>]*>/ /g;
		s/\s+/ /g;
		push @buf2, $_;
	}
	$_ = join "\n", @buf2;
	if ($jcode =~ /UTF-?8/i) {
		$_ = Jcode->new($_, "utf8")->euc;
	} elsif ($jcode =~ /SHIFT_JIS/i) {
		$_ = Jcode->new($_, "sjis")->euc;
	} elsif ($jcode =~ /EUC-JP/i) {
		# $_ = Jcode->new($_, "euc")->euc;
	} elsif ($jcode =~ /ISO-2022-JP/i) {
		$_ = Jcode->new($_, "jis")->euc;
	} elsif ($xjcode) {
		$_ = Jcode->new($_, $xjcode)->euc;
	} else {
		$_ = Jcode->new($_)->euc;
	}
	return $_;
}

#
# ファイルを読む(タグは飛ばす)
#
sub readHTML($) {
	my($file) = @_;
	my($IN);
	local $_;
	my $jcode = "";
	open $IN, $file or return ();
	my @buf = <$IN>;
	close $IN;
	return html2text($JCODE, @buf);
}

#
# 単語頻度
#
sub freq(@) {
	my @file = @_;
	my %freq = ();
	foreach (@file) {
		warn "reading $_\n";
		my %freq_file = ();
		local $_ = readHTML($_);
		my @buf = split /\s+/, $_;
		my @prev = ();
		foreach (@buf) {
			$_ = substr $_, 0, $LIMIT_STRING;
			print $CHASEN_OUT $_, "\n";
			do {
				$_ = <$CHASEN_IN>;
				chomp;
				@_ = split;
				if ((defined $_[2]) && ($_[2] =~ /$IGNORE/)) {
					# nop
				} elsif ($_[3] && ($_[3] =~ /$IGNORE_TYPE/)) {
					# nop
				} elsif ($_[3] && ($_[3] =~ /$TYPE/)) {
					my $key = $_[2];
					my $tmp = $key;
					$key = "@prev $key";
					push @prev, $tmp;
					shift @prev while (@prev >= $NGRAM);
					if ($DOCS_MODE && (! $freq_file{$key})) {
						$freq_file{$key}++;
						$freq{$key}++;
					} elsif (! $DOCS_MODE) {
						$freq{$key}++;
					}
				}
			} while ($_ && ($_ ne "EOS"));
		}
	}
	return %freq;
}

#
# リストの読み込み
#
sub readList(@) {
	my @file = @_;
	local $_;
	my %freq = ();
	my($IN);
	foreach (@file) {
		open $IN, $_ or next;
		while (<$IN>) {
			chomp;
			@_ = split /: /, $_, 2;
			next if (@_ < 2);
			$_[0] =~ s/\s//g;
			$freq{$_[1]} = $_[0];
		}
	}
	return %freq;
}

#
# wget
#
sub wget($) {
	my($uri) = @_;
	my($IN, $OUT);
	open2($IN, $OUT, "wget", "-i", "-", "-O", "-",
		   "-U", "Mozilla/4.0 (Webtf)", "-T", 10, "-t", 2);
	print $OUT $uri, "\n";
	close $OUT;
	my @buf = <$IN>;
	close $IN;
	wait;
	return @buf;
}

#
# 文書の点数付け
#
sub score($%) {
	my($uri, %freq) = @_;
	my @buf = wget($uri);
	local $_ = html2text("", @buf);
	@buf = split /\s+/, $_;
	my $score = 0;
	my @prev = ();
	my %freq_file = ();
	my $size = 0;
	foreach (@buf) {
		$_ = substr $_, 0, $LIMIT_STRING;
		$size += length $_;
		print $CHASEN_OUT $_, "\n";
		do {
			$_ = <$CHASEN_IN>;
			chomp;
			@_ = split;
			if ((defined $_[2]) && ($_[2] =~ /$IGNORE/)) {
				# nop
			} elsif ($_[3] && ($_[3] =~ /$IGNORE_TYPE/)) {
				# nop
			} elsif ($_[3] && ($_[3] =~ /$TYPE/)) {
				my $key = $_[2];
				my $tmp = $key;
				$key = "@prev $key";
				push @prev, $tmp;
				shift @prev while (@prev >= $NGRAM);
				if ($freq{$key} && $DOCS_MODE && (! $freq_file{$key})) {
					$freq_file{$key}++;
					$score += $freq{$key};
				} elsif ($freq{$key} && (! $DOCS_MODE)) {
					$score += $freq{$key};
				}
			}
		} while ($_ && ($_ ne "EOS"));
	}
	return $score / sqrt($size+1);
}

#
# URLエンコード
#
sub encode($) {
	my($s) = @_;
	$s =~ s|[^\w]|'%' . uc(unpack('H2', $&))|eg;
	return $s;
}

#
# 検索
#
sub search($) {
	my($key) = @_;
	$key =~ s/^\s+//;
	$key = encode($key);
	my $uri = $SEARCH;
	$uri =~ s/<KEY>/$key/g;
	my @buf = wget($uri);
	my @uri = ();
	local $_;
	foreach (@buf) {
		while (/href=["']?([^"'>]+)/) {
			push @uri, $1;
			$_ = $';
		}
	}
	@uri = grep $_ =~ /^http/, @uri;
	@uri = grep $_ !~ /google|rss|rdf|pdf/, @uri;
	return @uri;
}

#
# メイン
#
my @file2 = ();
foreach (@file) {
	push @file2, files($_);
}
@file = @file2;

my %freq;
if ($READ_LIST) {
	%freq = readList(@file);
} else {
	%freq = freq(@file);
}

my @key = keys %freq;
@key = sort {$freq{$b} <=> $freq{$a}} @key;

if ($WRITE_LIST) {
	foreach (@key) {
		printf "%7d: %s\n", $freq{$_}, $_ if ($freq{$_} >= $UNDER);
	}
	exit;
} elsif (@key == 0) {
	exit;
}

my @uri = search($key[0]);
my %score = ();
foreach (@uri) {
	$score{$_} = score($_, %freq);
}
@uri = sort {$score{$b} <=> $score{$a}} @uri;

close $CHASEN_IN;
close $CHASEN_OUT;
wait;

print "<html><head><title>webtf</title></head><body><ul>\n";
foreach (@uri) {
	printf "<li>%7d: <a href='%s'>%s</a></li>\n", $score{$_}, $_, $_;
}
print "</ul></body></html>\n";
