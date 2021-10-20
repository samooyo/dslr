from describe import Describe
import plotly.express as px
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage : histogram.py PathToDatasetFile\n')
        exit(1)

    describe = Describe(sys.argv[1])

    std = describe.stat.loc['std']

    fig = px.histogram(std, x=std.index, y=std.values, log_y=True)
    fig.update_layout(xaxis_title_text='Courses', yaxis_title_text='Standard deviation')
    fig.show()