import os,argparse
import pandas as pd
import plotly.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--speedcsv',default=os.path.expanduser('~')+'/speedtest-asc.csv',
                         help='speedtest-cli output csv file - see https://github.com/sivel/speedtest-cli')
    args = parser.parse_args()

    speedcsv = args.speedcsv
    speedplot = os.path.dirname(speedcsv) + '/speedplot.html'
    pingplot = os.path.dirname(speedcsv) + '/pingplot.html'
    speed_df = pd.read_csv(speedcsv,sep=',')

    # Speeds down and up

    Download_trace = go.Scatter(x=speed_df.Timestamp,y=speed_df.Download,name='Download',mode='lines')
    Upload_trace = go.Scatter(x=speed_df.Timestamp,y=speed_df.Upload,name='Upload',mode='lines')

    speeddata = [Download_trace,Upload_trace]
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

    if os.path.exists(os.path.expanduser('~')+'/.plotly/.credentials'):
       py.plot(figP, filename='pingplot',auto_open=False)
       py.plot(figS, filename='speedtests', auto_open=False)
       print ("posted to plot.ly")


if __name__ == '__main__':
    main()

# End
