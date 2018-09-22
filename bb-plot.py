import os,argparse, datetime
import pandas as pd
import plotly.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--speedcsv',default=os.path.expanduser('~')+'/speedtest-asc.csv',
                         help='speedtest-cli output csv file - see https://github.com/sivel/speedtest-cli')
    parser.add_argument('--days', default='7', help='day range from now')
    parser.add_argument('--post',action='store_true', default=False, help="post to plot.ly")
    args = parser.parse_args()

    speedcsv = args.speedcsv
    speedplot = os.path.dirname(speedcsv) + '/speedplot.html'
    pingplot = os.path.dirname(speedcsv) + '/pingplot.html'
    speed_df = pd.read_csv(speedcsv,sep=',')
    speed_df['Timestamp'] = pd.to_datetime(speed_df['Timestamp'])
    offset = datetime.timedelta(days=int(args.days))
    start = datetime.date.today() - offset
    pd_start = pd.Timestamp(start)
    pd_filter = speed_df['Timestamp'] >= pd_start
    speed_df= speed_df[pd_filter]

    # Speeds down and up

    Download_trace = go.Scatter(x=speed_df.Timestamp,y=speed_df.Download,name='Download',mode='lines')
    Downsync_trace = go.Scatter(x=speed_df.Timestamp,y=speed_df.Downsync,name='Downsync',mode='lines')
    Upload_trace = go.Scatter(x=speed_df.Timestamp,y=speed_df.Upload,name='Upload',mode='lines')
    Upsync_trace = go.Scatter(x=speed_df.Timestamp,y=speed_df.Upsync,name='Upsync',mode='lines')

    speeddata = [Download_trace,Upload_trace,Downsync_trace,Upsync_trace]
    layout = go.Layout(title='Speed tests',
        xaxis=dict(title='',titlefont=dict(family='Courier New, monospace',size=14,color='#7f7f7f')),
        yaxis=dict(rangemode='tozero',title='Mbps',titlefont=dict(family='Courier New, monospace',size=14,color='#7f7f7f'))
    )
    figS = go.Figure(data=speeddata, layout=layout)

    pyoff.plot(figS, filename=speedplot, auto_open=False)
    print ("plotted to %s ") % (speedplot)

    # Pings

    speed_df = speed_df[speed_df.Ping < 60000] # take out ridiculous pings
    Ping_trace = go.Scatter(x=speed_df.Timestamp,y=speed_df.Ping,name='Ping',mode='lines')
    pingdata = [Ping_trace]
    layout = go.Layout(title='Latency',
        xaxis=dict(title='',titlefont=dict(family='Courier New, monospace',size=14,color='#7f7f7f')),
        yaxis=dict(range=[0,2000],title='Ping Ms',titlefont=dict(family='Courier New, monospace',size=14,color='#7f7f7f'))
    )
    figP = go.Figure(data=pingdata, layout=layout)
    pyoff.plot(figP, filename=pingplot, auto_open=False)
    print ("plotted to %s ") % (pingplot)

    # post to plot.ly if credentials setup

    if os.path.exists(os.path.expanduser('~')+'/.plotly/.credentials') and args.post:
       py.plot(figP, filename='pingplot',auto_open=False)
       py.plot(figS, filename='speedtests', auto_open=False)
       print ("posted to plot.ly")


if __name__ == '__main__':
    main()

# End
