(function() {
    var p = document.createElement('p');
    document.body.insertBefore(p, document.body.childNodes[0]);
    p.style.textAlign = 'left';
    var a = document.createElement('a');
    p.appendChild(a);
    a.href = 'http://b.hatena.ne.jp/entry/' + escape(location.href);
    a.style.textDecoration = 'none';
    var img = document.createElement('img');
    //img.src = 'http://b.hatena.ne.jp/entry/image/large/' + escape(location.href);
    img.src = 'http://b.hatena.ne.jp/bc/dg/' + escape(location.href);
    img.style.borderWidth = '0px';
    a.appendChild(img);
    window.scroll(0,0);
})();
