


EDITOR=gvim

source $HOME/.zsh/git.rc


function Jobs(){
    local n=$(jobs | \grep '^\[' | wc -l)
    #if [ "X$n" -ge "X0" ]; then
    #    return 0;
    #fi
    if [ "x$n" != "x0" ]; then
        echo "Jobs: $n "
    fi
}
#}}}

#color{{{
autoload colors zsh/terminfo
if [[ "$terminfo[colors]" -ge 8 ]]; then
    colors
fi
for color in BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
    eval __$color='%{$terminfo[bold]$fg[${(L)color}]%}'
    eval $color='%{$fg[${(L)color}]%}'
    eval _$color='%{$bg[${(L)color}]%}'
    (( count = $count + 1 ))
done
FINISH="%{$terminfo[sgr0]%}"
#}}}

#命令提示符 {{{
precmd () {
    local zero='%([BSUbfksu]|([FB]|){*})'
    local gitst="$(GIT \gs)"

    local left="$YELLOW%M$GREEN$gitst$FINISH$RED$(Jobs)$FINISH$CYAN%~ $FINISH"
    local right="$MAGENTA%D %T"
    local TTY=$(tty)
    TTY=${TTY:9}
    local newline="$CYAN%n-$TTY>>$FINISH"
    HBAR=""

    local leftsize=${#${(S%%)left//$~zero/}}
    local rightsize=${#${(S%%)right//$~zero/}}

    FILLBAR="\${(l.(($COLUMNS - ($leftsize + $rightsize)))..${HBAR}.)}"
    local mid=$WHITE${(e)FILLBAR}

    #PROMPT="$(echo "$WHITE$left$mid$right$FINISH\n$newline")"
    PROMPT="$(echo "$WHITE$left$FINISH\n$newline")"

    #在 Emacs终端 中使用 Zsh 的一些设置
    if [[ "$TERM" == "dumb" ]]; then
        setopt No_zle
        PROMPT='%n@%M %/\n>>'
        alias ls='ls -F'
    fi
    #local count_db_wth_char=${#${${(%):-%/}//[[:ascii:]]/}}
    #local leftsize=${#${(%):-%M%/}}+$count_db_wth_char+${#${(S%%)gitbranch//$~zero/}}
    #local rightsize=${#${(%):-%D %T }}
    #FILLBAR="\${(l.(($COLUMNS - ($leftsize + $rightsize +2)))..${HBAR}.)}"
    #RPROMPT=$(echo "%(?..$RED%?$FINISH)")
    #PROMPT=$(echo "$BLUE%M$GREEN%/ $gitbranch\n$CYAN%n >>>$FINISH ")
    #PROMPT=$(echo "$BLUE%M$GREEN%/ $gitbranch$WHITE${(e)FILLBAR} $MAGENTA%D %T$FINISH\n$CYAN%n >>>$FINISH ")
    #PROMPT=$(echo "$left$mid$right\n$CYAN%n >>>$FINISH ")
}
#}}}

#标题栏、任务栏样式{{{
case $TERM in (*xterm*|*rxvt*|(dt|k|E)term)
   preexec () {
       #print -Pn "\e]0;%n@%M//%/\ $1\a"
       print -Pn "\e]0;$1 - %M %/\a"
       #print -Pn "\e]0;${PWD}\a" # change the title
   }
   ;;
esac
#}}}

#关于历史纪录的配置 {{{
#历史纪录条目数量
export HISTSIZE=10000
#注销后保存的历史纪录条目数量
export SAVEHIST=10000
#历史纪录文件
#export HISTFILE=~/.zhistory
#以附加的方式写入历史纪录
setopt INC_APPEND_HISTORY
#如果连续输入的命令相同，历史纪录中只保留一个
setopt HIST_IGNORE_DUPS
#为历史纪录中的命令添加时间戳
setopt EXTENDED_HISTORY

#启用 cd 命令的历史纪录，cd -[TAB]进入历史路径
setopt AUTO_PUSHD
#相同的历史路径只保留一个
setopt PUSHD_IGNORE_DUPS



#在命令前添加空格，不将此命令添加到纪录文件中
#setopt HIST_IGNORE_SPACE
#}}}

#每个目录使用独立的历史纪录{{{
HISTDIR="$HOME/.zhistory"
    [[ ! -d "$HISTDIR" ]] && mkdir -p "$HISTDIR"
HISTFILE="$HISTDIR/${PWD//\//:}"
chpwd() {
#   fc -W                                       # write current history  file
#   "setopt INC_APPEND_HISTORY"
    HISTFILE="$HISTDIR/${PWD//\//:}"            # set new history file
    [[ ! -e "$HISTFILE" ]] && touch $HISTFILE
    local ohistsize=$HISTSIZE
        HISTSIZE=0                              # Discard previous dir's history
        HISTSIZE=$ohistsize                     # Prepare for new dir's history
    fc -R                                       # read from current histfile
}

function allhistory { cat $HISTDIR/* }                                   #*/
function convhistory {
            sort $1 | sed 's/^:\([ 0-9]*\):[0-9]*;\(.*\)/\1::::::\2/'
            #|
            #awk -F"::::::" '{ $1=strftime("%Y-%m-%d %T",$1) "|"; print }'
}
#使用 histall 命令查看全部历史纪录
function histall { convhistory =(allhistory) |
            sed '/^.\{20\} *cd/i\\' }
#使用 hist 查看当前目录历史纪录
function h {
    echo $?
    if [[ "x$?" == "x2" ]]; then
        convhistory $HISTFILE  | grep $1
        return
    fi
    convhistory $HISTFILE
}

#全部历史纪录 top55
function top55 { allhistory | awk -F':[ 0-9]*:[0-9]*;' '{ $1="" ; print }' | sed 's/ /\n/g' | sed '/^$/d' | sort | uniq -c | sort -nr | head -n 55 }


#}}}

#杂项 {{{
#允许在交互模式中使用注释  例如：
#cmd #这是注释
setopt INTERACTIVE_COMMENTS

#启用自动 cd，输入目录名回车进入目录
#稍微有点混乱，不如 cd 补全实用
setopt AUTO_CD
setopt AUTO_LIST AUTO_MENU

#扩展路径

#禁用 core dumps
limit coredumpsize 0

#vim风格 键绑定
bindkey -v
#设置 [DEL]键 为向后删除
bindkey "\e[3~" delete-char
bindkey "^R" history-incremental-search-backward

#Alt
bindkey "^[1"  digit-argument
bindkey "^[2"  digit-argument
bindkey "^[3"  digit-argument
bindkey "^[4"  digit-argument
bindkey "^[5"  digit-argument
bindkey "^[-"  neg-argument
#以下字符视为单词的一部分
WORDCHARS='*?_-[]~=&;!#$%^(){}<>'

#  设置可以依据于已经输入的命令进行histroy过滤
bindkey "^[[A" history-search-backward
bindkey "^[[B" history-search-forward
#}}}

#自动补全功能 {{{
setopt AUTO_LIST
setopt AUTO_MENU
#开启此选项，补全时会直接选中菜单项
#setopt MENU_COMPLETE


fpath=($HOME/.zsh/completion $fpath)
autoload -U compinit
compinit

#自动补全缓存
#zstyle ':completion::complete:*' use-cache on
#zstyle ':completion::complete:*' cache-path .zcache
#zstyle ':completion:*:cd:*' ignore-parents parent pwd

#自动补全选项
zstyle ':completion:*' verbose yes
zstyle ':completion:*' menu select
zstyle ':completion:*:*:default' force-list always
zstyle ':completion:*' select-prompt '%SSelect:  lines: %L  matches: %M  [%p]'

zstyle ':completion:*:match:*' original only
zstyle ':completion::prefix-1:*' completer _complete
zstyle ':completion:predict:*' completer _complete
zstyle ':completion:incremental:*' completer _complete _correct
zstyle ':completion:*' completer _complete _prefix _correct _prefix _match _approximate

#路径补全
zstyle ':completion:*' expand 'yes'
zstyle ':completion:*' squeeze-slashes 'yes'
zstyle ':completion::complete:*' '\\'


#修正大小写
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}'
#错误校正
zstyle ':completion:*' completer _complete _match _approximate
zstyle ':completion:*:match:*' original only
zstyle ':completion:*:approximate:*' max-errors 0 numeric

#kill 命令补全
compdef pkill=killall
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:*:*:*:processes' force-list always
zstyle ':completion:*:processes' command 'ps -au$USER'

#补全类型提示分组
zstyle ':completion:*:matches' group 'yes'
zstyle ':completion:*' group-name ''
zstyle ':completion:*:options' description 'yes'
zstyle ':completion:*:options' auto-description '%d'
zstyle ':completion:*:descriptions' format $'\e[01;33m -- %d --\e[0m'
zstyle ':completion:*:messages' format $'\e[01;35m -- %d --\e[0m'
zstyle ':completion:*:warnings' format $'\e[01;31m -- No Matches Found --\e[0m'
zstyle ':completion:*:corrections' format $'\e[01;32m -- %d (errors: %e) --\e[0m'

# cd ~ 补全顺序
zstyle ':completion:*:-tilde-:*' group-order 'named-directories' 'path-directories' 'users' 'expand'

#补全 ping
#zstyle ':completion:*:ping:*' hosts 192.168.128.1{38,} http://www.g.cn \
#       192.168.{1,0}.1{{7..9},}
zstyle ':completion:*:ping:*' hosts http://www.g.cn  192.168.{1,0}.1 www.sina.com

#补全 ssh scp sftp 等
#my_accounts=()
#zstyle ':completion:*:my-accounts' users-hosts $my_accounts

#[ -f ~/.ssh/config ] && : ${(A)ssh_config_hosts:=${${${${(@M)${(f)"$(<~/.ssh/config)"}:#Host *}#Host }:#*\**}:#*\?*}}
[ -f ~/.ssh/config ] && ssh_config_hosts=($(grep "^Host" ~/.ssh/config| awk '{print $2}'))
zstyle ':completion:*:*:*' hosts $ssh_config_hosts
#}}}

##行编辑高亮模式 {{{
# Ctrl+@ 设置标记，标记和光标点之间为 region
zle_highlight=(region:bg=magenta #选中区域
               special:bold      #特殊字符
               isearch:underline)#搜索时使用的关键字
#}}}

##空行(光标在行首)补全 "cd " {{{
user-complete(){
    case $BUFFER in
        "/" )                       # 空行填入 "cd "
            BUFFER="cd /"
            zle end-of-line
            zle expand-or-complete
            ;;
        ".." )                       # 空行填入 "cd "
            BUFFER="cd ../"
            zle end-of-line
            zle expand-or-complete
            ;;
        "" )                       # 空行填入 "cd "
            BUFFER="cd "
            zle end-of-line
            zle expand-or-complete
            ;;
        "cd  " )                   # TAB + 空格 替换为 "cd ~"
            BUFFER="cd ~"
            zle end-of-line
            zle expand-or-complete
            ;;
        " " )
            BUFFER="!?"
            zle end-of-line
            ;;
        "cd --" )                  # "cd --" 替换为 "cd +"
            BUFFER="cd +"
            zle end-of-line
            zle expand-or-complete
            ;;
        "cd +-" )                  # "cd +-" 替换为 "cd -"
            BUFFER="cd -"
            zle end-of-line
            zle expand-or-complete
            ;;
        * )
            zle expand-or-complete
            ;;
    esac
}
zle -N user-complete
bindkey "\t" user-complete

