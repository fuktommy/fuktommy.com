#!/usr/bin/perl
#
# ���˥å�����4���ޥǡ����١�������
#
# (c) FukTommy <fuktommy@my.tramonline.net>
#
# 2002/06/18	ver.0.0.1
#

# �ץ�ȥ���������ʤ�
sub mydie(;$);
sub getArgv();
$file  = "eg4koma.dat";

# ��å�������������
%argv    = getArgv;
$keyword = $argv{keyword};
$work    = $argv{work};

# �������뤫���ʤ��������
if (($work eq "")&&($keyword eq "")) {
	select STDOUT;
	printHead();
	printTail();
	exit;
}

# �ե�������ɤ�
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

# ��������
if ($work eq "��԰���") {
	$title = "��԰���";
	@body = uniq(@authors);
} elsif ($work eq "���ʰ���") {
	$title = "���ʰ���";
	@body = uniq(@titles);
} elsif ($keyword ne "") {
	$title = "$keyword �κ���";
	@_ = split /\n/, $titleof{$keyword};
	@body = uniq(@_);
} else {
	select STDOUT;
	printHead();
	printTail();
	exit;
}

# ��̤�ɽ��
select STDOUT;
printHead();
print "<h2 align='center'>$title</h2>";
foreach (@body) {
	print "$_<br>\n";
}
printTail();


#-----------------------------------------------------------------------#
# �إå��ν���
sub printHead {
	my $title = "���˥å���������4����������ǡ����١���";
	local $\ = "\n";
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head><body>";
	print "<h1 align='center'>$title</h1>";
	print "<form method='GET' action='eg4koma.cgi'>";
	print "<input name='keyword' size=50><br>";
	print "<input type='submit' value='���̾����' name='work'>";
	print "<input type='submit' value='��԰���' name='work'>";
	print "<input type='submit' value='���ʰ���' name='work'>";
}

#-----------------------------------------------------------------------#
# �եå��ν���
sub printTail {
	local $\ = "\n";
	print "<p align='right'>(c)FukTommy 2002",
	      " <a href='http://bbs.fuktommy.com/'>�����Ȥ�ɤ���</a></p>";
	print "</body></html>";
}

#-----------------------------------------------------------------------#
# ��ˡ����ʤ�Τ������
# ����: ����
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
# die�ε�ʪ
# ����: [���ϥ�å�����]
sub mydie(;$) {
	select STDOUT;
	print "Content-type: text/html\n\n";
	print "<html><head><title>ERROR</title></head><body>\n";
	if (@_) {
		print @_;
	} else {
		print "$0: $!";
	}
	#print "<br><a href='$file'>�Ǽ��Ĥ����</a><br>";
	print "</body></html>\n";
	exit 0;
}

#-----------------------------------------------------------------------#
# ������ϥå���˳�Ǽ����
# ����: �ϥå���˳�Ǽ���줿����
# cgi-lib.pl((c) 1995 Steven E. Brenner)���ˤ��Ƥ��ޤ�
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
