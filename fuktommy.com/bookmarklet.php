<?php
$scriptURI = $_REQUEST['js'];
$title     = $_REQUEST['title'];
$scriptURI = preg_replace("/\"/", "\\\"", $scriptURI);
$jsstring = 'javascript:(function(){' .
            'var s=document.createElement("script");' .
            's.src="' . $scriptURI . '";' .
            'document.body.appendChild(s);' .
            '})();void(0);';
$url = parse_url($scriptURI);
if ((array_key_exists('host', $url) && ($url['host'] == 'fuktommy.com'))) {
    // pass
} else {
    $jsstring = '';
}
require_once('MySmarty.class.php');
$smarty = new MySmarty();
$smarty->assign('title', $title);
$smarty->assign('jsstring', $jsstring);
$smarty->display('bookmarklet.tpl');
?>