#显示 path-directories ，避免候选项唯一时直接选中
cdpath="/home"
#}}}

##在命令前插入 sudo {{{
#定义功能
sudo-command-line() {
    [[ -z $BUFFER ]] && zle up-history
    [[ $BUFFER != sudo\ * ]] && BUFFER="sudo $BUFFER"
    zle end-of-line                 #光标移动到行末
}
zle -N sudo-command-line
#定义快捷键为： [Esc] [Esc]
bindkey "\e\e" sudo-command-line
#}}}

function blog(){
    vim -c "TexList"
}

function frain(){
    if [[ "X$1" == "X" ]];then
        return
    fi
    cd $1
    vim -c "Frain $(pwd)"
}

function ssh(){
    Profile=SSH
    echo -e "\033]50;SetProfile=$Profile\x7"
    export ITERM_PROFILE=$Profile

    /usr/bin/ssh $*

    Profile=Default
    echo -e "\033]50;SetProfile=$Profile\x7"
    export ITERM_PROFILE=$Profile
}

function arch(){
    P='/Users/fengidri/vagrant/archlinux/'

    Profile=ArchLinux
    echo -e "\033]50;SetProfile=$Profile\x7"
    export ITERM_PROFILE=$Profile

    /usr/bin/ssh vagrant@127.0.0.1 -p 2222 \
        -o DSAAuthentication=yes \
        -o LogLevel=FATAL -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -o IdentitiesOnly=yes \
        -i $P.vagrant/machines/default/virtualbox/private_key
        #-o Compression=yes

    if [[ "X$?" == "X255" ]]
then
	cd $p
	vagrant up
fi

    Profile=Default
    echo -e "\033]50;SetProfile=$Profile\x7"
    export ITERM_PROFILE=$Profile
}

