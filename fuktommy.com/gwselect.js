//
// shinGETsu - P2P anonymous BBS
//
// ���������쥯��
//
// (c) shinGETsu Project
// Released under the Creative Commons License
//   http://creativecommons.org/licenses/by/2.0/jp/
//
// �Ȥ���(1): printBody()
//   ���Τ褦��HTML�ե��������:
//     <html>
//	 <head><script type="text/javascript" src="shingetsu.js"></script></head>
//	 <body><script type="text/javascript">printBody();</script></body>
//     </html>
//
//   ���Τ褦�˸ƤӽФ�:
//     shingetsu.html
//     shingetsu.html?list.cgi/P2P
//
// �Ȥ���(2): printForm(msg,path)
//   printForm(msg,path) ��ñ�ȤǸƤӽФ���
//   ���餫���� readCookie() ��Ƥ�Ǥ������ȡ�
//
// �Ȥ���(3): hiddenForm(id,msg,path)
//   ���Τ褦��HTML�ե��������:
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
// printForm(msg,path)��hiddenForm(id,msg,path)��Ȥ���Ǥ�ʣ���Ȥ߹�碌�뤳�Ȥ��Ǥ��ޤ���
//
// ư���ǧ:
//   Mozilla Firefox 1.0
//   Microsoft Internet Explorer 6.0
//

//
// �Ƽ��ѿ�
//
host = "bbs.shingetsu.info";
port = 80;
nForm = 0;

//
// ���å������ɤ߹��ߡ��ѿ������ꤹ��
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
// ���å�������Ϥ���
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
// �����פ�ư��
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
// �������ѤΥե��������Ϥ���
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
// �������ѤΥե��������Ϥ���(�켰)
//
function printForm(msg, path) {
	id = "shingetsu" + nForm;
	printFormEntity(id, msg, path);
	nForm++;
}

//
// ��󥯤�ɽ��
//
function printLink() {
	document.write('<ul class="linklist">');
	document.write('<li><a href="http://shingetsu.sourceforge.net/">����������</a></li>');
	document.write('<li><a href="http://bbs.shingetsu.info/">�����ȥ�����</a></li>');
	document.write('</ul>');
} 

//
// ��å�������ɽ��
//
function printMotd() {
	document.write('<p class="gwmotd">���ξ���Ʊ�դ������Τ߿���ͥåȥ���˻��äǤ��ޤ���</p>');
	document.write('<ol class="gwmotd">');
	document.write('<li>��Ƥ��������˻��ѡ����Ѥޤ��Ϻ����ۤξ��򵭽Ҥ��뤫��');
	document.write('������̵���¤�ǧ��뤳�ȡ�</li>');
	document.write('<li>��ˡ�԰٤˻Ȥ�ʤ����ȡ��ä������º�Ť��뤳�ȡ�</li>');
	document.write('<li>�Ӥ餷�԰٤򤷤ʤ����ȡ�</li>');
	document.write('</ol>');
}

//
// ɽ����ON/OFF
//
function showForm(id) {
	if (document.getElementById(id).style.display == "none") {
		document.getElementById(id).style.display = ""
	} else {
		document.getElementById(id).style.display = "none"
	}
}

//
// ����ɽ��
//
function hiddenForm(id, msg, path) {
	printFormEntity(id, msg, path);
	document.getElementById(id).style.display = "none";
}

//
// ����ɽ���Υե�����ȥ�󥯤δ�Ϣ�Ť�
//
function linkForm(linkid, formid) {
	document.getElementById(linkid).href = 'javascript:showForm("' + formid +  '")';
}

//
// �켰��ɽ��
//
function printBody() {
	readCookie();
	printForm("�����ȥ�����������", location.search);
	printLink();
	printMotd();
}
