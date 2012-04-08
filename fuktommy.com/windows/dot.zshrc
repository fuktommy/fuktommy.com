#
# ~/.zshrc
#

setopt NOCLOBBER
setopt INTERACTIVE_COMMENTS
setopt APPEND_HISTORY
setopt NOHUP
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE
setopt NO_BG_NICE
unsetopt NOMATCH

export PAGER="lv -Os -c"
export VISUAL=vi
export PERL5LIB=${HOME}/lib/perl
export PYTHONPATH=${HOME}/lib/python
export PYTHONSTARTUP=${HOME}/.pythonrc
export HTTP_HOME=${HOME}/.w3m/bookmark.html
export TMP=/tmp
export TMPDIR=/tmp

if [ -n "$CYGTERM" -o "$TERM" = emacs ]; then
    PATH="/usr/local/sbin:/usr/sbin:/sbin:$PATH"
    PATH="/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin:$PATH"
    PATH="/usr/local/node/bin:$PATH"
fi
PATH=$HOME/bin:$PATH

bindkey -e
WORDCHARS="*?_-.[]~=&!#$%^(){}<>"

#autoload -U compinit && compinit
#zstyle ':completion:*' verbose yes
#zstyle ':completion:*:descriptions' format '%B%d%b'
#zstyle ':completion:*:messages' format '%d'
#zstyle ':completion:*:warnings' format 'No matches for: %d'
#zstyle ':completion:*' group-name ''

alias ls="ls -F"
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"
xpwd () { echo -ne "\033]0;${HOST}: `pwd | sed "s|$HOME|~|"`\007" }

umask 022

HISTSIZE=2000
SAVEHIST=1000
HISTFILE=${HOME}/.zhistory

if [ -n $PS1 ]; then
	PS1='%m:%~%# '
	xpwd
	cd () { builtin cd $* ; xpwd }
fi

alias   ls='/bin/ls -F'
alias   ll='/bin/ls -lFh'
alias   rm='/bin/rm -i'
alias   cp='/bin/cp -i'
alias   mv='/bin/mv -i'
alias	md='/bin/mkdir'
alias	rd='/bin/rmdir'
alias	px='/bin/ps x'
alias	tgz='tar zcvf'
alias	untgz='tar zxvf'
alias	w='w3m'
alias	df='df -h'
alias	du='du -h'
alias	j='jobs'
alias	today='date +%Y-%m-%d'

title	() { echo -ne "\033]0;$*\007" }
mcd	() { mkdir -p $1 ; cd $1 }
rcd	() { local d=`pwd`; cd ..; rmdir "$d" }

#compdef -d mcd