function archvim(){
    P='/Users/fengidri/vagrant/archlinux/'

    /usr/bin/ssh vagrant@127.0.0.1 -p 2222 \
        -o Compression=yes -o DSAAuthentication=yes \
        -o LogLevel=FATAL -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -o IdentitiesOnly=yes \
        -i $P.vagrant/machines/default/virtualbox/private_key -t bash -l -c 'vim'
}

################################################################################

function grep(){
    /usr/bin/grep -E --color=auto --binary-file=without-match $@
}

#alias -g curl='curl -o /dev/null -sqv '
alias  pp='\ps h -eo pid,euser,command|\grep -E --color=auto --binary-file=without-match '

function curl(){
    /usr/bin/curl -o /dev/null $@
}

function p(){
    \ps h -eo pid,euser,command |\
        \grep -v \grep | \
        \grep -E --color=auto --binary-file=without-match $1
}

source $HOME/.zsh/alias.rc

#alias -g chromium='chromium --password-store=basic'
#alias -g luatex='~/.luatex/bin/linux/luatex'

#[Esc][h] man 当前命令时，显示简短说明
autoload run-help


#路径别名 {{{
#进入相应的路径时只要 cd ~xxx
hash -d www="/home/.vtph"
hash -d E="/etc/env.d"
hash -d C="/etc/rc.conf"
hash -d I="/etc/rc.d"
hash -d X="/etc/X11"
hash -d HIST="$HISTDIR"

