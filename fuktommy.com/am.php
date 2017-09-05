<?php
define('PC_FORMAT', 'https://www.amazon.co.jp/dp/%s?tag=fuktommy-22');
define('MOBILE_FORMAT', 'http://www.amazon.co.jp/gp/aw/rd.html?ie=UTF8&dl=1&uid=NULLGWDOCOMO' .
                        '&lc=msn&a=%s&at=fuktommysstor-22&url=%%2Fgp%%2Faw%%2Fd.html');

if (preg_match('|^/([-_.A-Za-z0-9]+)$|', $_SERVER['PATH_INFO'], $maches)) {
    $asin = $maches[1];
} else {
    $asin = null;
}

$ua = $_SERVER['HTTP_USER_AGENT'];
if (! $asin) {
    // pass
} elseif (preg_match('/Google Wireless Transcoder|Hatena/', $ua)) {
    // pass
} elseif (preg_match('/DoCoMo|KDDI|SoftBank|Vodafone|J-PHONE/', $ua)) {
    header('Location: ' . sprintf(MOBILE_FORMAT, $asin));
} else {
    header('Location: ' . sprintf(PC_FORMAT, $asin));
}
header('Content-Type: text/html; charset=UTF-8');

?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <title>Jump to Amazon.co.jp</title>
  <link rev="made" href="http://fuktommy.com/" />
  <link rel="contents" href="/" title="Top" />
  <?php if ($asin): ?>
    <link rel="alternate" media="handheld"
          href="<?php echo htmlspecialchars(sprintf(MOBILE_FORMAT, $asin), ENT_QUOTES); ?>" />
  <?php endif; ?>
</head>
<body>
<div>
  <?php if ($asin): ?>
    <a href="<?php echo htmlspecialchars(sprintf(PC_FORMAT, $asin), ENT_QUOTES); ?>">Next</a>
  <?php else: ?>
    Error
  <?php endif; ?>
</div>

<!--
<rdf:RDF
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:foaf="http://xmlns.com/foaf/0.1/">
<rdf:Description rdf:about="http://fuktommy.com/">
   <foaf:maker rdf:parseType="Resource">
     <foaf:holdsAccount>
       <foaf:OnlineAccount foaf:accountName="fuktommy">
         <foaf:accountServiceHomepage rdf:resource="http://www.hatena.ne.jp/" />
       </foaf:OnlineAccount>
     </foaf:holdsAccount>
   </foaf:maker>
</rdf:Description>
</rdf:RDF>
-->

</body>
</html>
