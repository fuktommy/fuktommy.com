// ==UserScript==
// @name        Hatena Dialy Button Modifier
// @namespace   http://fuktommy.com/js/
// @description Hatena Dialy Button Modifier
// @include     http://d.hatena.ne.jp/*
// @include     http://*.g.hatena.ne.jp/*
// ==/UserScript==

// Copyright (c) 2009 Satoshi Fukutomi <info@fuktommy.com>.
// Distributed under 2-clause BSD license.
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function init() {
        var style = document.createElement('style');
        document.getElementsByTagName('head')[0]
                .appendChild(style);
        style.type = 'text/css';
        style.appendChild(
            document.createTextNode(
                '#pager-bottom img { width: 500px; height: 50px}'
            )
        );
    }

    window.addEventListener('load', init, false);
})();