#}}}

#{{{自定义补全

#}}}

#{{{ F1 计算器
arith-eval-echo() {
  LBUFFER="${LBUFFER}echo \$(( "
  RBUFFER=" ))$RBUFFER"
}
zle -N arith-eval-echo
bindkey "^[[11~" arith-eval-echo
#}}}

####{{{
function timeconv { date -d @$1 +"%Y-%m-%d %T" }
# }}}

## END OF FILE #################################################################
# vim:filetype=zsh foldmethod=marker autoindent expandtab shiftwidth=4
#

LS_COLORS='rs=0:di=01;35:ln=01;95:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01'
LS_COLORS=$LS_COLORS':cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:ca=30;41'
LS_COLORS=$LS_COLORS':tw=30;42:ow=34;42:st=37;44:ex=01;91:*.tar=01;31:'
LS_COLORS=$LS_COLORS'*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31'
LS_COLORS=$LS_COLORS':*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.zip=01;31'
LS_COLORS=$LS_COLORS':*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lz=01;31'
LS_COLORS=$LS_COLORS':*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:'
#LS_COLORS='rs=0:di=00;35:ln=00;36:mh=00:pi=40;33:so=00;35:do=00;35:bd=40;33;00:cd=40;33;00:or=40;31;00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=00;91:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.lzma=00;31:*.tlz=00;31:*.txz=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.dz=00;31:*.gz=00;31:*.lz=00;31:*.xz=00;31:*.bz2=00;31:*.bz=00;31:*.tbz=00;31:*.tbz2=00;31:*.tz=00;31:*.deb=00;31:*.rpm=00;31:*.jar=00;31:*.war=00;31:*.ear=00;31:*.sar=00;31:*.rar=00;31:*.ace=00;31:*.zoo=00;31:*.cpio=00;31:*.7z=00;31:*.rz=00;31:*.jpg=00;35:*.jpeg=00;35:*.gif=00;35:*.bmp=00;35:*.pbm=00;35:*.pgm=00;35:*.ppm=00;35:*.tga=00;35:*.xbm=00;35:*.xpm=00;35:*.tif=00;35:*.tiff=00;35:*.png=00;35:*.svg=00;35:*.svgz=00;35:*.mng=00;35:*.pcx=00;35:*.mov=00;35:*.mpg=00;35:*.mpeg=00;35:*.m2v=00;35:*.mkv=00;35:*.webm=00;35:*.ogm=00;35:*.mp4=00;35:*.m4v=00;35:*.mp4v=00;35:*.vob=00;35:*.qt=00;35:*.nuv=00;35:*.wmv=00;35:*.asf=00;35:*.rm=00;35:*.rmvb=00;35:*.flc=00;35:*.avi=00;35:*.fli=00;35:*.flv=00;35:*.gl=00;35:*.dl=00;35:*.xcf=00;35:*.xwd=00;35:*.yuv=00;35:*.cgm=00;35:*.emf=00;35:*.axv=00;35:*.anx=00;35:*.ogv=00;35:*.ogx=00;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:'


