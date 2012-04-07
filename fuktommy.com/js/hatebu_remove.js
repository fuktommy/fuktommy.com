// Copyright (c) 2008 Satoshi Fukutomi <info@fuktommy.com>.
// http://fuktommy.com/js/
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
    var form = document.getElementsByTagName('form');
    for (var i=0; i<form.length; i++) {
        if (form[i].className == 'delete') {
            if (form[i].action, form[i].rkm.value && form[i].eid.value) {
                deleteFormList.addItem([form[i].action, form[i].rkm.value, form[i].eid.value]);
            }
        }
    }
    deleteFormList.removeNextItem();
})();
