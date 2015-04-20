#!/usr/bin/env sh
#    author    :   丁雪峰
#    time      :   2015-03-05 09:54:51
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

ln -s `pwd`/Xdefaults ~/.Xdefaults
ln -s `pwd`/zshrc     ~/.zshrc
ln -s `pwd`/fonts     ~/.fonts

xrdb ~/.Xdefaults

packages = '
autojump
git
'



sudo pacman -Sy $packages


git config --global core.editor='gvim -f'
