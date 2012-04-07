#!/usr/bin/perl -w
#
# 簡易RSSリーダ
#
# 使用法: $0 [-i list] [-a] [-n] [uri]...
#
# -i: リストからの読み込み。リスト名「-」は標準入力を意味する。
# -a: 日付に関係なく全部表示する。
# -n: ダウンロードを行わない。
# uri: RSSのURI
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
use Jcode;

my $CACHE = "$ENV{HOME}/.web";
my $AGENT = "RSSreader/0.3.1";

#
# wget
#
sub wget($) {
	my($uri) = @_;
	my $code =system "wget", "-U", $AGENT,
			 "-T", 10, "-t", 2, "-x", "-N", "-P", $CACHE, $uri;
	return (! $code);
}

#
# read RSS file
#
sub readFile($) {
	my($uri) = @_;
	$uri =~ s|^.*?://||;
	my $file = "$CACHE/$uri";
	if ($file =~ m|/\?|) {
		$file = "$`/index.html?$'";
	} elsif ($file =~ m|/$|) {
		$file .= "index.html";
	}
	open IN, $file;
	my @buf = <IN>;
	close IN;

	local $_ = join "", @buf;
	s/\s+/ /g;
	my $jcode = "UTF-8";
	if (/<?xml[^>]+encoding=["']([^'">]+)["']/) {
		$jcode = $1;
	}
	if ($jcode =~ /UTF-?8/i) {
		$_ = Jcode->new($_, "utf8")->euc;
	} elsif ($jcode =~ /SHIFT_JIS/i) {
		$_ = Jcode->new($_, "sjis")->euc;
	} elsif ($jcode =~ /EUC-JP/i) {
		# $_ = Jcode->new($_, "euc")->euc;
	} elsif ($jcode =~ /ISO-2022-JP/i) {
		$_ = Jcode->new($_, "jis")->euc;
	} else {
		$_ = Jcode->new($_, "utf8")->euc;
	}
	return $_;
}

#
# get RSS channel
#
sub getChannel($) {
	local($_) = @_;
	my %channel = ();
	if (m|<channel[^>]*>(.*?)</channel>|) {
		$_ = $';
		my $str = $1;
		$channel{link}  = ($str =~ m|<link>([^<]*)</link>|)? $1: "";
		$channel{title} = ($str =~ m|<title>([^<]*)</title>|)? $1: "";
		$channel{desc}  = ($str =~ m|<description>([^<]*)</description>|)? $1: "";
	}
	return %channel;
}

#
# get URI and Title
#
sub getItem($) {
	local($_) = @_;
	my %item = ();
	while (m|<item[^>]*>(.*?)</item>|) {
		$_ = $';
		my $str = $1;
		my $link  = ($str =~ m|<link>([^<]*)</link>|)? $1: "";

		$item{$link}{title} = ($str =~ m|<title>([^<]*)</title>|)? $1: "";
		$item{$link}{date}  = ($str =~ m|date>([^<]*)</[^>]*date>|i)? $1: "";
		$item{$link}{desc}  = ($str =~ m|<description>([^<]*)</description>|)? $1: "";
	}
	return %item;
}

#
# main
#
my @rss = ();
my %flag = ();

while (@ARGV) {
	$_ = shift @ARGV;
	if ($_ eq "-i") {
		my $file = shift @ARGV;
		if ($file eq "-") {
			@rss = <STDIN>;
		} elsif (open IN, $file) {
			@rss = <IN>;
			close IN;
		}
	} elsif ($_ eq "-a") {
		$flag{all} = 1;
	} elsif ($_ eq "-n") {
		$flag{no_down} = 1;
	} else {
		push @rss, $_;
	}
}
chomp @rss;
@rss = grep $_!~/^\s*$|^\s*#/, @rss;

die "usage: $0 [-i list] [-a] [uri]...\n" unless (@rss);

my %read = ();
print "<html><head><title>RSS</title></head><body>\n";
foreach (@rss) {
	next if ($read{$_}++);

	my $old = readFile($_);
	my %old = getItem($old);

	wget($_) unless ($flag{no_down});

	my $new = readFile($_);
	my %new = getItem($new);
	my %channel = getChannel($new);

	my $link;
	my @buf = ();
	foreach $link (keys %new) {
		if ($flag{all} || $flag{no_down} ||
			(! defined $old{$link}) ||
			($old{$link}{date} ne $new{$link}{date})) {
			push @buf, $link;
		}
	}

	if (@buf) {
		print "<h1><a href='$channel{link}'>$channel{title}</a></h1>\n",
		      "<p>$channel{desc}<p>\n",
		      "<dl>\n";
		foreach $link (@buf) {
			print "  <dt><a href='$link'>$new{$link}{title}</a></dt>\n";
			my $key;
			foreach $key qw(date desc) {
				print "    <dd>$new{$link}{$key}</dd>\n" if ($new{$link}{$key});
			} 
		}
		print "</dl>\n";
	}
}
print "</body></html>\n";
