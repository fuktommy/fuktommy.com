#!/usr/bin/perl -w
#
# �ϥå��奵����
#
# �֥������ǡ����פΥǡ����١�����������ɤ߹���Ǥ�����
# TCP��ͳ���䤤��碌�������롢�ʰ�Ū�ʥǡ����١���������
#
# ����ˡ: $0 [-p �ݡ����ֹ�] [-s ���ڤ�ʸ����] �ե�����̾...
#
# ���Υե��ȥ���ɤ�HashServ.pm
# 1�ĤΥ������Ф���ʣ�����ͤ����äƤ褤
#
# �ݡ����ֹ�Υǥե���Ȥ� 8000
# ���ڤ�ʸ����Υǥե���Ȥ� 1�İʾ�Υ���ʸ�� (\t+)
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
# 2004-09-29	0.1-beta6	���ޤ��ʤ�
# 2004-09-21	0.1-beta5	���ޤ��ʤ�
# 2004-08-30	0.1-beta4	�����ʥ�ΥХ�����
# 2004-08-30	0.1-beta3	���å������ݤ�
# 2004-06-02	0.1-beta2	���̲����뤿��������֤�
# 2004-06-02	0.1-beta1
#
use strict;
use Socket;

my $port = 5000;
my $separater = "\t+";
$SIG{CHLD} = "IGNORE";

my @file = ();
while (@ARGV) {
	$_ = shift @ARGV;
	if ($_ eq "-p") {
		$port = shift @ARGV;
	} elsif ($_ eq "-s") {
		$separater = shift @ARGV;
	} else {
		push @file, $_;
	}
}
die "usage: $0 [-p port] [-s separater] file...\n" unless (@file);
@ARGV = @file;

socket CLIENT_WAITING, PF_INET, SOCK_STREAM, 0 or die;
setsockopt CLIENT_WAITING, SOL_SOCKET, SO_REUSEADDR, 1 or die;
bind CLIENT_WAITING, pack_sockaddr_in($port, INADDR_ANY) or die;
listen CLIENT_WAITING, SOMAXCONN or die;

my %hash = ();
while (<>) {
	chomp;
	@_ = split /$separater/, $_, 2;
	unless (defined $hash{$_[0]}) {
		$hash{$_[0]} = [];
	}
	push @{$hash{$_[0]}}, $_[1];
}

while (1) {
	accept CLIENT, CLIENT_WAITING;
	select CLIENT; $|=1;

	if (fork) {
		close CLIENT;
		next;

	} else {
		$SIG{ALRM} = sub {kill "TERM", $$; die};
		alarm 600;
		while (<CLIENT>) {
			s/[\r\n]//g;
			if ($_ eq 0xFF) {
				last;
			} elsif (defined $hash{$_}) {
				my $a;
				foreach $a (@{$hash{$_}}) {
					print CLIENT $a, "\n";
				}
			}
			print "\n";
			alarm 600;
		}
		shutdown CLIENT, 2;
		close CLIENT;
		kill "TERM", $$;
		exit;
	}
}
