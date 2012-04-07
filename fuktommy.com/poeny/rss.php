<?php
/* -*- coding: utf-8 -*- */
/* Copyright (c) 2007 Satoshi Fukutomi <info@fuktommy.com>. */

require_once('RSS.class.php');

$rss = new RSS('Poeny mirror',
               'http://fuktommy.com/poeny/',
               'http://fuktommy.com/poeny/rss',
               'Poeny is a colne of Winny.');
$suffix = array('tar.gz', 'zip', 'diff', 'diff.gz', 'exe.bz2');
foreach ($suffix as $s) {
    foreach (glob('*.' . $s) as $f) {
        $rss->append(array('title' => $f,
                           'date'  => filemtime($f),
                           'link'  => 'http://fuktommy.com/poeny/' . $f,
                    ));
    }
}
header('Content-Type: text/xml; charset=UTF-8');
$rss->display();

?>
