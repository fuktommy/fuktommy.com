// ==UserScript==
// @name        Hanena Bookmark Tag Filter
// @namespace   http://fuktommy.com/js/
// @description Accent recent userd tag at add entry page.
// @include     http://b.hatena.ne.jp/add?mode=confirm&*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/hatebu_tagfilter.user.js
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id: hatebu_tagfilter.user.js 35 2008-03-20 14:52:31Z fuktommy $

(function() {
    function resizeTags(cloud) {
        var tags = document.getElementById('tags_list').getElementsByTagName('span');
        for (var i=tags.length-1; i>=0; i--) {
            var tag = tags[i].innerHTML;
            if (cloud[tag]) {
                tags[i].style.fontSize = '20pt';
            }
        }
    }

    function loadTagsFromCache() {
        var cloud = {};
        var now = (new Date()).getTime() / 1000;
        if (GM_getValue('cache_time', 0) + 1800*1000 < now) {
            return false;
        } else {
            var cached = GM_getValue('tags', '');
            var tags = cached.split('[]');
            for (var i=tags.length-1; i>=0; i--) {
                cloud[decodeURIComponent(tags[i])] = true;
            }
            resizeTags(cloud);
            return true;
        }
    }

    function loadTagsFromXML(xml) {
        var cloud = {};
        var cached = '';
        var subjects = xml.getElementsByTagName('dc:subject');
        if (subjects.length == 0) {
            subjects = xml.getElementsByTagName('subject');
        }
        for (var i=subjects.length-1; i>0; i--) {
           cloud[subjects[i].firstChild.nodeValue] = true;
           cached += encodeURIComponent(subjects[i].firstChild.nodeValue) + '[]';
        }
        if (subjects.length > 0) {
            cloud[subjects[0].firstChild.nodeValue] = true;
            cached += encodeURIComponent(subjects[i].firstChild.nodeValue);
        }
        var now = Math.floor((new Date()).getTime() / 1000);
        GM_setValue('cache_time', now);
        GM_setValue('tags', cached);

        var tags = document.getElementById('tags_list').getElementsByTagName('span');
        for (var i=tags.length-1; i>=0; i--) {
            var tag = tags[i].innerHTML;
            if (cloud[tag]) {
                tags[i].style.fontSize = '20pt';
            }
        }
    }

    function getUsername() {
        var anchor = document.getElementsByTagName('a');
        for (var i=anchor.length-1; i>=0; i--) {
            if (anchor[i].className == 'username') {
                return anchor[i].firstChild.nodeValue;
            }
        }
        return null;
    }

    function readFeed() {
        if (loadTagsFromCache()) {
            return;
        }

        var username = getUsername();
        if (! username) {
            return;
        }
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if ((request.readyState == 4) && (request.status == 200)) {
                loadTagsFromXML(request.responseXML);
            }
        }
        request.open('GET', 'http://b.hatena.ne.jp/' + username + '/rss', true);
        request.send(null);
    }

    window.addEventListener('load', readFeed, false);
})();
