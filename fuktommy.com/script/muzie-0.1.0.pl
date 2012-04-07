#!/usr/bin/perl -w
#
# muzie(http://www.muzie.co.jp/)の曲をアーティスト単位でランダムに取得
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

my $DIR		= "$ENV{HOME}/tmp/muzie";
my $HOST	= "www.muzie.co.jp";
my $RANDOM	= "http://$HOST/cgi-bin/random_song.cgi";
my $AGENT	= "Mozilla/4.0 (Muzie Viewer)";
my $WAIT	= 180;

sub pipe_wget($) {
	my($uri) = @_;
	my($IN, $OUT);
	open2 $IN, $OUT, "wget", "-U", $AGENT, "-T", 20, "-t", 2, "-O", "-", $uri;
	close $OUT;
	my @buf = <$IN>;
	close $IN;
	wait;
	return @buf;
}

sub file_wget($$) {
	my($dir, $uri) = @_;
	system "wget", "-U", $AGENT, "-T", 20, "-t", 2, "-nc", "-P", $dir, $uri;
}

while (1) {
	my @buf = pipe_wget($RANDOM);
	my $artist;
	foreach (@buf) {
		if (m|"/cgi-bin/artist\.cgi\?id=([^"]+)"|) {
			$artist = $1;
			last;
		}
	}
	if (defined $artist) {
		my @buf = pipe_wget("http://$HOST/cgi-bin/artist.cgi?id=$artist");
		my %file  = ();
		foreach (@buf) {
			while (m|<a href=['"]?([^'">]+)['"]?>|) {
				my $file = $1;
				$_ = $';
				if ($file =~ m|.*/([^/]+)\.([^./]+)|) {
					my($base, $suffix) = ($1, $2);
					if ($suffix eq "ram") {
						next;
					} elsif (($suffix eq "mp3") && (! $file{$base})) {
						$file{$base} = $file;
					} elsif ($suffix eq "ogg") {
						$file{$base} = $file;
					}
				}
			}
		}
		next unless (keys %file);
		mkdir $artist, 0777;
		open OUT, "> $artist/profile.html";
		print OUT @buf;
		close OUT;
		while (my($k, $v) = each(%file)) {
			file_wget($artist, "http://$HOST$v");
			sleep $WAIT;
		}
	}
}
