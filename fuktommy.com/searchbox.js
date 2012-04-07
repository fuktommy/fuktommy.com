//
// Search Box
//
// Copyright (c) 2006 Satoshi Fukutomi <info@fuktommy.com>.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS ``AS IS'' AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
// OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
// HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
// LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
// OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
// SUCH DAMAGE.
//

(function() {
    //
    // Config (Sample)
    //
/*
    var searchbox_engines = [
        ['WWW', 'Yahoo! Search', false,
         'http://search.yahoo.com/search?fr=yssw&ei=utf-8&p='],
        ['shinGETsu', 'Yahoo! Search', true,
         'http://search.yahoo.com/search?fr=yssw&ei=utf-8&' +
         'vs=shingetsu.info&p='],
        ['Feed', 'Google Search', false,
         'http://blogsearch.google.com/blogsearch?ie=UTF-8&' +
         'scoring=d&q=blogurl:shingetsu.info+']
    ];
    var searchbox_poweredby = [
        ['Yahoo!', 'http://www.yahoo.co.jp/'],
        ['Google', 'http://www.google.co.jp/']
    ];
*/

    //
    // Search Radio Button
    //
    function SearchEngine(searchForm, label, buttonLabel, prefix) {
        this.form = searchForm;
        this.label = label;
        this.buttonLabel = buttonLabel;
        this.prefix = prefix;
    }

    SearchEngine.prototype.write = function (selected) {
        try {
            this.radio = document.createElement('input');
            this.radio.type = 'radio';
        } catch (e) {
            try {
                this.radio = document.createElement('<input type="radio" />');
            } catch (e) {
            }
        }
        this.form.panel.appendChild(this.radio);
        this.radio.name = 'searchtarget';
        var radiolabel = document.createElement('span');
        radiolabel.appendChild(document.createTextNode(this.label));
        radiolabel.style.cursor = 'default';
        this.form.panel.appendChild(radiolabel);

        var onclick = (function(self){
                            return function(e){self.select();}})(this);
        this.radio.onclick = onclick;
        radiolabel.onclick = onclick;

        if (selected) {
            this.radio.checked = true;
            this.select();
        }
    }

    SearchEngine.prototype.select = function () {
        this.form.button.innerHTML = this.buttonLabel;
        this.form.prefix = this.prefix;
        this.form.uncheck();
        this.radio.checked = true;
        return true;
    }; 


    //
    // Search Form Object
    //
    function SearchForm(formObject) {
        this.form = formObject;
        this.prefix = '';
    }

    SearchForm.prototype.write = function () {
        var onsubmit = (function(self){
                            return function(e){return self.search();}})(this);

        this.panel = document.createElement('p');
        this.form.appendChild(this.panel);

        this.query = document.createElement('input');
        this.panel.appendChild(this.query);
        this.query.size = '55';

        this.button = document.createElement('button');
        this.panel.appendChild(this.button);
        this.button.innerHTML = 'submit';
        this.button.onclick = onsubmit;
        this.panel.appendChild(document.createElement('br'));

        this.radio = [];
        for (var i=0; i<searchbox_engines.length; i++) {
            this.radio[i] = new SearchEngine(this,
                                             searchbox_engines[i][0],
                                             searchbox_engines[i][1],
                                             searchbox_engines[i][3]);
            this.radio[i].write(searchbox_engines[i][2]);
        }

        this.panel.appendChild(document.createElement('br'));
        this.panel.appendChild(document.createTextNode('Powered by '));
        for (var i=0; i<searchbox_poweredby.length; i++) {
            var anchor = document.createElement('a');
            this.panel.appendChild(anchor);
            var name = document.createTextNode(searchbox_poweredby[i][0]);
            anchor.appendChild(name);
            anchor.href = searchbox_poweredby[i][1];
            if ((searchbox_poweredby.length >= 3) &&
                (i == searchbox_poweredby.length-2)) {
               this.panel.appendChild(document.createTextNode(', and '));
            } else if (i == searchbox_poweredby.length-2) {
               this.panel.appendChild(document.createTextNode(' and '));
            } else if (i < searchbox_poweredby.length-2) {
               this.panel.appendChild(document.createTextNode(', '));
            }
        }
        this.panel.appendChild(document.createTextNode('.'));

        this.form.onsubmit = onsubmit;
    };

    SearchForm.prototype.uncheck = function () {
        for (var i=0; i<this.radio.length; i++) {
            this.radio[i].radio.checked = false;
        }
    }

    SearchForm.prototype.search = function () {
        location.href = this.prefix + encodeURIComponent(this.query.value);
        return false;
    }

    //
    // main
    //
    function main() {
        document.write('<form id="search"></form>');
        form = new SearchForm(document.getElementById('search'));
        form.write();
    }

    main();
})();
