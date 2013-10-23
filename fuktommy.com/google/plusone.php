<?php
//
// Google +1 をどのページにもつけるための中間ページ
//
// Copyright (c) 2011,2013 Satoshi Fukutomi <info@fuktommy.com>.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS ``AS IS'' AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
// OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
// HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
// LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
// OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
// SUCH DAMAGE.
//

require_once '../modchain/code/ModifireChain.php';

$defaultUrl = 'http://fuktommy.com/';
$url = empty($_GET['url']) ? $defaultUrl : $_GET['url'];
if ((! is_string($url)) || (! preg_match('<^https?://>', $url))) {
    $url = $defaultUrl;
}

$chain = ModifireChain::factory();
$chain->url = $url;

?>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <meta http-equiv="content-script-type" content="text/javascript" />
  <title>Google +1 中間ページ</title>
  <link rev="made" href="mailto:webmaster@fuktommy.com" />
  <link rel="contents" href="/" title="トップ" />
  <link rel="alternate" type="application/rss+xml" title="RSS" href="/rss" />
  <link rel="alternate" type="application/atom+xml" title="Blog Atom Feed" href="http://feeds.feedburner.com/fuktommy" />
  <link rel="meta" type="application/rdf+xml" title="license" href="/license" />
  <link rel="stylesheet" type="text/css" href="/common.css" />
  <link rel="stylesheet" type="text/css" href="/pc.css" media="screen" />
</head>
<body>
<h1>Google +1 中間ページ</h1>
<div>↓ここにボタンが出てこない人は残念でした。</div>
<div><g:plusone href="<?php $chain->url->e(); ?>" /></div>
<div><a href="<?php $chain->url->e(); ?>"><?php $chain->url->e(); ?></a></div>
<script src="http://apis.google.com/js/plusone.js">{lang: 'ja'}</script>

<div>ブックマークレット: <a href="javascript:location.href='http://fuktommy.com/google/plusone?url='+encodeURIComponent(location.href);">+1</a></div>
<div>ブックマークレット(別ウィンドウ開く版): <a href="javascript:(function(){window.open('http://fuktommy.com/google/plusone?url='+encodeURIComponent(location.href),'','width=800,height=600,scrollbars=no')})();">+1</a></div>

<p>ChromeでサードパーティのCookieをブロックしている場合には
設定→プライバシー→コンテンツの設定→Cookie→例外の管理で [*.]google.com を許可する必要があります。</p>

<div class="adsfoot" style="margin:2em">
<script type="text/javascript"><!--
amazon_ad_tag="fuktommy-22"; 
amazon_ad_width="468"; 
amazon_ad_height="60"; 
amazon_color_background="EFEFEF"; 
amazon_color_border="000000"; 
amazon_color_logo="FFFFFF"; 
amazon_color_link="0000FF"; //--></script> 
<script type="text/javascript" src="http://www.assoc-amazon.jp/s/asw.js"></script> 
<noscript> 
<br />
<iframe src="http://rcm-jp.amazon.co.jp/e/cm?t=fuktommy-22&amp;o=9&amp;p=13&amp;l=ez&amp;f=ifr&amp;f=ifr" width="468" height="60" scrolling="no" marginwidth="0" marginheight="0" frameborder="0" style="border:none;"></iframe>
</noscript> 
</div> 

<div style="text-align:center;font-style:italic;margin:2em">Copyright&copy; 2011,2013
<a href="https://plus.google.com/104787602969620799839" rel="auther">Fuktommy</a>.
All Rights Reserved.<br /> 
<a href="mailto:webmaster@fuktommy.com">webmaster@fuktommy.com</a> 
(<a rel="license" href="http://creativecommons.org/licenses/by/2.1/jp/" title="This work is licensed under a Creative Commons Attribution 2.1 Japan License.">Legal Notices</a>)
</div>
</body>
</html>
