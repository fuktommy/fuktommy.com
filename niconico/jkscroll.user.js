// ==UserScript==
// @name        Nico Nico Video Scroll Viewer
// @namespace   http://fuktommy.com/js/
// @description J and K scroll viewer for Nico Nico Video ranking, tag search and more.
// @include     http://www.nicovideo.jp/history
// @include     http://www.nicovideo.jp/hotlist
// @include     http://www.nicovideo.jp/mylist/*
// @include     http://www.nicovideo.jp/newarrival
// @include     http://www.nicovideo.jp/newarrival#*
// @include     http://www.nicovideo.jp/newarrival?page=*
// @include     http://www.nicovideo.jp/ranking/*
// @exclude     http://www.nicovideo.jp/ranking/*/ichiba
// @include     http://www.nicovideo.jp/recent
// @include     http://www.nicovideo.jp/recent#*
// @include     http://www.nicovideo.jp/recent?page=*
// @include     http://www.nicovideo.jp/search/*
// @include     http://www.nicovideo.jp/tag/*
// @include     http://www.nicovideo.jp/myvideo/*
// ==/UserScript==

// キー操作:
//      j:      下へ
//      k:      上へ
//      o:      新しいウィンドウ(タブ)で開く
//      v:      新しいウィンドウ(タブ)で開く
//      Enter:  開く

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

