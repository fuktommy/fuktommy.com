// ==UserScript==
// @name        Hanena Bookmark Ignore Tags Filter
// @namespace   http://fuktommy.com/js/
// @description Ignore tags user set.
// @include     http://b.hatena.ne.jp/add?mode=confirm&*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/hatebu_ignore_tags.user.js
// Distributed under new BSD license
// http://fuktommy.com/bsdl

(function() {
    var ignoreTags = [
        'amazon',
        'DL違法化',
        'filtering',
        'googlevideo',
        'miau',
        'musashi',
        'ngn',
        'ohmynews',
        'slp',
        'seo',
        'stage6',
        'tinycafe',
        'しょこたん',
        'ひこにゃん',
        'らきすた',
        'ガンダム式',
        'クリムゾン',
        'サイトウサン',
        'デブサミ',
        'ニコブ',
        'モスバーガー問題',
        'ライトセイバー',
        'ロングテール',
        'リーダーシップ',
        '人間力',
        '医療',
        '人間関係',
        '公私問題',
        '転載',
        '先行者',
        '初音ミク',
        '初音ミク公序良俗問題',
        '初音ミク着うた問題',
        '瀧澤',
        '缶りょめ',
        '蒟蒻',
        '虚構新聞',
        '麻生太郎'
    ];

    var button = document.createElement('button');

    function displayTags() {
        var span = document.getElementById('tags_list').getElementsByTagName('span');
        for (var i=span.length-1; i>=0; i--) {
             span[i].style.display = 'inline';
        }
        button.innerHTML = 'タグを隠す';
        button.removeEventListener('click', displayTags, false);
        button.addEventListener('click', hideTags, false);
    }

    function hideTags() {
        var ignoreTable = {};
        for (var i=ignoreTags.length-1; i>=0; i--) {
            ignoreTable[ignoreTags[i]] = true;
        }
        var span = document.getElementById('tags_list').getElementsByTagName('span');
        for (var i=span.length-1; i>=0; i--) {
            var tag = span[i].innerHTML;
            if (ignoreTable[tag]) {
                span[i].style.display = 'none';
            }
        }
        button.innerHTML = '全タグを表示';
        button.removeEventListener('click', hideTags, false);
        button.addEventListener('click', displayTags, false);
    }

    function init() {
        button.innerHTML = '全タグを表示';
        button.type = 'button';
        document.getElementById('tags_list').appendChild(button);
        hideTags();
    }

    window.addEventListener('load', init, false);
})();
