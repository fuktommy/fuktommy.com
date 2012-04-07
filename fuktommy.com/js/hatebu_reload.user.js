// ==UserScript==
// @name        Hatena Bookmark Tag Filter
// @namespace   http://fuktommy.com/js/
// @description Add reload tag for NoScript
// @include     http://b.hatena.ne.jp/add?mode=confirm&*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function addLink() {
        var editForm = document.getElementById('edit_form');
        var tagsCompletion = document.getElementById('tags_completion');
        var link = document.createElement('a');
        editForm.insertBefore(link, tagsCompletion);
        link.href = location.href;
        link.appendChild(document.createTextNode('RELOAD'));
    }

    window.addEventListener('load', addLink, false);
})();
