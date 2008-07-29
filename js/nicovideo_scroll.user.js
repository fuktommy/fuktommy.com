// ==UserScript==
// @name        Nico Nico Video Scroll Viewer
// @namespace   http://fuktommy.com/js/
// @description J and K scroll viewer
// @include     http://www.nicovideo.jp/newarrival
// @include     http://www.nicovideo.jp/newarrival?page=*
// @include     http://www.nicovideo.jp/recent
// @include     http://www.nicovideo.jp/recent?page=*
// @include     http://www.nicovideo.jp/search/*
// @include     http://www.nicovideo.jp/tag/*
// ==/UserScript==

// キー操作:
//      j:      下へ
//      k:      上へ
//      o:      新しいウィンドウ(タブ)で開く
//      v:      新しいウィンドウ(タブ)で開く
//      Enter:  開く

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    /**
     * 動画ページと前後のページへのリンクが入っている
     */
    function Links() {
        this.links = [];
        this.index = 0;
        this.firstLink = 0;
        this.prevPage = null;
        this.nextPage = null;
    }
    Links.prototype.append = function(anchor) {
        this.links[this.links.length] = anchor;
    };
    Links.prototype.select = function(index) {
        this.index = index;
        if (this.links[index] != null) {
            window.scroll(0, this.links[index].offsetParent.offsetParent.offsetTop);
            this.links[index].focus();
        }
    };
    Links.prototype.back = function() {
        if (this.index <= 0) {
            this.index = 0;
            if (this.prevPage) {
                location.href = this.prevPage;
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
        window.open(this.links[this.index].href);
    };
    var links = new Links();

    /**
     * 戻るリンク・次へリンク
     */
    function setNavigation() {
        var anchors = document.getElementsByTagName('a');
        for (var i = 0; i < anchors.length; i++) {
            if ((anchors[i].className == 'prevpage') && (! links.prevPage)) {
                links.prevPage = anchors[i].href + '#bottom';
            } else if (anchors[i].className == 'nextpage') {
                links.nextPage = anchors[i].href;
            }
        }
        links.firstLink = anchors[0];
    }

    /**
     * 動画の並べ変え
     */
    function makeListView() {
        // 動画一覧を探す
        var videoListSrc = null;
        var tables = document.getElementsByTagName('table');
        for (var i = 0; i < tables.length; i++) {
            if (tables[i].className == 'video_list') {
                videoListSrc = tables[i];
                break;
            }
        }
        if (videoListSrc == null) {
            return;
        }

        // 動画一覧をコピー
        var videoListDst = document.createElement('div');
        videoListSrc.parentNode.insertBefore(videoListDst, videoListSrc);
        var videoInfos = videoListSrc.getElementsByTagName('td');
        for (var i = 0; i < videoInfos.length; i++) {
            if (videoInfos[i].className != 'video_info') {
                continue;
            }
            var dst = document.createElement('div');
            videoListDst.appendChild(dst);
            dst.appendChild(videoInfos[i].cloneNode(true));
            videoInfos[i].innerHTML = '';
        }

        // 動画へのリンク
        var images = videoListDst.getElementsByTagName('img');
        for (var i = 0; i < images.length; i++) {
            if (images[i].className != 'thumb_img_M') {
                continue;
            }
            var anchor = images[i].parentNode;
            links.append(anchor);
        }
    }

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
        for (var i = 0; i < 10; i++) {
            document.body.appendChild(document.createElement('br'));
        }
    }

    function init() {
        makeListView();
        setNavigation();
        window.addEventListener('keypress', dispatchKeyPress, false);
        addLastSpace();
        if (location.hash == '#bottom') {
            links.select(links.links.length - 1);
        } else {
            links.index = -1;
            links.firstLink.focus();
        }
    }

    window.addEventListener('load', init, false);
})();
