>>>ifndef TOPPAGE
</div>

<div id="sidebar">
>>>endif
>>>ifdef AMAZONADS
>>>include "amazonwidget.h"
>>>else
>>>ifndef TOPPAGE
>>>include "adsmini.h"
>>>endif
>>>include "amazonbanner.h"
>>>endif

>>>ifndef TOPPAGE
<form action="http://www.google.com/cse" id="searchbar"><p>
  <input type="hidden" name="cx" value="003570941829906538055:5apetotzz44" />
  <input type="hidden" name="ie" value="UTF-8" />
  <input type="text" name="q" size="31" id="searchbox" /><br />
  <input type="submit" value="検索" />
</p></form>
<script type="text/javascript" src="http://www.google.com/coop/cse/brand?form=searchbar&amp;lang=ja"></script>
>>>endif

<h2>リンク</h2>
<ul>
  <li><a href="/">トップ</a></li>
>>>ifdef SECTION
  <li><a href="./"><$SECTION></a></li>
>>>endif
  <li><a href="http://blog.fuktommy.com/">ブログ</a></li>
  <li><a href="http://b.hatena.ne.jp/fuktommy/">はてなブックマーク</a></li>
  <li><a href="http://bbs.fuktommy.com/">掲示板</a></li>
  <li><a href="http://mixi.jp/show_friend.pl?id=30173">mixi/fuktommy</a></li>
  <li><a href="http://bbs.shingetsu.info/" id="shingetsu_link" title="関連する新月の掲示板">shinGETsu</a></li>
</ul>

<h2>最近の記事</h2>
<script type="text/javascript" src="/recent.js"></script>

<h2>つながり</h2>
<ul>
  <li><a href="http://bbs.fuktommy.com/">コメント</a></li>
  <li><a href="/rss">
      <img src="/feed-icon-16x16.gif" width="16" height="16" alt="" />
      RSS 1.0</a></li>
  <li><a href="http://fusion.google.com/add?feedurl=http%3A//fuktommy.com/rss"><img src="http://buttons.googlesyndication.com/fusion/add.gif" width="104" height="17" alt="Add to Google" /></a></li>
  <li><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;business=paypal%40fuktommy%2ecom&amp;item_name=Fuktommy%2ecom&amp;amount=500&amp;no_shipping=0&amp;no_note=1&amp;tax=0&amp;currency_code=JPY&amp;bn=PP%2dDonationsBF&amp;charset=UTF%2d8"><img src="/donate.gif" alt="Make payments with PayPal" width="73" height="44" /></a></li>
  <li><a rel="license" href="http://creativecommons.org/licenses/by/2.1/jp/" title="This work is licensed under a Creative Commons Attribution 2.1 Japan License."><img alt="Creative Commons License" src="/cc-by-88x31.png" width="88" height="31" /></a></li>
  <li><a href="http://mobile.fuktommy.com/"><img src="/mobileqrcode.gif" width="132" height="132" alt="モバイルサイト" title="モバイルサイト" /></a></li>
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
