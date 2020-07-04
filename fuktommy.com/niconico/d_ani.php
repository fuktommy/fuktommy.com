<?php
$links = call_user_func(function () {
    $url = 'https://site.nicovideo.jp/danime/all_contents_1201.html';
    $key = "cache:http:$url";
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $html = $redis->get($key);
    if (! $html) {
        $html = file_get_contents($url);
        $redis->set($key, $html, 300);
    }
    $lines = explode("\n", $html);
    $links = [];
    foreach ($lines as $line) {
        if (preg_match('/\A<a href="([^"]+)">([^<]+)<\/a>\r*\z/', $line, $matches)) {
            $links[htmlspecialchars_decode($matches[1])] = htmlspecialchars_decode($matches[2]);
        }
    }
    return $links;
});
?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <title>dアニメニコニコ支店作品リストforはてなアンテナ</title>
</head>
<body>

<h1>dアニメニコニコ支店作品リストforはてなアンテナ</h1>
<p>オリジナルのページには改行がなくてはてなアンテナがうまく認識してくれないので。</p>

<ul>
<?php
    foreach ($links as $url => $title) {
        echo '<li><a href="', htmlspecialchars($url), '">', htmlspecialchars($title), "</a></li>\n"; 
    }
?>
</ul>

</body>
</html>
