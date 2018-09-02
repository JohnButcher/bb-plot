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
# Run the test
#
$base/.local/bin/speedtest-cli --exclude 17689 --csv >$cur 2>$err
#
# Add in time now, not from server (which sometimes gets it wrong)
# plus convert to Mbits. Record dummy with zero up/down if it failed.
#
if [ $? -eq 0 ];then
   python $here/munge-csv.py $cur >>$asc
else
   echo "$now,2000,0,0" >>$asc
fi
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
<tr><th>Time</ht><th>Latency</th><th>Download</th><th>Upload</th></tr>
+++
tac $asc | grep -vi ping |
awk -F, '{print "<tr><td>"$1"</td><td>"$2"</td><td>"$3"</td><td>"$4"</td></tr>"}' >>$htm
echo "</table></body></html>" >>$htm
#
# Build basic CSV in same fashion
#
echo "Timestamp,Latency,Download,Upload" >$dsc
tac $asc |
awk -F, '{print $1","$2","$3","$4}' >>$dsc
if [ $(wc -l $asc|awk '{print $1}') -gt 10000 ]
then
   $base/.local/bin/speedtest-cli --csv-header >${asc}.header
   tail -10000 $asc >>${asc}.10000
   cat ${asc}.100000 > $asc
   rm ${asc}.10000
fi
#
# Build plot
#
python $here/bb-plot.py --post

# End
