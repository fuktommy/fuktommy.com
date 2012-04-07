// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/hatebu_tagfilter.js
// Distributed under new BSD license
// http://fuktommy.com/bsdl

(function() {
    function resizeTags(xml) {
        var cloud = {};
        var subjects = xml.getElementsByTagName('dc:subject');
        if (subjects.length == 0) {
            subjects = xml.getElementsByTagName('subject');
        }
        for (var i=subjects.length-1; i>=0; i--) {
            cloud[subjects[i].firstChild.nodeValue] = true;
        }

        var tags = $('tags_list').getElementsByTagName('span');
        for (var i=tags.length-1; i>=0; i--) {
            var tag = tags[i].innerHTML;
            if (cloud[tag]) {
                tags[i].style.fontSize = '20pt';
            }
        }
    }

    function readFeed() {
        var request = new Ajax.Request(
            'http://b.hatena.ne.jp/' + Hatena.id + '/rss',
            {
                'method': 'get',
                onComplete: function(req) {
                    resizeTags(req.responseXML);
                }
            }
        );
    }

    readFeed();
})();
