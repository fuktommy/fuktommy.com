(function(){
    var d = document,
        w = window,
        e = w.getSelection,
        k = d.getSelection,
        x = d.selection,
        s = (e?e():(k)?k():(x?x.createRange().text:0)),
        f = 'http://www.tumblr.com/share',
        l = d.location,
        e = encodeURIComponent,
        p = '?v=3&u='+e(l.href) +'&t='+e(d.title) +'&s='+e(s),
        u = f+p;
    if ((document.body.innerHTML.search('http://creativecommons.org/licenses/') < 0) &&
        (! confirm('looks like NOT CC. continue ?'))) {
        return;
    }
    try {
        if(!/^(.*\.)?tumblr[^.]*$/.test(l.host))
            throw(0);
        tstbklt();
    } catch(z) {
        a = function() {
            if (! w.open(u,'t','toolbar=0,resizable=0,status=1,width=450,height=430'))
                l.href=u;
        };
        if (/Firefox/.test(navigator.userAgent))
            setTimeout(a,0);
        else
            a();
    }
})();
void(0);
