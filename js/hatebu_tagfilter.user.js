// ==UserScript==
// @name        Hatena Bookmark Tag Filter
// @namespace   http://fuktommy.com/js/
// @description Accent recent userd tag at add entry page.
// @include     http://b.hatena.ne.jp/add?mode=confirm&*
// ==/UserScript==

// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/hatebu_tagfilter.user.js
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function resizeTags(cloud) {
        var tags = document.getElementById('all-tags').getElementsByTagName('span');
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
        var cacheTime = GM_getValue('cache_time', 0);
        if (cacheTime <= 0) {
            return false;
        }
        var result = now < cacheTime + 1800;
        var cached = GM_getValue('tags', '');
        var tags = cached.split('[]');
        for (var i=tags.length-1; i>=0; i--) {
            cloud[decodeURIComponent(tags[i])] = true;
        }
        resizeTags(cloud);
        return result;
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

        var tags = document.getElementById('all-tags').getElementsByTagName('span');
        for (var i=tags.length-1; i>=0; i--) {
            var tag = tags[i].innerHTML;
            if (cloud[tag]) {
                tags[i].style.fontSize = '20pt';
            }
        }
    }

    function getUsername() {
        var img = document.getElementsByTagName('img');
        for (var i=img.length-1; i>=0; i--) {
            if (img[i].className == 'profile-image') {
                return img[i].title;
            }
        }
        return null;
    }

    function readFeed() {
        document.body.style.width = '90%';
        document.getElementById('all-tags').style.lineHeight = '1.5';

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
