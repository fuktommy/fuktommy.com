#!/usr/bin/perl -w
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

my $input = $ARGV[0] or die;
open IN, $input or die;

$input =~ s/.*\///;
$input =~ s/\.ogg$//i;
my $i = 0;
my $stat = 0;

while (read IN, $_, 1024) {
	my $buf;
	if (($stat == 0) && /OggS.{1,30}vorbis/m) {
		my $file = sprintf "$input.%03d.ogg", $i++;
		warn $file;
		open OUT, "> $file";
		print OUT;
		$stat = 1;

	} elsif ($stat == 0) {

	} elsif (/OggS.{1,30}vorbis/m) {
		print OUT $`;
		my $file = sprintf "$input.%03d.ogg", $i++;
		warn $file;
		open OUT, "> $file";
		print OUT $&, $';

	} elsif (read IN, $buf, 1024) {
		if (($_ . $buf) =~ /OggS.{1,30}vorbis/m) {
			print OUT $`;
			my $file = sprintf "$input.%03d.ogg", $i++;
			warn $file;
			open OUT, "> $file";
			print OUT $&, $';

		} else {
			print OUT $_;
			$_ = $buf;
			redo;
		}

	} else {
		print OUT;
	}
}
