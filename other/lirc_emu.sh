#!/bin/bash


while true
do
    read -n1 s

    btn=
    
    case $s in
        0|1|2|3|4|5|6|7|8|9)
            btn=BTN_$s
            ;;
        a)
            btn=BTN_LEFT
            ;;
        d)
            btn=BTN_RIGHT
            ;;
        w)
            btn=BTN_UP
            ;;
        s)
            btn=BTN_DOWN
            ;;
        o)
            btn=BTN_OK
            ;;
        n)
            btn=BTN_STAR
            ;;
        m)
            btn=BTN_SHARP
            ;;
    esac


    [[ "$btn" != "" ]]  && echo "0000000000000000 00 $btn clock"

done | nc -Ul /tmp/lirc_emulator
