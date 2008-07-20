// ==UserScript==
// @name        Hatena Bookmark Check Go Bookmark
// @namespace   http://fuktommy.com/js/
// @description Check go bookmark checkbox in hatena bookmark add entry page.
// @include     http://b.hatena.ne.jp/add?mode=confirm&*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/hatebu_check_gobm.user.js
// Distributed under the new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function checkGoBookmark() {
        document.getElementById('go_bm').checked = true;
    }

    window.addEventListener('load', checkGoBookmark, false);
})();
