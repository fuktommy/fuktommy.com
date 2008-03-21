// 必勝!! ナンバープレイス
//
// Copyright (c) 2001,2006 Satoshi Fukutomi <info@fuktommy.com>.
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

var SIZE = 9;
var ROWS = 3;	// 箱の縦の長さ
var COLS = 3;	// 箱の横の長さ


//
// 次のマスに飛ぶ設定
//
function addEventJump(prev, next) {
    if (prev.addEventListener) {
        prev.addEventListener(
            'keyup',
            (function (_next) {
                return function (e) {
                    if (prev.value != '') {
                        _next.focus();
                    }
                }
            })(next),
            false);
    } else if (prev.attachEvent) {
        prev.attachEvent(
            'onkeyup',
            (function (_next) {
                return function () {
                    if (prev.value != '') {
                        _next.focus();
                    }
                }
            })(next));
    }
}


//
// 確定した数字の表
//
function FixedMatrix() {
    this.matrix = [];
    this.area = document.getElementById('matrix');
    this.area.innerHTML = '';
    var form = document.createElement('form');
    this.area.appendChild(form);
    var prev = null;
    for (var i=0; i<SIZE; i++) {
        var array = [];
        for (var j=0; j<SIZE; j++) {
            var input = document.createElement('input');
            input.size = 2;
            array.push(input);
            form.appendChild(input);
            if ((j+1 != SIZE) && ((j+1) % ROWS == 0)) {
                var text = document.createElement('span');
                text.innerHTML = '&nbsp;';
                form.appendChild(text);
            }
            if (prev) {
                addEventJump(prev, input)
            }
            prev = input;
        }
        form.appendChild(document.createElement('br'));
        if ((i+1 != SIZE) && ((i+1) % COLS == 0)) {
            var text = document.createElement('br');
            form.appendChild(text);
        }
        this.matrix.push(array);
    }
}

// 参照
FixedMatrix.prototype.get = function(x, y) {
    return this.matrix[x][y].value;
}

// 代入
FixedMatrix.prototype.set = function(x, y, value) {
    this.matrix[x][y].value = value;
}


//
// 数字の候補を格納する表
//
function CandidateMatrix() {
    this.matrix = [];
    for (var i=0; i<SIZE; i++) {
        var array1 = [];
        for (var j=0; j<SIZE; j++) {
            var array2 = []
            for (var k=0; k<SIZE; k++) {
                array2.push(true);
            }
            array1.push(array2);
        }
        this.matrix.push(array1);
    }
}

// あるマスについての候補の集合
CandidateMatrix.prototype.condidate = function(x, y) {
    var buf = [];
    for (var i=0; i<SIZE; i++) {
        if (this.matrix[x][y][i]) {
            buf.push(i);
        }
    }
    return buf;
}

// 数字の確定
CandidateMatrix.prototype.fix = function(x, y, value) {
    for (var i=0; i<SIZE; i++) {
        this.matrix[x][y][i] = false;
        this.matrix[x][i][value-1] = false;
        this.matrix[i][y][value-1] = false;
    }
    var x0 = Math.floor(x/ROWS)*ROWS;
    var y0 = Math.floor(y/COLS)*COLS;
    for (var i=x0; i<x0+ROWS; i++) {
        for (var j=y0; j<y0+COLS; j++) {
            this.matrix[i][j][value-1] = false;
        }
    }
}

// 候補が1つしかないマスを検索
CandidateMatrix.prototype.search = function() {
    var buf = [];
    for (var i=0; i<SIZE; i++) {
        for (var j=0; j<SIZE; j++) {
            var condidate = this.condidate(i, j);
            if (condidate.length == 1) {
                buf.push([i, j, condidate[0]+1]);
            }
        }
    }
    return buf;
}

// 数字が入るかどうか
CandidateMatrix.prototype.check = function(x, y, value) {
    return this.matrix[x][y][value-1];
}


//
// メイン
//
var fixedMatrix;
var candidateMatrix;
function np_init() {
    var status = document.getElementById('status');
    status.innerHTML = '';
    fixedMatrix = new FixedMatrix();
}

function np_clear() {
     for (var i=0; i<SIZE; i++) {
        for (var j=0; j<SIZE; j++) {
            fixedMatrix.set(i, j, '');
        }
    }
    var status = document.getElementById('status');
    status.innerHTML = '';
}

function np_start() {
    candidateMatrix = new CandidateMatrix();
    var status = document.getElementById('status');
    status.innerHTML = '計算中';
    var count = 0;

    for (var i=0; i<SIZE; i++) {
        for (var j=0; j<SIZE; j++) {
            var value = fixedMatrix.get(i, j);
            if (value.search(/^[0-9]+$/)==0) {
                candidateMatrix.fix(i, j, value);
            } else {
                fixedMatrix.set(i, j, '');
            }
        }
    }

    var done = false;
    while (! done) {
        status.innerHTML = '計算中: ' + count++;
        done = true;
        condidate = candidateMatrix.search();
        if (condidate.length) {
            for (var i=0; i<condidate.length; i++) {
                var x = condidate[i][0];
                var y = condidate[i][1];
                var value = condidate[i][2];
                if (fixedMatrix.get(x, y) != value) {
                    fixedMatrix.set(x, y, value);
                    candidateMatrix.fix(x, y, value);
                    done = false;
                }
            }
        }
        for (var v=0; v<SIZE; v++) {
            for (var i=0; i<SIZE; i++) {
                var row = [];
                var col = [];
                for (var j=0; j<SIZE; j++) {
                    if (candidateMatrix.check(i, j, v+1)) {
                        row.push([i, j]);
                    }
                    if (candidateMatrix.check(j, i, v+1)) {
                        col.push([j, i]);
                    }
                }
                if (row.length == 1) {
                    fixedMatrix.set(row[0][0], row[0][1], v+1);
                    candidateMatrix.fix(row[0][0], row[0][1], v+1);
                    done = false;
                }
                if (col.length == 1) {
                    fixedMatrix.set(col[0][0], col[0][1], v+1);
                    candidateMatrix.fix(col[0][0], col[0][1], v+1);
                    done = false;
                }
            }
            for (var i=0; i<SIZE; i+=ROWS) {
                for (var j=0; j<SIZE; j+=COLS) {
                    var box = [];
                    for (var ii=i; ii<i+ROWS; ii++) {
                        for (var jj=j; jj<j+COLS; jj++) {
                            if (candidateMatrix.check(ii, jj, v+1)) {
                                box.push([ii, jj]);
                            }
                        }
                    }
                }
                if (box.length == 1) {
                    fixedMatrix.set(box[0][0], box[0][1], v+1);
                    candidateMatrix.fix(box[0][0], box[0][1], v+1);
                    done = false;
                }
            }
        }
    }

    status.innerHTML = '終了';
}
