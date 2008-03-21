// FukTorpy2 - Ajax Tropy
//
// Copyright (c) 2005 Satoshi Fukutomi <fuktommy@inter7.jp>.
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
// THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
// OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
// HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
// LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
// OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
// SUCH DAMAGE.
//

// Config
var cgiURL = "tropy.cgi";
var introURL = "intro.xml";     // InterTropy URL list
var xmlURL = "xml/";
var idsURL = "xml/ids.xml";
//var introRatio = 0.05;
var introRatio = 0.00;
var waitNavi = 1000;

//
// Send request
//
function XMLrequest() {
    var xmlhttp;
    try {
        xmlhttp = new XMLHttpRequest();
    } catch (e) {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (xmlhttp) {
        return xmlhttp;
    } else {
        return null;
    }
}

// End of XMLrequest


//
// Index of pages.
//
function Index() {
    this.counter = 0;
    this.pids = Array();
}

Index.prototype.nextPage = function () {
    if (this.pids.length <= this.counter) {
        this.update();
    }
    return this.pids[this.counter++];
}

Index.prototype.update = function () {
    this.xmlrequest = new XMLrequest();
    if (! this.xmlrequest) {
        return;
    }
    var self = this;
    this.xmlrequest.onreadystatechange = function () {
        if (! (self.xmlrequest.readyState == 4 &&
               self.xmlrequest.status == 200)) {
            return;
        }
        var xml = self.xmlrequest.responseXML;
        var ids = xml.getElementsByTagName("id");
        self.pids = Array();
        for (i=0; i<ids.length; i++) {
            try {
                self.pids[i] = ids[i].firstChild.nodeValue;
            } catch (e) {
            }
        }
        for (i=self.pids.length-1; i>=0; i--) {
            var j = Math.floor(Math.random() * (i+1))
            var tmp = self.pids[i];
            self.pids[i] = self.pids[j];
            self.pids[j] = tmp;
        }
        self.counter = 1;
        var page = new Page(self.pids[0]);
        page.update();
    }
    this.xmlrequest.open("GET", idsURL, true);
    this.xmlrequest.send(null);
}

// End of Index


//
// Page.
//
function Page(pid) {
    this.pid = pid;
    this.title = "";
    this.body = "";
}

Page.prototype.update = function () {
    this.xmlrequest = new XMLrequest();
    if (! this.xmlrequest) {
        return;
    } else if (this.pid) {
        panel.pid = this.pid;
        var self = this;
        this.xmlrequest.onreadystatechange = function () {
            if (self.xmlrequest.readyState != 4) {
                return;
            } else if (self.xmlrequest.status == 404) {
                panel.write("", "Page not found", "<h1>Page not found.</h1>");
            } else if (self.xmlrequest.status != 200) {
                panel.write("", "HTTP Error", "<h1>HTTP Error.</h1>");
            } else {
                var xml = self.xmlrequest.responseXML;
                panel.update(xml);
            }
        }
        this.xmlrequest.open("GET", xmlURL + this.pid + ".xml", true);
        this.xmlrequest.send(null);
    }
}

Page.prototype.post = function () {
    this.xmlrequest = XMLrequest();
    if (! this.xmlrequest) {
        return;
    }
    var buf = "";
    buf += "id=" + this.pid;
    buf += "&title=" + encodeURIComponent(this.title);
    buf += "&body=" + encodeURIComponent(this.body);
    var self = this;
    this.xmlrequest.onreadystatechange = function () {
        try {
            if (self.xmlrequest.readyState != 4) {
                return;
            } else if (self.xmlrequest.status != 200) {
                panel.write("HTTP Error", "<h1>HTTP Error.</h1>");
                return;
            }
        } catch (e) {
                panel.write("HTTP Error", "<h1>HTTP Error.</h1>");
                return;
        }
        var xml = self.xmlrequest.responseXML;
        if (! xml) {
            panel.write("XML Error", "<h1>XML Error.</h1>");
        } else if (xml.documentElement.nodeName == "error") {
            var err = "";
            try {
                err = xml.documentElement.firstChild.nodeValue;
            } catch (e) {
                err = "Error";
            }
            panel.write(err, "<h1>" + err + "</h1>");
        } else {
            panel.update(xml);
        }
    }
    this.xmlrequest.open("POST", cgiURL, true);
    try {
        this.xmlrequest.setRequestHeader("Content-Type",
                "application/x-www-form-urlencoded; charset=utf-8")
    } catch (e) {
    }
    this.xmlrequest.send(buf);
}

// End of Page


//
// InterTropy URL list
//
function InterTropy() {
    this.links = Array();
}

InterTropy.prototype.choice = function () {
    var i = Math.floor(Math.random() * this.links.length);
    return this.links[i];
}

InterTropy.prototype.check = function () {
    return (Math.random() < introRatio) ||
           (index.pids.length <= index.counter);
}

InterTropy.prototype.jump = function () {
    this.xmlrequest = new XMLrequest();
    if (! this.xmlrequest) {
        return;
    }
    var self = this;
    this.xmlrequest.onreadystatechange = function () {
        if (self.xmlrequest.readyState != 4) {
            return;
        } else if (self.xmlrequest.status != 200) {
            panel.write("", "HTTP Error", "<h1>HTTP Error.</h1>");
            return;
        }
        var xml = self.xmlrequest.responseXML;
        var links = xml.getElementsByTagName("link");
        self.links = Array();
        for (i=0; i<links.length; i++) {
            try {
                self.links[i] = links[i].firstChild.nodeValue;
            } catch (e) {
            }
        }
        location.href = self.choice();
    }
    this.xmlrequest.open("GET", introURL, true);
    this.xmlrequest.send(null);
}

// End of InterTropy


//
// Panel for display.
//
function Panel() {
    this.pid = "";
    this.title = "";
    this.body = "";
}

Panel.prototype.getTitle = function () {
    return document.getElementById("msgtitle").value;
}

Panel.prototype.getBody = function () {
    return document.getElementById("msgbody").value;
}

Panel.prototype.write = function (title, body) {
    var buf = "";
    buf 
    buf += "<p id='navi' class='head'>";
    buf += "<button type='button' id='save' value='Save' ";
    buf += "tabindex='1' accesskey='s' disabled='disabled' ";
    buf += "onclick='savePage();' onkeypress='savePage();'>";
    buf += "Save</button> ";
    buf += "<button type='button' tabindex='2' accesskey='c' ";
    buf += "onclick='createPage();' onckeypress='createPage();'>";
    buf += "Create</button> ";
    buf += "<button type='button' tabindex='3' accesskey='r' ";
    buf += "onclick='randomPage();' onkeypress='randomPage();'>";
    buf += "Random</button>";
    buf += "</p>";
    buf += body;
    buf += "<address>Powered by <a href='http://fuktommy.com/tropy/'>" +
           "FukTropy</a>.</address>"
    document.title = title + " - FukTropy";
    e_main = document.getElementById("main");
    e_main.innerHTML = buf;
    if (waitNavi > 0) {
        e_navi = document.getElementById('navi');
        e_navi.style.visibility = "hidden";
        setTimeout("e_navi.style.visibility='visible'", waitNavi);
    }
    this.disableSaveButton();
}

Panel.prototype.update = function (xml) {
    try {
        this.pid = xml.getElementsByTagName("id")[0].firstChild.nodeValue;
    } catch (e) {
        this.pid = "";
    }
    try {
        this.title =
            xml.getElementsByTagName("title")[0].firstChild.nodeValue;
    } catch (e) {
        this.title = "";
    }
    try {
        this.body = xml.getElementsByTagName("body")[0].firstChild.nodeValue;
    } catch (e) {
        this.body = "";
    }
    this.writepage();
}

Panel.prototype.editForm = function (title, body) {
    body = body.replace(/<br \/>/g, "\n");
    var buf = "";
    buf += "<form><p>";
    buf += "<input id='msgtitle' value='" + title + "' ";
    buf += "tabindex='4' accesskey='m' maxlength='30' ";
    buf += "onfocus='enableButton();' />";
    buf += "<textarea rows='20' id='msgbody' ";
    buf += "tabindex='5' accesskey='m' onfocus='enableButton();'>";
    buf += body + "</textarea></p></form>";
    return buf;
}

Panel.prototype.writepage = function () {
    this.write(this.title, this.editForm(this.title, this.body));
}

Panel.prototype.disableSaveButton = function () {
    var saveButton = document.getElementById("save");
    if (saveButton) {
        saveButton.disabled = true;
        saveButton.style.color = "#888";
        saveButton.style.borderColor = "#888";
    }
}

Panel.prototype.disableAllButton = function () {
    var button = document.getElementsByTagName("button");
    for (i=0; i<button.length; i++) {
        button[i].disabled = true;
        button[i].style.color = "#888";
        button[i].style.borderColor = "#888";
    }
}

Panel.prototype.enableSaveButton = function () {
    var saveButton = document.getElementById("save");
    if (saveButton) {
        saveButton.disabled = false;
        saveButton.style.color = "#000";
        saveButton.style.borderColor = "#000";
    }
}

// End of Panel


//
// Events
//

function enableButton() {
    panel.enableSaveButton();
}

function randomPage() {
    panel.disableAllButton();
    if (intro.check()) {
        intro.jump();
    } else {
        var pid = index.nextPage();
        var page = new Page(pid);
        page.update();
    }
}

function createPage() {
    panel.pid = "";
    panel.write("Create new page", panel.editForm("", ""));
}

function savePage() {
    panel.disableAllButton();
    var page = new Page(panel.pid);
    page.title = panel.getTitle();
    page.body = panel.getBody()
    if ((page.pid.length > 0) ||
        (page.title.length > 0) ||
        (page.body.length > 0)) {
        page.post();
    }
}

//
// Main
//
var panel = new Panel();
panel.write("Welcome", "<h1>Welcome</h1>");
intro = new InterTropy();
var index = new Index();
setTimeout("index.update();", 2000);
