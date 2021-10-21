from describe import Describe
import plotly.express as px
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage : pair_plot.py PathToDatasetFile\n')
        exit(1)

    describe = Describe(sys.argv[1])

    df = describe.df
    df = df.drop(['First Name', 'Last Name', 'Birthday', 'Best Hand'], axis=1)
    fig = px.scatter_matrix(df, color='Hogwarts House')
    fig.show()