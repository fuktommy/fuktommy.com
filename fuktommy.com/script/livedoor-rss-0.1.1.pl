#!/usr/bin/perl -w
#
# livedoorで検索し、読み易い形式で表示する
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

sub encode($) {
	my($s) = @_;
        $s =~ s|[^\w]|'%' . uc(unpack('H2', $&))|eg;
        return $s;
}

sub decode($) {
	my($s) = @_;
	$s =~ s/\+/ /g;
	$s =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
	return $s;
}

sub args($) {
	local $_ = $_[0];
	local @_ = split /&/;
	my %arg = ();
	foreach (@_) {
		local @_ = split /=/;
		if (defined $_[1]) {
			$arg{$_[0]} = decode($_[1]);
		} else {
			$arg{$_[0]} = "";
		}
	}
	return %arg;	
}

sub search($$) {
	my($key, $start) = @_;
	my $str = encode($key);
	$start = 0 unless $start;
	my($IN, $OUT);
	open2($IN, $OUT, "wget", "-q", "-O", "-",
	"http://sf.livedoor.com/search?os=rss&q=$str&sf=update_date&start=$start");
	close $OUT;
	my $count = 0;
	print "<ul>\n";
	my @buf = <$IN>;
	close $IN;
	wait;
	$_ = join "", @buf;
	s/\s+/ /g;
	while (m|<item [^>]*>(.*?)</item>|) {
		$_ = $';
		my $str = $1;
		my ($link, $title) = ("", "");
		if ($str =~ m|<title>([^<]*)</title>|) {
			$title = $1;
		}
		if ($str =~ m|<link>([^<]*)</link>|) {
			$link = $1;
		}
		print "<li><a href='$link'>$title</li>\n";
		$count++;
	}
	print "</ul>";
	if ($start > 0) {
		print "<a href='$ENV{SCRIPT_NAME}?key=$str&amp;start=", $start-10, "'>",
			      "Prev</a>";
	} else {
		print "....";
	}
	print " | ";
	if ($count >= 10) {
		print "<a href='$ENV{SCRIPT_NAME}?key=$str&amp;start=", $start+10, "'>",
		      "Next</A>";
	} else {
		print "....";
	}
	print "</p>",
	      "</body></html>\n";
}

sub printForm($) {
	my($key) = @_;
	$key = "" unless ($key);
	my $title = ($key)? $key: "livedoor search";
	print "Content-Type: text/html; chaset=utf-8\n\n",
	      "<html><head><title>$title</title></head><body>\n",
	      "<form method='get' action='$ENV{SCRIPT_NAME}'><p>",
	      "<input name='key' value='$key'>",
	      "<input type='submit' name='search' value='search'>\n",
	      "</p></form>\n";
}

#
# メイン
#
my %arg = args($ENV{QUERY_STRING});
printForm($arg{key});
if ($arg{key}) {
	search($arg{key}, $arg{start});
} else {
	print "</body></html>\n";
}
