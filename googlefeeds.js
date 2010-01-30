// Call Google Feeds API
// Copyright (c) 2007-2009 Satoshi Fukutomi <info@fuktommy.com>.
// $Id$

(function () {
    var feeds = [
        {'container': 'feed_blog', 'url': 'http://blog.fuktommy.com/rss'},
        {'container': 'feed_twitter', 'url': 'http://twitter.com/statuses/user_timeline/fuktommy.rss'}
    ];
    google.load('feeds', '1');

    function formatTwitterTitle(title) {
        return title.replace(/^fuktommy: /, '');
    }

    function insertEntries(container, entries) {
        container.innerHTML = '';
        var ul = document.createElement('ul');
        container.appendChild(ul);
        for (var j=0; j<entries.length; j++) {
            var item = entries[j];
            var li = document.createElement('li');
            ul.appendChild(li);
            var title = item.title;
            li.innerHTML = '<span class="listmark">●</span>';
            var a = document.createElement('a');
            li.appendChild(a);
            a.href = item.link;
            if (container.id == 'feed_twitter') {
                title = formatTwitterTitle(title);
            }
            a.appendChild(document.createTextNode(title));
        }
    }

    function initialize() {
        for (var i=0; i<feeds.length; i++) {
            var feed = new google.feeds.Feed(feeds[i].url);
            feed.setNumEntries(15);
            feed.load((function (_i) {
                return function (result) {
                    var container = document.getElementById(feeds[_i].container);
                    if (!result.error && container) {
                        insertEntries(container, result.feed.entries);
                    }
                }
            })(i));
        }
    }

    google.setOnLoadCallback(initialize);
})();
