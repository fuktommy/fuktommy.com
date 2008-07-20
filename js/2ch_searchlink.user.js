// ==UserScript==
// @name        2ch Search Link Modifier
// @namespace   http://fuktommy.com/js/
// @description Accent recent userd tag at add entry page.
// @include     http://find.2ch.net/*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function modifyLinks() {
        var links = document.getElementsByTagName('a');
        for(var i=0; i<links.length; i++) {
            links[i].href = links[i].href.replace(/[0-9]*-[0-9]*$/,'l50');
        }
    }

    window.addEventListener('load', modifyLinks, false);
})();
