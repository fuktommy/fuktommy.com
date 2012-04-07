#!/usr/bin/perl
#
# Webの深さ優先探索ごっこ
#
# $LISTでファイルを指定し、あらかじめ適当なURIを書いておいてください。
# あとはCGIを読み込む度に、どこかにジャンプします。
#
# 2004-07-24	0.1-beta1
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

my $LIST = "$ENV{HOME}/work/depth-main.txt";	
my $HIST = "$ENV{HOME}/work/depth-hist.txt";
my $SIZE = 100;
my $START = "http://fuktommy.s64.xrea.com/";

sub wget($) {
	my($uri) = @_;
	my($IN, $OUT);
	open2 $IN, $OUT, "wget", "-q", "-T", 10, "-t", 2, "-O", "-", $uri;
	close $OUT;
	my @buf = <$IN>;
	close $IN;
	wait;
	return @buf;
}

sub getURI($@) {
	my($base, @buf) = @_;

	$base =~ s|/[^/]*$||;
	my $prot = $base;
	$prot =~ s|/.*||;
	my $host = $base;
	$host =~ s|.*?//||;
	$host =~ s|/.*||;

	local $_;
	my @uri = ();
	foreach (@buf) {
		my $flag = 1;
		while ($flag) {
			if (/<a[^>]*?href="([^">]+)"/i) {
				push @uri, $1;
				$_ = $';
			} elsif (/<a[^>]*?href='([^'>]+)'/i) {
				push @uri, $1;
				$_ = $';
			} elsif (/<a[^>]*?href=([^\s>]+)/i) {
				push @uri, $1;
				$_ = $';
			} elsif (/<frame[^>]*?src="([^">]+)"/i) {
				push @uri, $1;
				$_ = $';
			} elsif (/<frame[^>]*?src='([^'>]+)'/i) {
				push @uri, $1;
				$_ = $';
			} else {
				$flag = 0;
			}
		}
	}
	foreach (@uri) {
		s/&amp;/&/g;
		s/#.*//;
		if (m|^https?://| or m|^ftp://|) {
			# NOP
		} elsif (/^mailto:/ or /^#/ or /^javascript:/) {
			undef $_;
		} elsif (/^#/) {
			undef $_;
		} elsif (/\.(tar\.gz|tar\.bz2|tgz|zip|exe|pdf|mp3)$/) {
			undef $_;
		} elsif (m|^/|) {
			$_ = "$prot//$host$_";
		} else {
			$_ = "$base/$_";
		}
	}
	return grep defined $_, @uri;
}

sub random(@) {
	my @list = @_;
	my($i);
	for ($i=@list; $i>0; $i--) {
		my $t = int rand $i;
		($list[$i-1], $list[$t]) = ($list[$t], $list[$i-1]);
	}
	return @list;
}

#
# main
#
my $list = new Stack($LIST, $SIZE);
my $hist = new Stack($HIST, $SIZE);

my $uri = $list->pop();
$uri = $list->pop() while ($uri && $hist->include($uri));
$uri = $START unless defined ($uri);

my @buf = wget($uri);
my @uri = getURI($uri, @buf);

my @tmp = ();
$hist->push($uri);
foreach (@uri) {
	unless ($hist->include($_)) {
		push @tmp, $_;
	}
}

@uri = random(@tmp);
$list->push(@uri);
print "Location: $uri\n\n";

#----------------------------------------------------------------#
package Stack;

sub new($$$) {
	my($this, $file, $size) = @_;
	my $IN;
	my @list = ();
	if (open $IN, $file) {
		@list = <$IN>;
		close $IN;
		chomp @list;
	}
	return bless {file=>$file, size=>$size, list=>\@list};
}

sub DESTROY($) {
	my($this) = @_;
	my $OUT;
	open $OUT, "> $$this{file}" or die;
	local $_;
	foreach (@{$$this{list}}) {
		print $OUT $_, "\n";
	}
	close $OUT;
}

sub push($@) {
	my($this, @item) = @_;
	push @{$$this{list}}, @item;
	shift @{$$this{list}} while (@{$$this{list}} > $$this{size});
}

sub pop($) {
	my($this) = @_;
	return pop @{$$this{list}};
}

sub include($$) {
	my($this, $key) = @_;
	return grep $_ eq $key, @{$$this{list}};
}
