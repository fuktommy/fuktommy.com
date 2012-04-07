function show(theID) {
    for (var i=0; i<menuIDs.length; i++) {
        id = menuIDs[i];
        var element = document.getElementById(id);
        var link = document.getElementById("link_" + id);
        if (id == theID) {
            element.style.display = "block";
            link.href = 'javascript:show("")';
        } else {
            element.style.display = "none";
            link.href = 'javascript:show("'+ id + '")';
        }
    }
}

function hideH2() {
    tags = document.getElementsByTagName("h2");
    for (var i=0; i<tags.length; i++) {
        tags[i].style.display = "none";
    }
}
