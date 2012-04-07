// Copyright (c) 2009,2010 Satoshi Fukutomi <info@fuktommy.com>.
// Distributed under 2-clause BSD license.
// http://fuktommy.com/bsdl
// $Id$

(function() {
    function ImageList(list) {
        this.list = list;
        this.index = -1;
    }

    ImageList.prototype.forward = function () {
        return this.jump(this.index + 1);
    }

    ImageList.prototype.back = function () {
        return this.jump(this.index - 1);
    }

    ImageList.prototype.jump = function (index) {
        if (index < 1) {
            this.index = 0;
        } else if (this.list.length <= index) {
            this.index = this.list.length - 1;
        } else {
            this.index = index;
        }
        return new ImageWrapper(this.list[this.index]);
    }


    function ImageWrapper(img) {
        this.img = img;
    }

    ImageWrapper.prototype.scrollToIt = function () {
        var offset = this.img.offsetTop;
        var tmp = this.img;
        while (tmp.offsetParent) {
            offset += tmp.offsetParent.offsetTop;
            tmp = tmp.offsetParent;
        }
        if (offset > 10) offset -= 10;
        window.scroll(0, offset);
    }


    function main() {
        var images = document.getElementsByTagName('img');
        var imageList = new ImageList(images);

        function dispatchKeyPress(event) {
            if (event.ctrlKey || event.shiftKey || event.altKey) {
                return;
            }
            if (event.target.tagName.toLowerCase() == 'input') {
                return;
            }
            var key = String.fromCharCode(event.which);
            if (key == 'j') {
                imageList.forward().scrollToIt();
            } else if (key == 'k') {
                imageList.back().scrollToIt();
            }
        }

        for (var i = images.length - 1; i >= 0; i--) {
            var listener = (function (_imageList, _i) {
                return function () {
                    _imageList.jump(_i);
                }
            })(imageList, i);
            images[i].addEventListener('mouseover', listener, false);
        }

        window.addEventListener('keypress', dispatchKeyPress, false);
    }

    main();
})();
