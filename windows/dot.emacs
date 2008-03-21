; -*- coding: shift_jis -*-
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 日本語表示の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(set-language-environment "Japanese")
(set-clipboard-coding-system 'japanese-shift-jis-dos)
;(set-w32-system-coding-system 'japanese-shift-jis-dos)
(setq default-file-name-coding-system 'japanese-shift-jis)
(setq file-name-coding-system 'japanese-shift-jis)
(set-default-coding-systems 'euc-jp-unix)
(set-buffer-file-coding-system 'euc-jp-unix)
(set-terminal-coding-system 'japanese-shift-jis-dos)
(set-keyboard-coding-system 'japanese-shift-jis-dos)
(setq default-process-coding-system '(euc-jp-unix . euc-jp-unix))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 漢字変換 (skk) の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(global-set-key "\C-o" 'skk-mode)
(global-set-key [?\S-\ ] 'skk-mode)
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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; ユニコード
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;(skk-mode 1)
;(require 'un-define)
;(require 'jisx0213)

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

(setq-default indent-tabs-mode nil)
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

(defun my-favorite-mode () (text-mode))
(setq default-major-mode 'my-favorite-mode)
(defun emacs-lisp-mode		() (my-favorite-mode))
(defun perl-mode		() (my-favorite-mode))
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
(setq initial-major-mode 'my-favorite-mode)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Windows
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;(set-default-font "-outline-ＭＳ ゴシック-normal-r-normal-normal-16-120-96-96-c-*-iso10646-1")

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

(set-scroll-bar-mode 'left)

(setenv "CYGWIN" "")
(setq explicit-shell-file-name "c:\\cygwin\\bin\\zsh.exe")
(setq shell-file-name "sh.exe")
(setq shell-command-switch "-c")
