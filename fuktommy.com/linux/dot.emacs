; -*- coding: utf-8 -*-
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 日本語表示の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(require 'un-define)
(coding-system-put 'utf-8 'category 'utf-8)
(set-language-info
    "Japanese"
    'coding-priority (cons 'utf-8
(get-language-info "Japanese" 'coding-priority)))
;(set-language-environment "Japanese")
(set-clipboard-coding-system 'utf-8-unix)
(setq default-file-name-coding-system 'utf-8)
(setq file-name-coding-system 'utf-8)
(set-default-coding-systems 'utf-8-unix)
(set-buffer-file-coding-system 'utf-8-unix)
(set-terminal-coding-system 'utf-8-unix)
(set-keyboard-coding-system 'utf-8-unix)
(setq default-process-coding-system '(utf-8-unix . utf-8-unix))

(setq load-path (append (list
                         "/usr/local/share/emacs/site-lisp"
                         "/usr/local/share/emacs/site-lisp/apel"
                         "/usr/local/share/emacs/site-lisp/emu"
                         "/usr/local/share/emacs/site-lisp/skk"
                         )
			 load-path))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 漢字変換 (skk) の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(require 'skk-autoloads)
(global-set-key "\C-o" 'skk-mode)
(global-set-key [?\S-\ ] 'skk-mode)
(setq skk-status-indicator 'left)
(setq skk-large-jisyo "/usr/local/share/skk/SKK-JISYO.L")
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
;(global-set-key [mouse-4] 'scroll-down)
;(global-set-key [mouse-5] 'scroll-up)
(setq initial-scratch-message nil)

(defun my-favorite-mode () (text-mode))
(setq default-major-mode 'my-favorite-mode)
(defun emacs-lisp-mode		() (my-favorite-mode))
(defun perl-mode		() (my-favorite-mode))
(defun php-mode                 () (my-favorite-mode))
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
(setq initial-major-mode 'my-favorite-mode)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Windows
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;(set-default-font "-outline-\202l\202r \203\123\203V\203b\203N-normal-r-normal-normal-16-120-96-96-c-*-iso10646-1")
;(set-scroll-bar-mode 'left)
