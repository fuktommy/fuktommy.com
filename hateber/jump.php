<?php
// -*- coding: utf-8 -*-

$now   = time();
$title = 'はてバーぶろぐ';
$base  = 'http://fuktommy.com/hateber/';

$ua = @$_SERVER['HTTP_USER_AGENT'];
if (preg_match('/DoCoMo|KDDI|SoftBank|Vodafone|J-PHONE/', $ua)) {
    $action = 'addmobile';
} else {
    $action = 'add';
}
header('Location: http://b.hatena.ne.jp/' . $action
        . '?mode=confirm'
        . '&title=' . urlencode($title . ' ' . strftime('%Y-%m-%d %H:%M:%S', $now))
        . '&url=' . urlencode($base . '#b' . strftime('%Y%m%d%H%M%S', $now))
);
