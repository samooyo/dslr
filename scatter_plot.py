from describe import Describe
import plotly.express as px
import plotly.graph_objects as go
import sys

## TO DO : Add title to graph

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage : scatter_plot.py PathToDatasetFile\n')
        exit(1)

    describe = Describe(sys.argv[1])


    df = describe.stat

    fig = go.Figure()

    for ind in df.index:
       fig.add_trace(go.Scatter(y=df.loc[ind], x=df.columns, mode='markers', name=ind))

    # fig.update_yaxes(type="log")
    fig.update_traces(marker_size=40)
    fig.show()

########### PRINT ALL VALUES ###########

    # df = describe.df.iloc[:,5:18]

    # print(df)
    
    
    # fig = go.Figure()

    # for col in df.columns:
    #    fig.add_trace(go.Scatter(y=df[col], mode='markers', name=col))

    # fig.update_yaxes(type="log")
    # fig.show()