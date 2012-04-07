#!/usr/bin/perl
#
# ネットワークに1秒間あたり何バイトの入出力があるか監視する
#
# 使用法: $0 [-n 秒数]
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

sub getStatus() {
	open IN, "/proc/net/dev";
	<IN> foreach (1..2);
	while (<IN>) {
		@_ = split /[:\s]+/;
		$stat{$_[1]} = [$_[2], $_[10]];
	}
	close IN;
	return %stat;
}

sub printStatus($$$) {
	my %old = %{$_[0]};
	my %new = %{$_[1]};
	my $sec = $_[2];
	my $if;
	printf "%16s %8s\n", "Receive", "Transmit";
	foreach $if (@if) {
		printf "%6s:", $if;
		foreach (0..1) {
			my $diff = ($new{$if}[$_] - $old{$if}[$_])/$sec;
			printf " %8d", $diff;
		}
		print "\n";
	}
}

$second = 1;
while (@ARGV) {
	$_ = shift @ARGV;
	if ($_ eq "-n") {
		$second = shift @ARGV;
	}
}

%old = getStatus();
@if = sort keys %old;
while(1) {
	%new = getStatus();
	print "\033(B\033[H\033[J";
	printStatus(\%old, \%new, $second);
	%old = %new;
	sleep $second;
}
