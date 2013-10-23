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
  <li><a href="https://plus.google.com/104787602969620799839?rel=author" rel="author">ブログ</a></li>
  <li><a href="http://bbs.fuktommy.com/">掲示板</a></li>
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
  <li><form action="https://www.paypal.com/cgi-bin/webscr" method="post"><div>
        <input type="hidden" name="cmd" value="_s-xclick" />
        <input type="hidden" name="hosted_button_id" value="7210101" />
        <input type="image" src="https://www.paypal.com/ja_JP/JP/i/btn/btn_paynow_SM.gif" name="submit" alt="PayPal - オンラインで安全・簡単にお支払い" />
        <img alt="" src="https://www.paypal.com/ja_JP/i/scr/pixel.gif" width="1" height="1" />
      </div></form></li>
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
