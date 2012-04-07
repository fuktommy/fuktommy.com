#!/usr/bin/perl -w
#
# 画像掲示板 メロメロの画像をぶっこ抜き
#
# 使用法: $0 bid [tid]
#
# 2004-07-04	0.1.1	tid, partの指定ができる
# 2004-07-04	0.1.0
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

use vars qw($SLEEP $HOST $BBS $AGENT @WGET);
use vars qw($countImage);
my $SLEEP = 2;
my $HOST  = "www.mero-mero.net";
my $BBS   = "/meroboard2/meroboard2.php";
my $AGENT = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)";
my @WGET  = ( "wget", "-w", $SLEEP, "--random-wait", "-i", "-",
	      "-T", "10", "-t", "4", "-q", "-U", $AGENT);
$countImage = 0;

#
# 引数の処理
#
my($bid, $tid, $part);
if (@ARGV == 1) {
	($bid) = @ARGV;
} elsif (@ARGV == 2) {
	($bid, $tid) = @ARGV;
} elsif (@ARGV == 3) {
	($bid, $tid, $part) = @ARGV;
}
if (! defined $bid) {
	die "usage: $0 bid [tid [part]]\n";
}

#
# 板を取得し、スレッドのリストを返す
#
sub getBoard($) {
	my($bid) = @_;
	my($IN, $OUT);
	open2 $IN, $OUT, @WGET, "-O", "-";
	print $OUT "http://$HOST$BBS?bid=$bid\n";
	print	   "http://$HOST$BBS?bid=$bid\n";
	close $OUT;
	my @buf = <$IN>;
	close $IN;
	wait;

	my @thread = ();
	foreach (@buf) {
		push @thread, m|<a href=/meroboard2/meroboard2.php\?bid=$bid&tid=\d+&part=\d+>|g;
	}
	foreach (@thread) {
		m|<a href=(/meroboard2/meroboard2.php\?bid=$bid&tid=\d+&part=\d+)>|;
		$_ = $1;
	}

	return (@thread);
}

#
# スレッドを取得し、画像のリストを返す
#
sub getThread($$) {
	my($path, $page) = @_;
	my($IN, $OUT);
	open2 $IN, $OUT, @WGET, "-O", "-";
	print $OUT "http://$HOST$path&page=$page\n";
	print	   "http://$HOST$path&page=$page\n";
	close $OUT;
	my @buf = <$IN>;
	close $IN;
	wait;

	my @image = ();
	foreach (@buf) {
		push @image, m|href=/meroboard2/image2/\S+|g;
	}
	foreach (@image) {
		m|href=(/meroboard2/image2/\S+)|;
		$_ = $1;
	}

	my $done = 1;
	foreach (@buf) {
		if (m|page=(\d+)>\d+</a>]</td>|) {
			$page = $1;
			last;
		}
	}
	return ($page, \@image);
}

#
# 取得する画像の選択
#
sub getURI(@) {
	my @image = @_;
	my @uri  = ();
	local $_;
	foreach (@image) {
		my $file = $_;
		$file =~ s|.*/||;
		next if (-e $file);
		push @uri, "http://$HOST$_";
	}
	return (@uri);
}

#
# 画像の取得
#
sub getImage(@) {
	my @uri = @_;
	my($IN, $OUT);
	open2 $IN, $OUT, @WGET;
	close $IN;
	foreach (@uri) {
		$countImage++;
		print $OUT "$_\n";
#		print	   "$_\n";
	}
	close $OUT;
	wait;
}

#
# メインループ
#
my @thread = ();
if ((defined $tid) && (defined $part)) {
	@thread = ("$BBS?bid=$bid&tid=$tid&part=$part");
} elsif (defined $tid) {
	@thread = ("$BBS?bid=$bid&tid=$tid&part=0");
} else {
	@thread = getBoard($bid);
}


sleep $SLEEP if ($SLEEP > 0);
foreach (@thread) {
	my $page = 0;
	my($maxpage, $image);
	do {
		($maxpage, $image) = getThread($_, $page);
		my @uri = getURI(@$image);
#		goto XXX if (@uri == 0);
		getImage(@uri);
		sleep $SLEEP if ($SLEEP > 0);
	} while (++$page <= $maxpage);
#	XXX: ;
}
print "Dounload $countImage image(s)\n";
