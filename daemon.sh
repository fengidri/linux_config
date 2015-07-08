#!/usr/bin/env sh
#    author    :   丁雪峰
#    time      :   2015-06-19 18:02:55
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


if [ "x$1" == "xwatchdog" ]
then
    while [ 1 ]
    do
        setsid $2 &
        wait
    done

else
    for p in $DAEMON_PROCS
    do
        sh $0 watchdog $p &
    done
fi
