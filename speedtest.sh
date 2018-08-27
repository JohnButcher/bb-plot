#!/bin/bash
#
here=$(dirname $0)
#
base=/home/pi
asc=$base/speedtest-asc.csv
dsc=$base/speedtest.csv
err=$base/speedtest.err
htm=$base/speedtest.html
$base/.local/bin/speedtest-cli \
--csv 2>$err | 
 awk -F, '{printf("%s,%s,%s,%s,%.1f,%.1f,%.2f,%.2f,%s,%s\n",\
           $1,$2,$3,$4,$5,$6,$7/1048576,$8/1048576,$9,$10)}' \
 >>$asc
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
awk -F, '{print "<tr><td>"$4"</td><td>"$6"</td><td>"$7"</td><td>"$8"</td></tr>"}' >>$htm
echo "</table></body></html>" >>$htm
#
echo "Latency,Download,Upload" >$dsc
tac $asc |
awk -F, '{print $6","$7","$8}' >>$dsc
if [ $(wc -l $asc|awk '{print $1}') -gt 10000 ]
then
   $base/.local/bin/speedtest-cli --csv-header >${asc}.header
   tail -10000 $asc >>${asc}.10000
   cat ${asc}.100000 > $asc
   rm ${asc}.10000
fi
python $here/bb-plot.py --post

# End
