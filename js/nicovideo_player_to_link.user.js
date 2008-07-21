// ==UserScript==
// @name        Nicovideo Player to Link
// @namespace   http://fuktommy.com/js/
// @description Nicovideo external player wittern by script element to link.
// @include     http://mixi.jp/*
// @include     http://*.fc2.com/*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function playerToLink() {
        var scripts = document.getElementsByTagName('script');
        var pattern = new RegExp('http://[a-z0-9]+.nicovideo.jp/thumb_watch/([a-z]{2})([0-9]+)');
        for (var i=scripts.length-1; i>=0; i--) {
            if (scripts[i].src.search(pattern) == 0) {
                var cms = RegExp.$1;
                var num = RegExp.$2;
                var anchor = document.createElement('a');
                scripts[i].parentNode.insertBefore(anchor, scripts[i]);
                anchor.href = 'http://www.nicovideo.jp/watch/' + cms + num;
                anchor.appendChild(document.createTextNode(cms + num));
                var img = new Image();
                img.src='http://tn-skr.smilevideo.jp/smile?i=' + num;
                anchor.appendChild(img);
            }
        }
    }

    window.addEventListener('load', playerToLink, false);
})();
