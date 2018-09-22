#!/bin/bash
#
ip="192.168.0.254"
p=$(cat $(dirname BASH_SOURCE)/.p)
expect -c " 
        set timeout 3
        spawn telnet "$ip"
        expect \"Login:\" 
        send \"admin\n\"
        expect \"Password:\"
        send \"$p\n\"
        expect \"commands.\"
        send \"adsl show info\n\"
        set timeout 9
        expect \"transmitted\"
        send \"exit\"
        " >/tmp/router.info 2>/dev/null
egrep '^upstreamCurrRate=|^downstreamCurrRate=' /tmp/router.info | sed 's/CurrRate//g;s/stream/sync/g' |
awk -F= '{printf("%s=%.2f\n",$1,$2/1024)}' # assumes reported in Kbps so convert to Mbps
rm -f /tmp/router.info
#
# End
