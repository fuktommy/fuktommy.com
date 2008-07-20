// ==UserScript==
// @name        Hatena Bookmark Ignore Tags Filter
// @namespace   http://fuktommy.com/js/
// @description Ignore tags user set.
// @include     http://b.hatena.ne.jp/add?mode=confirm&*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/hatebu_ignore_tags.user.js
// Distributed under new BSD license
// http://fuktommy.com/bsdl

(function() {
    var button = document.createElement('button');

    var saveForm = document.createElement('form');
    var saveText = document.createElement('input');
    var saveButton = document.createElement('button');

    var ignoreTable = {};
    var ignoreTagsString = '';

    function loadIgnoreTags() {
        var tags = GM_getValue('tags', '').split('[]');
        for (var i=tags.length-1; i>=0; i--) {
            var tag = decodeURIComponent(tags[i]);
            ignoreTable[tag] = true;
            if (ignoreTagsString == '') {
                ignoreTagsString = tag;
            } else {
                ignoreTagsString += ', ' + tag;
            }
        }
    }

    function saveIgnoreTags() {
        ignoreTable = {};
        var tags = saveText.value.split(/, */);
        var data = '';
        for (var i=tags.length-1; i>=0; i--) {
            if (data == '') {
                data = encodeURIComponent(tags[i]);
            } else {
                data += '[]' + encodeURIComponent(tags[i]);
            }
            ignoreTable[tags[i]] = true;
        }
        GM_setValue('tags', data);
        hideTags();
        saveForm.appendChild(document.createTextNode('保存しました。'));
    }

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
        var span = document.getElementById('tags_list').getElementsByTagName('span');
        for (var i=span.length-1; i>=0; i--) {
            var tag = span[i].innerHTML;
            if (ignoreTable[tag]) {
                span[i].style.display = 'none';
            } else {
                span[i].style.display = 'inline';
            }
        }
        button.innerHTML = '全タグを表示';
        button.removeEventListener('click', hideTags, false);
        button.addEventListener('click', displayTags, false);
    }

    function init() {
        document.getElementById('tags_list').appendChild(button);
        document.getElementById('tags_list').appendChild(saveForm);

        button.innerHTML = '全タグを表示';
        button.type = 'button';

        saveText.size = 100;
        saveButton.innerHTML = '無視タグを保存';
        saveButton.type = 'button';
        saveForm.appendChild(saveText);
        saveForm.appendChild(saveButton);

        loadIgnoreTags();
        hideTags();

        saveText.value = ignoreTagsString;
        saveButton.addEventListener('click', saveIgnoreTags, false);
    }

    window.addEventListener('load', init, false);
})();
