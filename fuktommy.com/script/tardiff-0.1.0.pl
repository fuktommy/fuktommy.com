#!/usr/bin/perl -w
#
# tarで固められたディレクトリの差分を調べる
#
# 使用法: $0 tarボール1 tarボール2
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

use Cwd;

$TMP = "/tmp";

#
# make temporary directory
#
sub tmpdir($) {
	my($parent) = @_;
	my $i = 0;
	my $dir;
	do { $dir = "$parent/tmp$i"; $i++; } until ((! -e $dir) && mkdir($dir));
	chmod 0700, $dir;
	return $dir;
}

#
# unpack TAR arcive
#
sub unpackTar($$$) {
	my($dir, $sub, $arc) = @_;
	local $_ = $arc;
	my @opt = ("-x");
	if (/\.tar.gz$/ || /\.tgz$/) {
		push @opt, "-z";
	} elsif (/\.tar.bz2$/ || /\.tbz2$/) {
		push @opt, "-j";
	}
	mkdir "$dir/$sub", 0777 or die;
	my $code = system "tar", @opt, "-C", "$dir/$sub", "-f", $arc;
	return ($code == 0);
}

#
# basename of path
#
sub basename($) {
	my($path) = @_;
	$path =~ s|.*/||;
	return $path
}

#
# main
#
die "usage: $0 tar1 tar2" if (@ARGV != 2);

($arc1, $arc2) = @ARGV;
die unless ((-f $arc1) && (-f $arc2));

$file1 = basename($arc1);
$file2 = basename($arc2);
if ($file1 eq $file2) {
	$file1 = "0$file1";
	$file2 = "1$file1";
}

$dir = tmpdir($TMP);
unpackTar($dir, $file1, $arc1) or die;
unpackTar($dir, $file2, $arc2) or die;

$work = cwd;
chdir $dir or die;
$code = system "diff", "-Nru", $file1, $file2;
chdir $work or die;
system "rm", "-Rf", $dir;
exit $code;