export PYTHONPATH="/home/feng/works/python-script/python/"
export SVN_EDITOR="gvim --nofork"
# 在安装了新的程序之后, zsh 并不会立即进行refresh. 下面的命令可以auto. 但
#是我怀疑这样做是不是合适, 且先用一段时间
#setopt nohashdirs










setopt extended_glob
TOKENS_FOLLOWED_BY_COMMANDS=('|' '||' ';' '&' '&&' 'sudo' 'do' 'time' 'strace' 'man')

#语法高亮
recolor-cmd() {
    region_highlight=()
    colorize=true
    start_pos=0
    for arg in ${(z)BUFFER}; do
        ((start_pos+=${#BUFFER[$start_pos+1,-1]}\
            -${#${BUFFER[$start_pos+1,-1]## #}}))
        ((end_pos=$start_pos+${#arg}))
        if $colorize; then
            colorize=false
            res=$(LC_ALL=C builtin type $arg 2>/dev/null)
            #case $res in
            #    *'reserved word'*)   style="fg=magenta,bold";;
            #    *'alias for'*)       style="fg=cyan,bold";;
            #    *'shell builtin'*)   style="fg=blue,bold";;
            #    *'shell function'*)  style='fg=green,bold';;
            #    *"$arg is"*)
            #        [[ $arg = 'sudo' ]] && style="fg=red,bold"\
            #                      || style="fg=blue,bold";;
            #    *)                   style='none,bold';;
            #esac
            style="fg=blue,bold";
            region_highlight+=("$start_pos $end_pos $style")
        fi
        [[ ${${TOKENS_FOLLOWED_BY_COMMANDS[(r)${arg//|/\|}]}:+yes} = 'yes' ]]\
            && colorize=true
        start_pos=$end_pos
    done
}

check-cmd-self-insert() { zle .self-insert && recolor-cmd }
check-cmd-backward-delete-char() { zle .backward-delete-char && recolor-cmd }

zle -N self-insert check-cmd-self-insert
zle -N backward-delete-char check-cmd-backward-delete-char


source $HOME/.upyun/upyun

