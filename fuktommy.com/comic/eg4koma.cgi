#!/usr/bin/perl
#
# エニックスの4コマデータベース検索
#
# (c) FukTommy <fuktommy@my.tramonline.net>
#
# 2002/06/18	ver.0.0.1
#

# プロトタイプ宣言など
sub mydie(;$);
sub getArgv();
$file  = "eg4koma.dat";

# メッセージを受け取る
%argv    = getArgv;
$keyword = $argv{keyword};
$work    = $argv{work};

# 検索するかしないかを決定
if (($work eq "")&&($keyword eq "")) {
	select STDOUT;
	printHead();
	printTail();
	exit;
}

# ファイルを読む
open FILE, "$file" or mydie "$0: $file: $!";
$/ = "====\n";
@titles  = ();
@authors = ();
%titleof = ();
while (<FILE>) {
	s/====\n$//;
	next if ($_ eq "");
	@input = split /\n/;
	@line = ();
	while (($_ = shift @input) ne "----") {
		s/\s+/ /;
		push @line, $_;
	}
	$title = join " ", @line;
	push @titles, $title;
	foreach (@input) {
		push @authors, $_;
		$titleof{$_} .= $title . "\n";
	}
}

# 記事を作る
if ($work eq "作者一覧") {
	$title = "作者一覧";
	@body = uniq(@authors);
} elsif ($work eq "作品一覧") {
	$title = "作品一覧";
	@body = uniq(@titles);
} elsif ($keyword ne "") {
	$title = "$keyword の作品";
	@_ = split /\n/, $titleof{$keyword};
	@body = uniq(@_);
} else {
	select STDOUT;
	printHead();
	printTail();
	exit;
}

# 結果の表示
select STDOUT;
printHead();
print "<h2 align='center'>$title</h2>";
foreach (@body) {
	print "$_<br>\n";
}
printTail();


#-----------------------------------------------------------------------#
# ヘッダの出力
sub printHead {
	my $title = "エニックスゲーム4コマ非公式データベース";
	local $\ = "\n";
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head><body>";
	print "<h1 align='center'>$title</h1>";
	print "<form method='GET' action='eg4koma.cgi'>";
	print "<input name='keyword' size=50><br>";
	print "<input type='submit' value='作者名検索' name='work'>";
	print "<input type='submit' value='作者一覧' name='work'>";
	print "<input type='submit' value='作品一覧' name='work'>";
}

#-----------------------------------------------------------------------#
# フッタの出力
sub printTail {
	local $\ = "\n";
	print "<p align='right'>(c)FukTommy 2002",
	      " <a href='http://bbs.fuktommy.com/'>コメントをどうぞ</a></p>";
	print "</body></html>";
}

#-----------------------------------------------------------------------#
# ユニークなものだけ抽出
# 引数: 配列
sub uniq {
	local @_ = sort @_;
	my $tmp = $_[0];
	my @ret = ($_[0]);
	my $i;
	for ($i=1; $i<@_; $i++) {
		if ($_[$i] ne $tmp) {
			push @ret, $_[$i];
			$tmp = $_[$i];
		}
	}
	return @ret;
}


#-----------------------------------------------------------------------#
# dieの偽物
# 引数: [出力メッセージ]
sub mydie(;$) {
	select STDOUT;
	print "Content-type: text/html\n\n";
	print "<html><head><title>ERROR</title></head><body>\n";
	if (@_) {
		print @_;
	} else {
		print "$0: $!";
	}
	#print "<br><a href='$file'>掲示板に戻る</a><br>";
	print "</body></html>\n";
	exit 0;
}

#-----------------------------------------------------------------------#
# 引数をハッシュに格納する
# 戻値: ハッシュに格納された引数
# cgi-lib.pl((c) 1995 Steven E. Brenner)を基にしています
sub getArgv() {
	my (%argv, $in, $key, $val);
	$argv{METHOD} = $ENV{REQUEST_METHOD};
	if ($ENV{REQUEST_METHOD} eq "GET") {
		$in = $ENV{QUERY_STRING};
	} elsif ($ENV{REQUEST_METHOD} eq "POST") {
		read(STDIN,$in,$ENV{CONTENT_LENGTH});
	} else {
		mydie "$0: Unknown Method.\n";
	}

	@in = split(/[&;]/,$in);
	foreach (@in) {
		s/\+/ /g;
		($key, $val) = split(/=/, $_, 2);
		$key =~ s/%(..)/pack("c",hex($1))/ge;
		$val =~ s/%(..)/pack("c",hex($1))/ge;
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\r//g;
		$val =~ s/\n/<br>/g;
		$argv{$key} .= "\0" if (defined($in{$key}));
		$argv{$key} .= $val;
	}
	return %argv;
}
