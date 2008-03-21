#!/usr/bin/perl -w
# Player for peercast+{ogg123,mpg123}+esd
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
use vars qw($esdpid);

my @uri  = ();
my $rate = 22050;

while (@ARGV) {
	$_ = shift @ARGV;
	if ($_ eq "-r") {
	} elsif ($_ eq "-8") {
		$rate = 8000;
	} else {
		push @uri, $_;
	}
}

die "usage: $0 [-r rate] [-8] URI...\n" unless (@uri);
exit if (fork);

open STDIN,  "< /dev/null";
open STDOUT, "> /dev/null";
open STDERR, "> /dev/null";

$esdpid = 0;
if (($esdpid=fork) == 0) {
	exec "esd", "-b", "-r", $rate, "-nobeeps";
}

my $pid = 0;
foreach (@uri) {
	if (($pid=fork) == 0) {
		if (/\.ogg/i) {
			exec "ogg123", "-v", $_;
		} elsif (/\.mp3/i) {
			exec "mpg123", "-v", $_;
		}
	}
	wait;
}

END { kill "TERM", $esdpid if ($esdpid)};
