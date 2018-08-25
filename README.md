# bb-plot

Plots broadband speedtests from a CSV file that is appended to by successive calls to speedtest-cli.
Setup
- Install speedtest-cli on a raspberry pi
- Install python plotly (will also need pandas etc)
- Setup plotly credentials
- cable pi to router
- setup speedtest.sh script to run every hour or more frequently if needed

Also useful to install a webserver such as nginx to see the local plots on your LAN
