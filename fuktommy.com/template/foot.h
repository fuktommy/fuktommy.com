>>>ifndef TOPPAGE
</div>

<div id="sidebar">
>>>include "adsmini.h"
<form action="https://www.google.com/cse" id="searchbar"><p>
  <input type="hidden" name="cx" value="003570941829906538055:5apetotzz44" />
  <input type="hidden" name="ie" value="UTF-8" />
  <input type="text" name="q" size="31" id="searchbox" /><br />
  <input type="submit" value="検索" />
</p></form>
<script type="text/javascript" src="https://www.google.com/coop/cse/brand?form=searchbar&amp;lang=ja"></script>
>>>endif

<h2>リンク</h2>
<ul>
  <li><a href="/">トップ</a></li>
>>>ifdef SECTION
  <li><a href="./"><$SECTION></a></li>
>>>endif
  <li><a href="https://fuktommy.hatenablog.com/">ブログ</a></li>
</ul>

<h2>最近の記事</h2>
<script type="text/javascript" src="/recent.js"></script>

<h2>つながり</h2>
<ul>
  <li><a href="/rss">
      <img src="/feed-icon-16x16.gif" width="16" height="16" alt="" />
      RSS 1.0</a></li>
  <li><div class="p7-b" data-p7id="8b4d08a4415949e481b2975596b00778" data-p7c="r"></div>
      <script src="https://fuktommy.app.push7.jp/static/button/p7.js"></script></li>
  <li><a rel="license" href="https://creativecommons.org/licenses/by/2.1/jp/" title="This work is licensed under a Creative Commons Attribution 2.1 Japan License."><img alt="Creative Commons License" src="/cc-by-88x31.png" width="88" height="31" /></a></li>
</ul>

<p>Powered by <a href="/htmlpp/">Another HTMLPP</a>.</p>
</div>

<script type="text/javascript">
>>>ifdef TOPPAGE
  hideSideBar();
>>>else
  showSideBar();
>>>endif
</script>

>>>include "address.h"

</body>
</html>