(function() {
    // ---- 各ページ共通 ---------------------------------------------------------------- //

    /**
     * 動画ページと前後のページへのリンクが入っている
     */
    function Links() {
        this.links = [];
        this.index = 0;
        this.prevPage = null;
        this.nextPage = null;
    }
    /**
     * 追加
     * anchor = {anchor: aタグのDOMオブジェクト, offset: Y軸のオフセット}
     */
    Links.prototype.push = function(anchor) {
        this.links.push(anchor);
    };
    /**
     * 逆方向からの追加
     * anchor = {anchor: aタグのDOMオブジェクト, offset: Y軸のオフセット}
     */
    Links.prototype.unshift = function(anchor) {
        this.links.unshift(anchor);
    };
    Links.prototype.select = function(index) {
        this.index = index;
        if (this.links[index] != null) {
            window.scroll(0, this.links[index].offset);
            this.links[index].anchor.focus();
        }
    };
    Links.prototype.back = function() {
        if (this.index <= 0) {
            this.index = 0;
            if (this.prevPage) {
                location.href = this.prevPage + '#bottom';
            }
        } else {
            this.index--;
        }
        this.select(this.index)
    };
    Links.prototype.forward = function() {
        if (this.links.length - 1 <= this.index) {
            this.index = this.links.length - 1;
            if (this.nextPage) {
                location.href = this.nextPage;
            }
        } else {
            this.index++;
        }
        this.select(this.index)
    };
    Links.prototype.openWindow = function() {
        if (this.links[this.index].anchor.href) {
            window.open(this.links[this.index].anchor.href);
        }
    };
    var links = new Links();

    /**
     * キーが押されたとき
     */
    function dispatchKeyPress(event) {
        if (event.ctrlKey || event.shiftKey || event.altKey) {
            return;
        }
        if (event.target.tagName == 'INPUT') {
            return;
        }
        var key = String.fromCharCode(event.which);
        if (key == 'j') {
            links.forward();
        } else if (key == 'k') {
            links.back();
        } else if ((key == 'o') || (key == 'v')) {
            links.openWindow();
        }
    }

    /**
     * ページの最下部に改行を入れる。
     * 最後の動画にスクロールしたとき左上に来るように。
     */
    function addLastSpace() {
        var div = document.createElement('div');
        document.body.appendChild(div);
        div.innerHTML = 'Powered by <a href="http://fuktommy.com/niconico/">JKScroll</a>.';
        div.style.textAlign = 'center';
        div.style.paddingTop = '500px';
    }

    /**
     * 初期フォーカス
     */
    function initFocus() {
        if (location.hash == '#bottom') {
            links.select(links.links.length - 1);
        } else {
            links.select(0);
        }
    }


    // ---- 検索ページ等 ---------------------------------------------------------------- //
    /**
     * 検索ページのナビゲーションリンク
     */
    function setNavigationForSearch() {
        var anchors = document.getElementsByTagName('a');
        for (var i = 0; i < anchors.length; i++) {
            if ((! links.prevPage) && (anchors[i].className == 'prevpage')) {
                links.prevPage = anchors[i];
            } else if (anchors[i].className == 'nextpage') {
                links.nextPage = anchors[i];
            }
        }
        if (links.prevPage) {
            links.unshift({anchor: links.prevPage, offset: 0});
        } else {
            links.unshift({anchor: anchors[0], offset: 0});
        }
    }

    /**
     * 検索ページの動画の並べ変え
     */
    function makeListViewForSearch() {
        if (document.getElementById('filtertext')) {
            var tableIndex = 1;
        } else {
            var tableIndex = 0;
        }

        // 動画一覧を探す
        var videoListSrc = document.getElementById('PAGEBODY')
                                   .getElementsByTagName('table')[tableIndex]
                                   .getElementsByTagName('table')[1];
        if (videoListSrc == null) {
            return;
        }

        // 動画一覧をコピー
        var videoListDst = document.createElement('div');
        videoListSrc.parentNode.insertBefore(videoListDst, videoListSrc);
        var videoInfos = videoListSrc.getElementsByTagName('div');
        for (var i = 0; i < videoInfos.length; i++) {
            if (videoInfos[i].className != 'thumb_frm') {
                continue;
            }
            var dst = document.createElement('div');
            videoListDst.appendChild(dst);
            dst.appendChild(videoInfos[i].cloneNode(true));
            videoInfos[i].innerHTML = '';
            videoInfos[i].style.display = 'none';
        }

        // 動画へのリンク
        var images = videoListDst.getElementsByTagName('img');
        for (var i = 0; i < images.length; i++) {
            if (images[i].className != 'video_w96') {
                continue;
            }
            var offsetBase = images[i].parentNode.offsetParent.offsetParent.parentNode;
            var anchor = {anchor: images[i].parentNode,
                          offset: offsetBase.offsetTop
                                + offsetBase.offsetParent.offsetParent.offsetTop
                                + offsetBase.offsetParent.offsetParent.offsetParent.offsetTop};
            links.push(anchor);
        }
    }


    // ---- ランキングページ ------------------------------------------------------------ //

    /**
     * ランキングページのナビゲーションリンク
     */
    function setNavigationForRanking() {
        var page = 1;
        if (location.search.search(/.page=([0-9]+)/) == 0) {
            page = Math.floor(RegExp.$1);
        }

        var baseurl = location.protocol + '//' + location.host + location.pathname;
        var prevPage = baseurl + '?page=' + (page - 1);
        var nextPage = baseurl + '?page=' + (page + 1);

        var anchors = document.getElementsByTagName('a');
        for (var i = 0; i < anchors.length; i++) {
            if (anchors[i].href == prevPage) {
                links.prevPage = prevPage;
            } else if (anchors[i].href == nextPage) {
                links.nextPage = nextPage;
            } else if ((links.prevPage == null) && (anchors[i].href == baseurl)) {
                links.prevPage = baseurl;
            }
        }
        links.unshift({anchor: anchors[0], offset: 0});
    }

    /**
     * ランキングの動画をリストに入れる
     */
    function addVideosForRanking() {
        var images = document.getElementsByTagName('img');
        for (var i = 0; i < images.length; i++) {
            if (images[i].className != 'video_w96') {
                continue;
            }
            var offsetBase = images[i].parentNode.offsetParent.offsetParent;
            var anchor = {anchor: images[i].parentNode,
                          offset: offsetBase.offsetTop
                                + offsetBase.offsetParent.offsetTop
                                + offsetBase.offsetParent.offsetParent.offsetTop
                                + offsetBase.offsetParent.offsetParent.offsetParent.offsetTop};
            links.push(anchor);
        }
    }


    // ---- ホットリスト ---------------------------------------------------------------- //
    /**
     * ホットリストのナビゲーションリンク
     */
    function setNavigationForHotlist() {
        var anchors = document.getElementsByTagName('a');
        links.unshift({anchor: anchors[0], offset: 0});
        links.nextPage = location.href;
    }

    /**
     * ホットリストの動画の並べ変え
     */
    function makeListViewForHotlist() {
        // 動画一覧を探す
        var videoListSrc = document.getElementById('PAGEBODY')
                                   .getElementsByTagName('table')[1]
                                   .getElementsByTagName('table')[0];
        if (videoListSrc == null) {
            return;
        }

        // 動画一覧をコピー
        var videoListDst = document.createElement('div');
        videoListSrc.parentNode.insertBefore(videoListDst, videoListSrc);
        var videoInfos = videoListSrc.getElementsByTagName('td');
        for (var i = 0; i < videoInfos.length; i++) {
            var dst = document.createElement('div');
            videoListDst.appendChild(dst);
            dst.appendChild(videoInfos[i].cloneNode(true));
            videoInfos[i].innerHTML = '';
        }

        // 動画へのリンク
        var images = videoListDst.getElementsByTagName('img');
        for (var i = 0; i < images.length; i++) {
            if (images[i].className != 'video_w96') {
                continue;
            }
            var offsetBase = images[i].parentNode.offsetParent.offsetParent.parentNode;
            var anchor = {anchor: images[i].parentNode,
                          offset: offsetBase.offsetTop
                                + offsetBase.offsetParent.offsetParent.offsetTop
                                + offsetBase.offsetParent.offsetParent.offsetParent.offsetParent.offsetTop};

            links.push(anchor);
        }
    }


    // ---- マイリスト ------------------------------------------------------------------ //
    /**
     * マイリストのナビゲーションリンク
     */
    function setNavigationForMylist() {
        var anchors = document.getElementsByTagName('a');
        links.unshift({anchor: anchors[0], offset: 0});
    }

    /**
     * マイリストの動画をリストに入れる
     */
    function addVideosForMylist() {
        var images = document.getElementsByTagName('img');
        for (var i = 0; i < images.length; i++) {
            if (images[i].className != 'video_w96') {
                continue;
            }
            var anchor = {anchor: images[i].parentNode,
                          offset: images[i].parentNode.offsetParent.offsetTop
                                + images[i].parentNode.offsetParent.offsetParent.offsetTop
                                + images[i].parentNode.offsetParent.offsetParent.offsetParent.offsetTop
                                + images[i].parentNode.offsetParent.offsetParent.offsetParent.offsetParent.offsetTop};
            links.push(anchor);
        }
    }

    // ---- 振り分け -------------------------------------------------------------------- //

    function init() {
        if (location.pathname.search(new RegExp('/ranking/')) == 0) {
            addVideosForRanking();
            setNavigationForRanking();
        } else if ((location.pathname.search(new RegExp('/mylist/')) == 0)
                || (location.pathname == '/history')) {
            addVideosForMylist();
            setNavigationForMylist();
        } else if (location.pathname == '/hotlist') {
            makeListViewForHotlist();
            setNavigationForHotlist();
        } else {
            makeListViewForSearch();
            setNavigationForSearch();
        }

        window.addEventListener('keypress', dispatchKeyPress, false);
        addLastSpace();
        initFocus();
    }

    window.addEventListener('load', init, false);
})();
