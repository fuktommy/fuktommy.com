// Call Google Feeds API
// Copyright (c) 2007 Satoshi Fukutomi <info@fuktommy.com>.

(function () {
    var feeds = [
        {'container': 'feed_blog',     'url': 'http://blog.fuktommy.com/rss'},
        {'container': 'feed_bookmark', 'url': 'http://b.hatena.ne.jp/fuktommy/rss'},
        {'container': 'feed_twitter',  'url': 'http://twitter.com/statuses/user_timeline/fuktommy.rss'}
    ];
    google.load('feeds', '1');

    function initialize() {
        for (var i=0; i<feeds.length; i++) {
            var feed = new google.feeds.Feed(feeds[i].url);
            feed.setNumEntries(15);
            feed.load((function (_i) {
                return function (result) {
                    var container = document.getElementById(feeds[_i].container);
                    if (result.error || (container == null)) {
                        return;
                    }
                    container.innerHTML = '';
                    var ul = document.createElement('ul');
                    container.appendChild(ul);
                    for (var j=0; j<result.feed.entries.length; j++) {
                        var item = result.feed.entries[j];
                        var li = document.createElement('li');
                        ul.appendChild(li);
                        var title = item.title;
                        if (feeds[_i].container == 'feed_twitter') {
                            title = title.replace(/^fuktommy:\s*/i, '');
                        }
                        li.innerHTML = '<span class="listmark">●</span>';
                        var a = document.createElement('a');
                        li.appendChild(a);
                        a.href = item.link;
                        a.appendChild(document.createTextNode(title));
                        if (feeds[_i].container == 'feed_bookmark') {
                            var span = document.createElement('span');
                            li.appendChild(span);
                            span.className = 'comment';
                            for (k=0; k<item.categories.length; k++) {
                                span.appendChild(document.createTextNode('['));
                                var a = document.createElement('a');
                                span.appendChild(a);
                                a.href = 'http://b.hatena.ne.jp/fuktommy/' + 
                                         encodeURIComponent(item.categories[k]) +
                                         '/';
                                a.appendChild(document.createTextNode(item.categories[k]));
                                span.appendChild(document.createTextNode(']'));
                            }
                            var commentBody = document.createElement('span');
                            var content = item.content;
                            content = content.replace(/\n/g, '');
                            content = content.replace(/<blockquote.*blockquote>/, '');
                            content = content.replace(/<.*?>/g, '');
                            content = content.replace(/(https?:\/\/[^\0-\x20\x7F-\xFF"'<>]+)/g, '<a href="$1">$1</a>');
                            if (content != '') {
                                span.appendChild(commentBody);
                                commentBody.innerHTML = content;
                            }
                        }
                    }
                }
            })(i));
        }
    }

    google.setOnLoadCallback(initialize);
})();
