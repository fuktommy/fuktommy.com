<?php // -*- coding: utf-8 -*-

// local variables
$appRoot = __DIR__ . '/..';

// global settings
setlocale(LC_ALL, 'en_US.UTF-8');
date_default_timezone_set('Asia/Tokyo');
ini_set('user_agent', 'https://github.com/fuktommy/google-plus-feed');

// configration
return array(
    'google_api_key' => 'AIzaSyAMl46OeQC65XVPdTEinvPzZBqd00vwpkE',

    'site_top' => 'http://gpf.fuktommy.com/',
    'rights' => 'http://creativecommons.org/licenses/by/2.1/jp/',

    // PubSubHubbub. set empty to skip publish.
    'push_publisher' => 'https://pubsubhubbub.appspot.com/publish',

    'log_dir'         => "{$appRoot}/log",
    'gplus_cache_dir' => "{$appRoot}/tmp/gplus_cache",

    'smarty_template_dir' => "{$appRoot}/app/templates",
    'smarty_plugins_dir' => array("{$appRoot}/app/plugins"),
    'smarty_compile_dir' => "{$appRoot}/tmp/templates_c",
    'smarty_cache_dir' => "{$appRoot}/tmp/smarty_cache",

    'gplusfeed_default_userid' => '104787602969620799839', // Fuktommy

    'gplusfeed_userids' => array(
        '100234116023959363815',    // Shin Iwata
        '100890200991479840634',    // Tomoe Fukutomi
        '101341483406792705086',    // ssig33
        '101469377131638204516',    // Hiromi Ogata
        '102183698010783593298',    // 横田真俊
        '102354460982682319775',    // 赤井猫
        '104787602969620799839',    // Fuktommy
        '105684442055166146866',    // Hikaru Shimasaki
        '107002572043873162468',    // Masaki Yamada
        '108007043574812149024',    // 井原健紘
        '109147348593403414073',    // 鷹野凌
        '110737960632793111269',    // Masafumi Otsune
        '112667774340108374584',    // hiroyuki yamanaka
        '114835769462966948273',    // skame
        '115899767381375908215',    // Google Japan
    ),
);
