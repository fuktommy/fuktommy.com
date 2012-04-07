// ==UserScript==
// @name        Alt to Title
// @namespace   http://fuktommy.com/js/
// @description Accent recent userd tag at add entry page.
// @include     http://www.nicovideo.jp/*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function altToTitle() {
        var images = document.getElementsByTagName('img');
        for (var i=0; i<images.length; i++) {
            if (images[i].alt && (! images[i].title)) {
                images[i].title = images[i].alt;
            }
        }
    }

    window.addEventListener('load', altToTitle, false);
})();
