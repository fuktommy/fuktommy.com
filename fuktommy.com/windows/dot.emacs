; -*- coding: utf-8 -*-
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 日本語表示の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(set-language-environment "Japanese")
(set-clipboard-coding-system 'japanese-shift-jis-dos)
;(set-w32-system-coding-system 'japanese-shift-jis-dos)
(setq default-file-name-coding-system 'japanese-shift-jis)
(setq file-name-coding-system 'japanese-shift-jis)
(set-default-coding-systems 'utf-8-unix)
(set-buffer-file-coding-system 'utf-8-unix)
(set-terminal-coding-system 'japanese-shift-jis-dos)
(set-keyboard-coding-system 'japanese-shift-jis-dos)
(setq default-process-coding-system '(euc-jp-unix . euc-jp-unix))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 漢字変換 (skk) の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(skk-mode 1)
(global-set-key "\C-o" 'toggle-input-method)
(global-set-key [?\S-\ ] 'toggle-input-method)
(setq skk-status-indicator 'left)
(setq skk-large-jisyo "C:/Program Files/Common Files/SKK/SKK-JISYO.L")
(add-hook 'isearch-mode-hook
	  (function (lambda ()
		      (and (boundp 'skk-mode) skk-mode
			   (skk-isearch-mode-setup)))))
(add-hook 'isearch-mode-end-hook
	  (function                                             
	    (lambda ()
	      (and (boundp 'skk-mode) skk-mode (skk-isearch-mode-cleanup))
	      (and (boundp 'skk-mode-invoked) skk-mode-invoked
		   (skk-set-cursor-properly)))))
(setq default-input-method "japanese-skk")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; いろいろ
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(global-set-key [delete] 'delete-char)
(line-number-mode t)
(setq text-mode-hook nil)
(global-unset-key "\C-h")
(global-set-key "\C-h" 'delete-backward-char)
(global-set-key "\M-g" 'goto-line)
(setq make-backup-files nil)
(setq minibuffer-max-depth nil)
(setq next-line-add-newlines nil)
(setq visible-bell t)
(global-set-key "\C-\\" 'undo)
(server-start)

;(setq-default indent-tabs-mode t)
(setq-default indent-tabs-mode nil)
(setq-default tab-width 4)
(setq tab-stop-list
    '(4 8 12 16 20 24 28 32 36 40 44 48 52 56 60 64 68 72 76 80 84 88 92 96 100 104 108 112 116 120))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; emacs21
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(menu-bar-mode -1)
(tool-bar-mode -1)
(blink-cursor-mode -1)
(global-set-key [mouse-4] 'scroll-down)
(global-set-key [mouse-5] 'scroll-up)
(setq initial-scratch-message nil)
(setq inhibit-startup-message t)
(set-background-color "gray93")

(defun my-favorite-mode () (text-mode))
(setq default-major-mode 'my-favorite-mode)
(defun emacs-lisp-mode		() (my-favorite-mode))
(defun perl-mode		() (my-favorite-mode))
(defun python-mode		() (my-favorite-mode))
(defun sgml-mode		() (my-favorite-mode))
(defun html-mode		() (my-favorite-mode))
(defun html-mode		() (my-favorite-mode))
(defun bibtex-mode		() (my-favorite-mode))
(defun tex-mode			() (my-favorite-mode))
(defun shell-script-mode	() (my-favorite-mode))
(defun sh-mode			() (my-favorite-mode))
(defun tcsh-mode		() (my-favorite-mode))
(defun c-mode			() (my-favorite-mode))
(defun c++-mode			() (my-favorite-mode))
(defun lisp-mode		() (my-favorite-mode))
(defun pascal-mode		() (my-favorite-mode))
(defun java-mode		() (my-favorite-mode))
(defun nroff-mode		() (my-favorite-mode))
(defun makefile-mode		() (my-favorite-mode))
(defun conf-mode		() (my-favorite-mode))
(defun change-log-mode		() (my-favorite-mode))
(defun javascript-mode		() (my-favorite-mode))
(defun js-mode		() (my-favorite-mode))
(defun css-mode		() (my-favorite-mode))
(setq initial-major-mode 'my-favorite-mode)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Windows
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(create-fontset-from-ascii-font
 "-outline-ＭＳ ゴシック-normal-r-normal-normal-16-*-*-*-*-*-iso8859-1"
 nil "myfont")
(set-fontset-font "fontset-myfont"
                  'japanese-jisx0208
                  '("ＭＳ ゴシック*" . "jisx0208-sjis"))
(set-fontset-font "fontset-myfont"
                  'katakana-jisx0201
                  '("ＭＳ ゴシック*" . "jisx0201-katakana"))
(add-to-list 'default-frame-alist '(font . "fontset-myfont"))

;(set-default-font "-outline-\202l\202r \203\123\203V\203b\203N-normal-r-normal-normal-16-120-96-96-c-*-iso10646-1")

(set-scroll-bar-mode 'left)

(setenv "CYGWIN" "")
(setq explicit-shell-file-name "c:\\cygwin\\bin\\zsh.exe")
(setq shell-file-name "sh.exe")
(setq shell-command-switch "-c")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; テンプレート編集
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(add-to-list 'auto-coding-alist '("\\.tpl$" . utf-8))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; チルダ問題
;; http://www.bookshelf.jp/2ch/unix/1141309172.html#975
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(let ((my-translation-table
    (make-translation-table-from-alist
        '((#x301c . #xff5e)
    ))))
    (mapc
        (lambda (coding-system)
            (coding-system-put coding-system :decode-translation-table my-translation-table)
            (coding-system-put coding-system :encode-translation-table my-translation-table)
        )
    '(utf-8 cp932 utf-16le)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; クリップボード
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(setq x-select-enable-clipboard t)
(setq select-active-regions t)
(setq mouse-drag-copy-region t)
(setq x-select-enable-primary t)
(global-set-key [mouse-2] 'mouse-yank-at-click)
