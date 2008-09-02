#!/usr/bin/perl
#
# Koe No Kakera.
#
# Copyright (C) 2000-2004 by Hiroshi Yuki.
# <hyuki@hyuki.com>
# http://www.hyuki.com/kakera/about.html
#
# This program is free software; you can redistribute it and/or
# modify it under the same terms as Perl itself.
#
##############################
# Libraries.
use strict;
use lib "/srv/lib/perl";
use CGI::Carp qw(fatalsToBrowser);
use Jcode;
use Data::Dumper;
use Yuki::Kakera;
##############################
my $modifier_profile = '<a href="http://fuktommy.com/">Fuktommy</a>';
my $modifier_mail = 'webmaster@fuktommy.com';
my $modifier_sendmail = "";
my $modifier_site_name = q(bbs.fuktommy.com);
my $modifier_site_url = "http://bbs.fuktommy.com/";
my $modifier_theme_dir = "/srv/www/bbs.fuktommy.com/theme/default";
my $modifier_theme_base_url = "http://bbs.fuktommy.com/theme/default";
my $modifier_data_dir = "/srv/data/bbs.fuktommy.com/files";
my $modifier_image_dir = "/srv/www/bbs.fuktommy.com/images";
my $modifier_image_base_url = "http://bbs.fuktommy.com/images/";
my $modifier_touch_file = "/srv/data/bbs.fuktommy.com/files/touched.txt";
my $modifire_spam_list = "/srv/data/bbs.fuktommy.com/spam.txt";
my $modifire_robot_list = "/srv/data/bbs.fuktommy.com/robotua.txt";
my $modifier_charset = "utf-8";
##############################
&main;
exit(0);

sub main {
    my $cgi = new Yuki::Kakera(
        PROFILE => $modifier_profile,
        SITE_NAME => $modifier_site_name,
        SITE_URL => $modifier_site_url,
        THEME_DIR => $modifier_theme_dir,
        THEME_BASE_URL => $modifier_theme_base_url,
        DATA_DIR => $modifier_data_dir,
        IMAGE_DIR => $modifier_image_dir,
        IMAGE_BASE_URL => $modifier_image_base_url,
        SPAM_LIST => $modifire_spam_list,
        ROBOT_LIST => $modifire_robot_list,
        use_html_permalink => 0,
        max_summary_length => 500,
        max_msg_length => 5000,
        max_recent_changes => 20,
        max_search_count => 20,
        max_post_length => 100*1024,
        hook_send_mail => \&hook_send_mail,
        hook_touch => \&hook_touch_file,
        hook_code_convert => \&hook_code_convert,
        hook_rss_code_convert => \&hook_rss_code_convert,
        # If you want to check the parameters, uncomment the following line.
        # debug => 1,
    );
    $cgi->run;
}

sub hook_code_convert {
    my ($valueref) = @_;
    &Jcode::convert($valueref, $modifier_charset);
}

sub hook_rss_code_convert {
    my ($valueref) = @_;
    &Jcode::convert($valueref, "utf8");
}

sub hook_touch_file {
    if ($modifier_touch_file) {
        open(FILE, "> $modifier_touch_file");
        print FILE localtime() . "\n";
        close(FILE);
    }
}

sub hook_send_mail {
    my ($id, $mode, $content) = @_;
    return unless $modifier_sendmail;
    my $message = <<"EOD";
To: $modifier_mail
From: $modifier_mail
Subject: [KAKERA]
MIME-Version: 1.0
Content-Type: text/plain; charset=ISO-2022-JP
Content-Transfer-Encoding: 7bit

--------
MODE = $mode
REMOTE_ADDR = $ENV{REMOTE_ADDR}
REMOTE_HOST = $ENV{REMOTE_HOST}
--------
${modifier_site_url}?$id
--------
$content
--------
EOD
    &Jcode::convert(\$message, 'jis');
    open(MAIL, "| $modifier_sendmail");
    print MAIL $message;
    close(MAIL);
}

1;
