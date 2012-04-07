// ==UserScript==
// @name        2ch Menu Link Modifier
// @namespace   http://fuktommy.com/js/
// @description Modify link .../ to .../subback.html.
// @include     http://info.2ch.net/guide/map.html*
// @include     http://menu.2ch.net/bbsmenu.html
// ==/UserScript==

// Copyright (c) 2009 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/
// Distributed under 2-clause BSD license.
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function modifyLinks() {
        var links = document.getElementsByTagName('a');
        var regexp = new RegExp('^http://[0-9a-z]+\.2ch\.net/[0-9a-z]+/$');
        for(var i=0; i<links.length; i++) {
            if (! regexp.test(links[i].href.toString())) {
                continue;
            }
            links[i].href += 'subback.html';
        }
    }

    window.addEventListener('load', modifyLinks, false);
})();
