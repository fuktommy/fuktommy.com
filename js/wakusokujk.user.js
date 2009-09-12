// ==UserScript==
// @name        Wakusoku Scroll Viewer
// @namespace   http://fuktommy.com/js/
// @description J and K scroll for Wakusoku
// @include     http://blog.livedoor.jp/wakusoku/archives/*
// ==/UserScript==

// Copyright (c) 2009 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/wakusokujk.user.js
// Distributed under the new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function getImageList() {
        var divs = document.evaluate(
            "//div[@class='article-body-inner']", document, null,
            XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
        if (divs.snapshotLength != 1) {
            return [];
        }
        return divs.snapshotItem(0).getElementsByTagName('img');
    }

    function dispatchKeyPress(event) {
        if (event.ctrlKey || event.shiftKey || event.altKey) {
            return;
        }
        if (event.target.tagName == 'INPUT') {
            return;
        }
        var key = String.fromCharCode(event.which);
        if (key == 'j') {
            forward();
        } else if (key == 'k') {
            back();
        }
    }

    function forward() {
        if (imageList.length - 1 <= pointer) {
            return;
        }
        pointer++;
        scrollto(imageList[pointer]);
    }

    function back() {
        if (pointer <= 0) {
            return;
        }
        pointer--;
        scrollto(imageList[pointer]);
    }

    function scrollto(img) {
        var offset = img.offsetTop
                   + img.offsetParent.offsetTop
                   + img.offsetParent.offsetParent.offsetTop
                   - 10;
        window.scroll(0, offset);
    }

    var pointer = 0;
    var imageList = getImageList();
    if (1 <= imageList.length) {
        scrollto(imageList[0]);
    }
    window.addEventListener('keypress', dispatchKeyPress, false);
})();
