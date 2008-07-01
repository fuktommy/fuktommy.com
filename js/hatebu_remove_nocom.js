// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/hatebu_tagfilter.js
// Distributed under new BSD license
// http://fuktommy.com/bsdl
// $Id$

(function() {
    var DeleteFormList = Class.create();
    DeleteFormList.prototype.initialize = function () {
        this.item = [];
        this.i = 0;
        this.j = 0;
    };
    DeleteFormList.prototype.addItem = function (item) {
        this.item[this.i++] = item;
    };
    DeleteFormList.prototype.removeNextItem  = function () {
        if (this.item.length <= this.j) {
            alert('finish');
            return;
        } else {
            var pars = $H({rkm: this.item[this.j][1],
                           eid: this.item[this.j][2]}).toQueryString();
            new Ajax.Request(
                this.item[this.j][0],
                {parameters: pars}
            );
            this.j++;
            setTimeout(this.removeNextItem.bindAsEventListener(this), 1000);
        }
    };

    var deleteFormList = new DeleteFormList();
    var bookmarklist = null;
    var entry = document.getElementsByTagName('dl');
    for (var i=0; i<entry.length; i++) {
        if (entry[i].className != 'bookmarklist') {
            continue;
        }
        var span = entry[i].getElementsByTagName('span');
        var hasComment = false;
        for (var j=0; j<span.length; j++) {
            if (span[j].className == 'comment') {
                hasComment = true;
                break;
            }
        }
        if (hasComment) {
            continue;
        }
        var form = entry[i].getElementsByTagName('form');
        for (var j=0; j<form.length; j++) {
            if (form[j].className == 'delete') {
                if (form[j].action, form[j].rkm.value && form[j].eid.value) {
                    deleteFormList.addItem([form[j].action, form[j].rkm.value, form[j].eid.value]);
                }
            }
        }
    }
    deleteFormList.removeNextItem();
})();
