<?php
define('PC_FORMAT', 'http://astore.amazon.co.jp/fuktommy-22/detail/%s');
define('MOBILE_FORMAT', 'http://www.amazon.co.jp/gp/aw/rd.html?ie=UTF8&dl=1&uid=NULLGWDOCOMO' .
                        '&lc=msn&a=%s&at=fuktommysstor-22&url=%%2Fgp%%2Faw%%2Fd.html');

if (preg_match('|^/([-_.A-Za-z0-9]+)$|', $_SERVER['PATH_INFO'], $maches)) {
    $asin = $maches[1];
} else {
    header('Content-Type: text/plain');
    echo "$asin\n";
    echo 'Error';
}

$ua = $_SERVER['HTTP_USER_AGENT'];
if (preg_match('/DoCoMo|KDDI|SoftBank|Vodafone|J-PHONE/', $ua)) {
    header('Location: ' . sprintf(MOBILE_FORMAT, $asin));
} else {
    header('Location: ' . sprintf(PC_FORMAT, $asin));
}
?>
