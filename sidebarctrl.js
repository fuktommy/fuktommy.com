function setSideBarControl(html) {
    document.getElementById("sidebarctrl").innerHTML = html;
}

function showSideBar() {
    setSideBarControl('<a href="javascript:hideSideBar()">サイドバーを隠す</a>');
    document.getElementById("sidebar").style.display = "block";
    var main = document.getElementById("maincolumn");
    var ie = (navigator.userAgent.indexOf("MSIE") != -1);
    var top = (location.pathname == '/');
    if (top) {
        main.style.width = "70%";
    } else if (ie) {
        main.style.width = "78%";
    } else {
        main.style.width = "75%";
    }
}

function hideSideBar() {
    setSideBarControl('<a href="javascript:showSideBar()">サイドバーを表示する</a>');
    document.getElementById("sidebar").style.display = "none";
    var main = document.getElementById("maincolumn");
    if (navigator.userAgent.indexOf("MSIE") != -1) {
        main.style.width = "100%";
    } else {
        main.style.width = "95%";
    }
}
document.write('<p id="sidebarctrl"></p>');
