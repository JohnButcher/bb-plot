#!/bin/bash
#
here=$(dirname $0)
#
base=/home/pi
asc=$base/speedtest-asc.csv
dsc=$base/speedtest.csv
err=$base/speedtest.err
htm=$base/speedtest.html
now=$(date --iso-8601=seconds)
cur=$base/speedtest-cur.csv
#
# Get the router sync speed
# - requires telnet and "expect" to be installed and is router-specific
#
eval $($here/get-router-sync.sh) # hopefully returns "upsync= and downsync="
#
# Run the test
#
$base/.local/bin/speedtest-cli --exclude 17689 --csv >$cur 2>$err
#
# Add in time now, not from server (which sometimes gets it wrong)
# plus convert to Mbits. Record dummy with zero up/down if it failed.
#
if [ $? -eq 0 ];then
   python $here/munge-csv.py $cur >${cur}.0
   echo "$(cat ${cur}.0),${downsync:-0},${upsync:-0}" >>$asc
   rm ${cur}.0
else
   echo "$now,2000,0,0,0,0" >>$asc
fi
#
# Setup defaults for upsync and downsync for csvs that don't have them in history
#
cat $asc | awk -F, 'NF>4  {print}
                    NF==4 && /^Time/ {print $0",Downsync,Upsync"}
                    NF==4 && ! /^Time/ {print $0",0,0"}' >${asc}.0
cmp ${asc}.0 $asc >/dev/null 2>&1 || cat ${asc}.0 >$asc
rm ${asc}.0
#
# Build basic HTML table of history in reverse order
#
cat <<+++ >$htm
<html>
<head>
<meta http-equiv="refresh" content="900">
<title>Speedtests from the router</title>
</head>
<body>
<table>
<tr><th>Time</ht><th>Latency</th><th>Download</th><th>Upload</th><th>Downsync</th><th>Upsync</th></tr>
+++
tac $asc | grep -vi ping |
awk -F, '{print "<tr><td>"$1"</td><td>"$2"</td><td>"$3"</td><td>"$4"</td><td>"$5"</td><td>"$6"</td></tr>"}' >>$htm
echo "</table></body></html>" >>$htm
#
# Build basic CSV in same fashion
#
echo "Timestamp,Latency,Download,Upload,Downsync,Upsync" >$dsc
tac $asc | grep -v '^Timestamp' |
awk -F, 'NF>4  {print $1","$2","$3","$4","$5","$6}
         NF==4 {print $1","$2","$3","$4",0,0"}' >>$dsc
if [ $(wc -l $asc|awk '{print $1}') -gt 10000 ]
then
   $base/.local/bin/speedtest-cli --csv-header >${asc}.trimmed
   tail -10000 $asc >>${asc}.trimmed
   cat ${asc}.trimmed > $asc
   rm ${asc}.trimmed
fi
#
# Build plot
#
python $here/bb-plot.py --post

# End
