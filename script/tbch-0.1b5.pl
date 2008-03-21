#!/usr/bin/perl
#
# とらばちゃんねる
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

my $SELF_URI		= "/tbch.cgi";
my $ABS_URI		= "http://fuktommy.s64.xrea.com/tbch.cgi";
my $DATA_DIR		= "/virtual/fuktommy/private/tbch";
my $TITLE		= "とらばちゃんねる";
my $DESCRIPTION		= "トラックバックで作る分散掲示板";
my $MAIL_ADDRESS	= 'fuktommy@inter7.jp';
my $SYSTEM		= "とらばちゃんねる";
umask 0000;

#
# メッセージ
#
my %message = (
	rss	=> "RSS",
	edit	=> "管理モード",
	name	=> "名前",
	nextis	=> "続きはこちら",
	anonymous=> "名無しさん",
	trackback=> "トラックバック",
	description=> "トラックバックで作る掲示板です。" .
		      "あなたのBlogに「スレッド」を作って、下のURLにトラックバックしてください。",
);

#----------------------------------------------------------------#

#
# lock
#
sub lock() {
	open LOCK, "> $DATA_DIR/lock";
	flock LOCK, 002;
}
sub unlock() {
	close LOCK;
}

#
# encode/decode
#
sub escape($) {
	local($_) = @_;
	s/&/&amp;/g;
	s/&amp;(#\d+|#[Xx][0-9A-Fa-f]+|[A-Za-z0-9]+);/&$1;/g;
	s/</&lt;/g;
	s/>/&gt;/g;
	s/"/&quot;/g;
	s/\r//g;
	s|\n|<br />|g;
	return $_;
}
sub decode($;%) {		# Thanks for YukiWiki
	my($s, %opt) = @_;
	$s =~ s/\+/ /g;
	$s =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
	if ($opt{raw}) {
		return $s;
	} else {
		return escape($s);
	}
}

#
# 日付
#
sub w3c_time($) {
	my @buf  = gmtime($_[0]);
	return sprintf "%d-%02d-%02dT%02d:%02d:%02dZ",
		       1900+$buf[5], 1+$buf[4], $buf[3], $buf[2], $buf[1], $buf[0];
}

#
# 引数
#
sub args($) {
	local $_ = $_[0];
	local @_ = split /&/;
	my %arg = ();
	foreach (@_) {
		local @_ = split /=/;
		if ($_[0] eq "body") {
			$arg{$_[0]} = decode($_[1], raw=>1);
		} elsif (defined $_[1]) {
			$arg{$_[0]} = decode($_[1]);
		} else {
			$arg{$_[0]} = "";
		}
	}
	return %arg;	
}

#
# パスワード
#
sub setPasswd($) {
	my($passwd) = @_;
	lock();
	open OUT, "> $DATA_DIR/passwd";
	print OUT crypt($passwd, sprintf("%02X", 256*rand));
	unlock();
}
sub checkPasswd($) {
	my($passwd) = @_;
	return 1 unless (-s "$DATA_DIR/passwd");
	open IN, "$DATA_DIR/passwd" or return 1;
	local $_ = <IN>;
	close IN;
	return $_ eq crypt $passwd, $_;
}

#
# 文字コードの変換
#
sub jcode_convert(%) {
	use Jcode;
	my(%opt) = @_;
	local $_;
	foreach (keys %opt) {
		if ($opt{charset} =~ /UTF-?8/i) {
			$opt{$_} = Jcode->new($opt{$_}, "utf8")->euc;
		} elsif ($opt{charset} =~ /SHIFT_JIS/i) {
			$opt{$_} = Jcode->new($opt{$_}, "sjis")->euc;
		} elsif ($opt{charset} =~ /EUC-JP/i) {
			$opt{$_} = Jcode->new($opt{$_}, "euc")->euc;
		} elsif ($opt{charset} =~ /ISO-2022-JP/i) {
			$opt{$_} = Jcode->new($opt{$_}, "jis")->euc;
		} else {
			$opt{$_} = Jcode->new($opt{$_})->euc;
		}
	}
	return %opt;
}

#
# レコード
#
sub rec($) {
	local($_) = @_;
	s/\s*$//;
	@_ = split /<>/, $_, 5;
	my %buf = ( date      => $_[0],
		    blog_name => $_[1],
		    title     => $_[2],
		    url	      => $_[3],
		    excerpt   => $_[4],
		  );
	return %buf;
}
sub rec_join(%) {
	my(%rec) = @_;
	return "$rec{date}<>$rec{blog_name}<>$rec{title}<>$rec{url}<>$rec{excerpt}";
}

#
# ファイル入出力
# $opt{mode} opt{raw}
#
sub readFile(%) {
	my(%opt) = @_;
	if (open IN, "$DATA_DIR/data") {
		local $_;
		my @buf = ();
		while (<IN>) {
			if ($opt{raw}) {
				push @buf, $_;
			} else {
				my %rec = rec($_);
				push @buf, \%rec;
			}
		}
		close IN;
		return @buf;
	} else {
		return ();
	}
}
sub writeFile($%) {
	my($body, %opt) = @_;
	my $mode = ($opt{mode})? $opt{mode}: ">";
	my @buf = ();
	lock();
	if (open OUT, "$mode $DATA_DIR/data") {
		print OUT $body;
		close OUT;
		unlock();
	} else {
		unlock();
		return 0;
	}
	return 1;
}
sub stamp() {
	my @stat = stat "$DATA_DIR/data";
	return $stat[9] || 0;
}

#----------------------------------------------------------------#

#
# 日時
#
sub xlocaltime($) {
	my @buf = localtime($_[0]);
	return sprintf "%d-%02d-%02d %02d:%02d",
		       1900+$buf[5], $buf[4]+1, $buf[3], $buf[2], $buf[1];
}

#
# XMLレスポンス
#
sub printOK() {
	print "Content-Type: text/xml\r\n",
	      "\r\n",
	      "<?xml version='1.0' encoding='iso-8859-1'?>\n",
	      "<response>\n",
	      "  <error>0</error>\n",
	      "</response>\n";
}
sub printError(;$) {
	my $message = (@_)? $_[0]: "Error";
	print "Content-Type: text/xml\r\n",
	      "\r\n",
	      "<?xml version='1.0' encoding='iso-8859-1'?>\n",
	      "<response>\n",
	      "  <error>1</error>\n",
	      "  <message>$message</message>\n",
	      "</response>\n";
}

#
# ヘッダとか
# $opt{deny_robot}
#
sub printHeader($%) {
	my($title, %opt) = @_;
	local $_;
	$title = "" unless (defined $title);
	print "Content-Type: text/html; charset=EUC-JP\r\n";
	print "\r\n",
	      "<?xml version='1.0' encoding='EUC-JP'?>\n",
	      "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'\n",
	      "  'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n",
	      "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='ja'>\n",
	      "<head>\n",
	      "  <meta http-equiv='Content-Style-Type' content='text/css' />\n",
	      "  <meta http-equiv='Content-Type' content='text/html; charset=EUC-JP' />\n",
	      "  <meta name='description' content='$DESCRIPTION' />\n";
	print "  <meta name='robots' content='NOINDEX, NOFOLLOW' />\n" if ($opt{deny_robot});
	print "  <title>$title</title>\n",
	      "  <link rev='made' href='mailto:$MAIL_ADDRESS' />\n",
	      "  <link rel='contents' href='$SELF_URI' />\n",
	      "  <link rel='alternate' type='application/rdf+xml' title='RSS' href='$SELF_URI?rss' />\n",
	      "  <style type='text/css'>\n",
	      "    body { background-color: #d0b098; }\n",
	      "    h2 { color: red; }\n",
	      "    .title { background-color: #cfc; }\n",
	      "    .list { background-color: #cfc; }\n",
	      "    .thread { background-color: #efefef; }\n",
	      "    .responce { margin-left: 40px; }\n",
	      "	   .title, .list, .thread { padding: 10px; margin: 30px; border-style: double; }\n",
	      "	   .name { color: green; font-weight: bold; }\n",
	      "  </style>\n",
	      "</head>\n",
	      "<body>\n";
}

#
# フッタ
#
sub printFooter() {
	print "<p class='footer'>",
	      "<a href='$SELF_URI?rss'>$message{rss}</a> |\n",
	      "<a href='$SELF_URI?edit'>$message{edit}</a><br />\n",
	      "Powered by <a href='http://fuktommy.s64.xrea.com/'>$SYSTEM</a>.",
	      "</p>\n",
	      "<p><a href='http://img.xrea.com/ad_click.fcg?site=fuktommy.s64.xrea.com'><img src='http://img.xrea.com/ad_img.fcg?site=fuktommy.s64.xrea.com' height='60' width='468' alt='広告' style='border-width: 0px' /></a></p>\n";
	      "</body>\n</html>\n";
}

#
# タイトル
#
sub printTitle() {
	print "<div class='title'>\n",
	      "<h1>$TITLE</h1>\n",
	      "<p>$message{description}</p>\n",
	      "<p>$message{trackback}URL: $ABS_URI?trackback</p>\n";
	print "<!--\n",
	      "  <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\n",
	      "     xmlns:dc='http://purl.org/dc/elements/1.1/'\n",
	      "     xmlns:trackback='http://madskills.com/public/xml/rss/module/trackback/'>\n",
	      "  <rdf:Description\n",
	      "    rdf:about='$ABS_URI'\n",
	      "    dc:identifer='$ABS_URI'\n",
	      "    dc:title='$TITLE'\n",
	      "    trackback:ping='$ABS_URI?trackback' />\n",
	      "  </rdf:RDF>\n",
	      "-->\n";
	print "</div>\n";
}

#
# 「スレッド」のリスト
#
sub printList(@) {
	my @data = @_;
	my $i = 1;
	local $_;
	print "<p class='list'>\n";
	foreach (@data) {
		print "<a href=\"$$_{url}\">$i:</a> <a href='#r$i'>$$_{title}</a>&ensp;\n";
		$i++;
	}
	print "</p>\n";
}

#
# 「スレッド」の中身表示
#
sub printThread(@) {
	my @data = @_;
	my $i = 1;
	local $_;
	foreach (@data) {
		print "<div class='thread' id='r$i'>\n",
		      "<h2>$$_{title}</h2>\n",
		      "<p>1 $message{name}: <span class='name'>$$_{blog_name}</span> ",
		      xlocaltime($$_{date}), "</p>\n",
		      "<p class='responce'>$$_{excerpt}</p>\n",
		      "<p>2 $message{name}: <span class='name'>$message{anonymous}</span> ",
		      xlocaltime($$_{date}), "</p>\n",
		      "<p class='responce'>$message{nextis}<br /><a href=\"$$_{url}\">$$_{url}</a></p>\n",
		      "</div>\n";
		$i++;
	}
}

#
# RSS1.0
#
sub printRssPage() {
	local $_;
	my @data = reverse readFile();
	print "Content-Type: text/xml; charset=EUC-JP\r\n",
	      "\r\n",
	      "<?xml version='1.0' encoding='EUC-JP'?>\n",
	      "<rdf:RDF\n",
	      "  xmlns='http://purl.org/rss/1.0/'\n",
	      "  xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\n",
	      "  xmlns:dc='http://purl.org/dc/elements/1.1/'\n",
	      "  xml:lang='ja'>\n",
	      "<channel rdf:about='$ABS_URI?rss'>\n",
	      "  <title>$TITLE</title>\n",
	      "  <link>$ABS_URI</link>\n",
	      "  <description>$DESCRIPTION</description>\n",
	      "  <items><rdf:Seq>\n";
	foreach (@data) {
		print "    <rdf:li rdf:resource='$$_{url}' />\n";
	}
	print "  </rdf:Seq></items>\n</channel>\n";
	foreach (@data) {
		my $date = w3c_time($$_{date});
		print "<item rdf:about='$$_{url}'>\n",
		      "  <title>$$_{title}</title>\n",
		      "  <link>$$_{url}</link>\n",
		      "  <dc:date>$date</dc:date>\n",
		      "  <description>$$_{excerpt}</description>\n",
		      "</item>\n";
	}
	print "</rdf:RDF>\n";
}

#
# 「板」の表示
#
sub printBoard() {
	printHeader($TITLE);
	printTitle();
	my @data = reverse readFile();
	printList(@data);
	printThread(@data);
	printFooter();
}

#
# 編集ページ
#
sub printEdit() {
	printHeader($message{edit}, deny_robot=>1);
	print "<form method='post' action='$SELF_URI?setpasswd'><p>\n",
	      "Old Password <input type='password' name='oldpasswd' tabindex='1' accesskey='o' /><br />\n",
	      "New Password <input type='password' name='newpasswd' tabindex='2' accesskey='n' /><br />\n",
	      "New Password <input type='password' name='newpasswd2' tabindex='3' accesskey='m' /><br />\n",
	      "<input type='submit' value='SET' name='submit' tabindex='4' accesskey='s' />",
	      "</p></form>\n";

	local $_;
	my @buf = readFile(raw=>1);
	my $date = time;
	print "<form method='post' action='$SELF_URI?post'><p>\n",
	      "<input type='hidden' name='date' value='$date' />\n",
	      "<input type='submit' value='POST' name='submit' tabindex='7' accesskey='w' />",
	      "Password <input type='password' name='passwd' tabindex='5' accesskey='p' /><br />\n",
	      "<textarea name='body' rows='40' cols='80' tabindex='6' accesskey='e'>";
	foreach (@buf) {
		chomp;
		print escape($_), "\n";
	}
	print "</textarea>\n</p></form>\n";

	printFooter();
}

#
# パスワードの変更
#
sub passwd($$$) {
	my($old, $new, $new2) = @_;
	if ($new ne $new2) {
		printError("Not same password");
		exit;
	} elsif (! checkPasswd($old)) {
		printError("Wrong password");
		exit;
	} else {
		setPasswd($new);
	}
	printOK();
}

#
# データの編集
#
# $opt{body}, $opt{stamp}, $opt{passwd}
#
sub post(%) {
	my(%opt) = @_;
	if (! checkPasswd($opt{passwd})) {
		printError("Wrong password");
	} elsif ($opt{date} <= stamp()) {
		printError("Conflict");
	} elsif (writeFile($opt{body})) {
		printOK();
	} else {
		printError();
	}
}

#
# トラックバックを受ける
#
sub trackback(%) {
	my(%opt) = @_;
	%opt = jcode_convert(%opt);
	$opt{date} = time;
	my $body = rec_join(%opt) . "\n";
	if ($opt{url} && writeFile($body, mode=>">>")) {
		printOK();
	} else {
		printError();
	}
}

#----------------------------------------------------------------#

my %arg;
if ($ENV{REQUEST_METHOD} ne "POST") {
	%arg = args($ENV{QUERY_STRING});

} else {
	my $input;
	read(STDIN, $input, $ENV{CONTENT_LENGTH});
	$input .= "&$ENV{QUERY_STRING}";
	%arg = args($input);
}

if (defined $arg{edit}) {
	printEdit();

} elsif (defined $arg{post}) {
	post(%arg);

} elsif (defined $arg{rss}) {
	printRssPage();

} elsif (defined $arg{trackback}) {
	trackback(%arg);

} elsif (defined $arg{setpasswd}) {
	passwd($arg{oldpasswd}, $arg{newpasswd}, $arg{newpasswd2});

} else {
	printBoard();
}



