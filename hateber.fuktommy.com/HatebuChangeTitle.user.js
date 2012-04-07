// ==UserScript==
// @name        Hatena Bookmark Change Title Mode
// @namespace   http://hateber.fuktommy.com/
// @description Click change title button in hatena bookmark add entry page.
// @include     http://b.hatena.ne.jp/add?mode=confirm&*&url=http%3A%2F%2Fhateber.fuktommy.com%2F*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://hateber.fuktommy.com/
// Distributed under the new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function clickChangeTitle() {
        unsafeWindow.document
                    .getElementById('title-th-head')
                    .getElementsByTagName('img')[0]
                    .clickObserver
                    .listener('click');
    }

    window.addEventListener('load', clickChangeTitle, false);
})();
