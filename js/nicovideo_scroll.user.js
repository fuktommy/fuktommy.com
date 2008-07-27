// ==UserScript==
// @name        Nico Nico Video Scroll Viewer
// @namespace   http://fuktommy.com/js/
// @description J and K scroll viewer
// @include     http://www.nicovideo.jp/newarrival
// @include     http://www.nicovideo.jp/newarrival?page=*
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
    function Links() {
        this.links = [];
        this.index = 0;
    }
    Links.prototype.append = function(anchor) {
        this.links[this.links.length] = anchor;
    };
    Links.prototype.select = function(index) {
        this.index = index;
        if (this.links[index] != null) {
            if (index == 0) {
                window.scroll(0, 0);
            } else {
                window.scroll(0, this.links[index].offsetParent.offsetParent.offsetTop);
            }
            this.links[index].focus();
        }
    };
    Links.prototype.back = function() {
        if (this.index <= 0) {
            this.index = 0;
        } else {
            this.index--;
        }
        this.select(this.index)
    };
    Links.prototype.forward = function() {
        if (this.links.length - 1 <= this.index) {
            this.index = this.links.length - 1;
        } else {
            this.index++;
        }
        this.select(this.index)
    };
    Links.prototype.openWindow = function() {
        window.open(this.links[this.index].href);
    };
    var links = new Links();

    function makeListView() {
        // 戻るリンク
        var anchors = document.getElementsByTagName('a');
        for (var i = 0; i < anchors.length; i++) {
            if (anchors[i].className == 'prevpage') {
                links.append(anchors[i]);
                break;
            }
        }

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

        // 次へリンク
        var anchor = null;
        for (var i = 0; i < anchors.length; i++) {
            if (anchors[i].className == 'nextpage') {
                anchor = anchors[i];
            }
        }
        if (anchor != null) {
            links.append(anchor);
        }
        links.select(1);
    }

    function dispatchKeyPress(event) {
        if (event.ctrlKey || event.shiftKey) {
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

    function makeKeyBind() {
        window.addEventListener('keypress', dispatchKeyPress, false);
    }

    function init() {
        makeListView();
        makeKeyBind();
    }

    //window.addEventListener('init', modifyLinks, false);
    init();
})();
