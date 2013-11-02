<?php
//
// Google+ のフィード
//
// Copyright (c) 2011 Satoshi Fukutomi <info@fuktommy.com>.
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

$titleList = array(
    'Updated',
    '更新',
    'こうし～ん',
);

$chain = ModifireChain::factory();
$chain->accessTime = time();
$chain->title = $titleList[array_rand($titleList)];

header('Content-Type: text/xml; charset=UTF-8');

?>
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="/atomfeed.xsl" type="text/xsl"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Fuktommy - Google+</title>
  <subtitle>RSSリーダーのために自動生成されたエントリー</subtitle>
  <link rel="self" href="http://fuktommy.com/google/plusfeed" />
  <link rel="alternate" href="https://plus.google.com/+%E8%AB%AD%E7%A6%8F%E5%86%A8Fuktommy/posts" type="text/html"/>
  <updated><?php $chain->accessTime->dateFormat('%Y-%m-%dT%H:%M:%S+09:00')->e(); ?></updated>
  <generator>google/plusfeed tool</generator>
  <id>tag:fuktommy.com,2011:google/plus</id>
  <author><name>fuktommy</name></author>
  <entry>
    <title><?php $chain->title->e(); ?></title>
    <link rel="alternate" href="https://plus.google.com/+%E8%AB%AD%E7%A6%8F%E5%86%A8Fuktommy/posts?date<?php $chain->accessTime->dateFormat('%Y%m%d')->e(); ?>"/>
    <summary type="text"><?php $chain->title->e(); ?></summary>
    <content type="html"><?php $chain->title->e(); ?>: <a href="https://plus.google.com/+%E8%AB%AD%E7%A6%8F%E5%86%A8Fuktommy/posts">投稿</a>, <a href="https://plus.google.com/+%E8%AB%AD%E7%A6%8F%E5%86%A8Fuktommy/plusones">+1</a></content>
    <published><?php $chain->accessTime->dateFormat('%Y-%m-%dT%H:%M:%S+09:00')->e(); ?></published>
    <updated><?php $chain->accessTime->dateFormat('%Y-%m-%dT%H:%M:%S+09:00')->e(); ?></updated>
    <author><name>Fuktommy</name></author>
    <id>tag:fuktommy.com,2011:google/plus/<?php $chain->accessTime->dateFormat('%Y-%m-%d')->e(); ?></id>
    <rights>http://creativecommons.org/licenses/by/2.1/jp/</rights>
  </entry>
</feed>
