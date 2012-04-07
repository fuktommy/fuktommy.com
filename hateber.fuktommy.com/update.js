//
// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
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
// $Id$
//

(function () {
    var autoUpdateCheckBox;
    var jumpLink;
    var hashDate;

    /**
     * 2桁の数字にする
     * @param int n
     * @return string
     */
    function formatNumber(n) {
        if (n <= 9) {
            return '0' + n;
        } else {
            return '' + n;
        }
    }

    /**
     * リンクを更新する
     */
    function updateLink() {
        if (autoUpdateCheckBox.checked) {
            setLink(new Date());
        }
        setTimeout(updateLink, 1000);
    }

    /**
     * リンクを設定する
     * @param Date date
     * @param bool updateTitle
     */
    function setLink(date, updateTitle) {
        var year    = date.getFullYear();
        var month   = formatNumber(date.getMonth() + 1);
        var day     = formatNumber(date.getDate());
        var hours   = formatNumber(date.getHours());
        var minutes = formatNumber(date.getMinutes());
        var seconds = formatNumber(date.getSeconds());

        var dateForLink  = '' + year + month + day + hours + minutes + seconds;
        var dateForTitle = '' + year + '-' + month + '-' + day
                         + ' ' + hours + ':' + minutes + ':' + seconds;

        var base = location.href.replace(/#.*/, '');
        var title = 'はてバーぶろぐ ' + dateForTitle;
        if (updateTitle) {
            document.title = title;
        }
        jumpLink.href  = 'http://b.hatena.ne.jp/add?'
                       + 'mode=confirm'
                       + '&title=' + encodeURIComponent(title)
                       + '&url=' + encodeURIComponent(base + '#b' + dateForLink)
    }

    /**
     * ブックマークレットを更新する
     */
    function updateBookmarklet() {
        var bookmarklet = document.getElementById('bookmarklet');
        var base = location.href.replace(/#.*/, '');
        bookmarklet.href = "javascript:(function(){"
                         + "var s=document.createElement('script');"
                         + "s.src='" + base + "bookmarklet.js';"
                         + "s.charset='utf-8';"
                         + "document.body.appendChild(s);"
                         + "})();void(0);";
    }

    /**
     * 初期化
     */
    function init() {
        jumpLink = document.getElementById('jump');
        autoUpdateCheckBox = document.getElementById('autoUpdate');

        if (location.hash == '') {
            autoUpdateCheckBox.checked = true;
        } else if (location.hash.search(/^#b([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})$/) == 0) {
            hashDate = new Date(RegExp.$1, RegExp.$2 - 1, RegExp.$3, RegExp.$4, RegExp.$5, RegExp.$6);
            setLink(hashDate, true);
        }

        updateLink();
        updateBookmarklet();
    }

    if (window.addEventListener) {
        window.addEventListener('load', init, false);
    } else if (window.attachEvent) {
        window.attachEvent('onload', init);
    }
})();
