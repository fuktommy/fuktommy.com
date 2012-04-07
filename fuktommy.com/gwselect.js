//
// shinGETsu - P2P anonymous BBS
//
// 新月リダイレクタ
//
// (c) shinGETsu Project
// Released under the Creative Commons License
//   http://creativecommons.org/licenses/by/2.0/jp/
//
// 使い方(1): printBody()
//   次のようなHTMLファイルを作る:
//     <html>
//	 <head><script type="text/javascript" src="shingetsu.js"></script></head>
//	 <body><script type="text/javascript">printBody();</script></body>
//     </html>
//
//   次のように呼び出す:
//     shingetsu.html
//     shingetsu.html?list.cgi/P2P
//
// 使い方(2): printForm(msg,path)
//   printForm(msg,path) を単独で呼び出す。
//   あらかじめ readCookie() を呼んでおくこと。
//
// 使い方(3): hiddenForm(id,msg,path)
//   次のようなHTMLファイルを作る:
//     <html>
//       <head><script type="text/javascript" src="shingetsu.js"></script></head><body>
//	 <a id="fooid" href="http://localhost/thread.cgi/foo">foomsg</a>
//	 <script type="text/javascript">
//	   readCookie();
//	   linkForm("fooid", "fooid_form");
//	   hiddenFormEntity("fooid_form", "foomsg", "/thread.cgi/foo");
//	 </script></body>
//     </html>
//
// printForm(msg,path)やhiddenForm(id,msg,path)を使う例では複数組み合わせることができます。
//
// 動作確認:
//   Mozilla Firefox 1.0
//   Microsoft Internet Explorer 6.0
//

//
// 各種変数
//
host = "bbs.shingetsu.info";
port = 80;
nForm = 0;

//
// クッキーを読み込み、変数を設定する
//
function readCookie() {
	buf = document.cookie + ";";
	done = 0;
	while (! done) {
		done = 1;
		n = 0;
		ikey = buf.indexOf("=", 0);
		ival = buf.indexOf(";", ikey);
		if ((ikey >= 0) && (ival > 0)) {
			done = 0;
			key  = buf.substr(0, ikey);
			val  = buf.substr(ikey+1, ival-ikey-1);
			if (key == "shingetsu_host") {
				host = val;
			} else if (key == "shingetsu_port") {
				port = val;
			}
			buf = buf.substr(ival+1, buf.length);

			isp = buf.indexOf(" ", 0);
			while (isp == 0) {
				buf = buf.substr(1, buf.length);
				isp = buf.indexOf(" ", 0);
			}
		}
	}
}

//
// クッキーを出力する
//
function printCookie(key, val) {
	day = new Date();
	year = day.getYear();
	if (year < 2000) {
		year += 1900;
	}
	day.setFullYear(year + 1);
	document.cookie = key + "=" + escape(val) +"; path=/; expires=" + day.toGMTString();
}

//
// ジャンプの動作
//
function jump(id) {
	host = document.getElementById(id).host.value;
	port = document.getElementById(id).port.value;
	path = document.getElementById(id).path.value;
	path = path.substr(1, path.length);
	printCookie("shingetsu_host", host);
	printCookie("shingetsu_port", port);
	location.href = "http://" + host + ":" + port + "/" + path;
}

//
// ジャンプ用のフォームを出力する
//
function printFormEntity(id, msg, path) {
	document.write('<form method="get" id="' + id +'" action="javascript:jump(\'' + id + '\')"><p class="jumpform">');
	document.write(msg + ": ");
	document.write('http://');
	document.write('<input name="host" accesskey="h" tabindex="1" />:');
	document.write('<input name="port" accesskey="p" tabindex="2" />/...');
	document.write('<input type="hidden" name="path" />');
	document.write('<input type="submit" name="submit" value="GO" accesskey="g" tabindex="3" />');
	document.write('</p></form>');

	document.getElementById(id).host.value = host;
	document.getElementById(id).port.value = port;
	document.getElementById(id).path.value = path;
}

//
// ジャンプ用のフォームを出力する(一式)
//
function printForm(msg, path) {
	id = "shingetsu" + nForm;
	printFormEntity(id, msg, path);
	nForm++;
}

//
// リンクの表示
//
function printLink() {
	document.write('<ul class="linklist">');
	document.write('<li><a href="http://shingetsu.sourceforge.net/">公式サイト</a></li>');
	document.write('<li><a href="http://bbs.shingetsu.info/">ゲートウェイ</a></li>');
	document.write('</ul>');
} 

//
// メッセージの表示
//
function printMotd() {
	document.write('<p class="gwmotd">次の条件に同意した方のみ新月ネットワークに参加できます。</p>');
	document.write('<ol class="gwmotd">');
	document.write('<li>投稿した記事に使用、改変または再配布の条件を記述するか、');
	document.write('それらを無制限に認めること。</li>');
	document.write('<li>違法行為に使わないこと。特に著作権を尊重すること。</li>');
	document.write('<li>荒らし行為をしないこと。</li>');
	document.write('</ol>');
}

//
// 表示のON/OFF
//
function showForm(id) {
	if (document.getElementById(id).style.display == "none") {
		document.getElementById(id).style.display = ""
	} else {
		document.getElementById(id).style.display = "none"
	}
}

//
// 隠し表示
//
function hiddenForm(id, msg, path) {
	printFormEntity(id, msg, path);
	document.getElementById(id).style.display = "none";
}

//
// 隠し表示のフォームとリンクの関連づけ
//
function linkForm(linkid, formid) {
	document.getElementById(linkid).href = 'javascript:showForm("' + formid +  '")';
}

//
// 一式の表示
//
function printBody() {
	readCookie();
	printForm("ゲートウェイの選択", location.search);
	printLink();
	printMotd();
}
