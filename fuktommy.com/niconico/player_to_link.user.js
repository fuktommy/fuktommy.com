// ==UserScript==
// @name        Nicovideo Player to Link
// @namespace   http://fuktommy.com/niconico/
// @description Nicovideo external player wittern by script element to link.
// @include     http://mixi.jp/*
// @include     http://*.fc2.com/*
// ==/UserScript==

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
