<?php
header('HTTP/1.0 404 Not Found', true, 404);
header('Content-Type: text/html; charset=UTF-8');
?>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <title>404 Not Found テストページ</title>
  <meta name="description" content="実際にはページあるんだけどね。" />
  <link rev="made" href="mailto:webmaster@fuktommy.com" />
  <link rel="contents" href="/" title="トップ" />
  <link rel="stylesheet" type="text/css" href="/common.css" />
  <link rel="stylesheet" type="text/css" href="/pc.css" media="screen" />
  <link rel="alternate" type="application/rss+xml" title="RSS" href="/rss" />
  <link rel="meta" type="application/rdf+xml" title="license" href="/license" />
</head>
<body>

<?php if (array_key_exists('p', $_REQUEST) && ($_REQUEST['p'] == '1')): ?>
    <h1>404 Not Foundサブページ</h1>
    <p>サブページも404だから、例えばブログツールに細工して、
       全ページを404にしたら面白いんじゃないかなあ。</p>
    <p>とりあえずFxとIE7では見れるみたいだよ。</p>
    <p><a href="404page">トップに戻る。</a></p>

<?php else: ?>
    <h1>404 Not Foundテストページ</h1>
    <p>このページは実際には存在して、こうやってブラウザでも読める(と思う)んだけど、
       HTTPのステータスコードが 404 Not Found なので、
       検索エンジンのロボットとかからは読めないじゃないかな。
       つまり検索避けとして使えると思う。</p>
    <p>ブクマ避けになるかは謎。無理かもね。</p>
    <p>こんな風に他のページも作っちゃったりして→<a href="404page?p=1">サブページ</a></p>
<?php endif; ?>

<address>Copyright&copy; 1998-2009 <a href="http://fuktommy.com/">Fuktommy</a>.
All Rights Reserved.<br />
<a href="mailto:webmaster@fuktommy.com">webmaster@fuktommy.com</a>
(<a rel="license" href="http://creativecommons.org/licenses/by/2.1/jp/" title="This work is licensed under a Creative Commons Attribution 2.1 Japan License.">Legal Notices</a>)
</address>

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

<script type="text/javascript" src="http://bbs.shingetsu.info/suggest.js" charset="utf-8"></script>
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-61877-7";
urchinTracker();
</script>
</body>
</html>
