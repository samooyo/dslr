from describe import Describe
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage : scatter_plot.py PathToDatasetFile\n')
        exit(1)

    describe    = Describe(sys.argv[1])
    df          = describe.df
    fig         = make_subplots(rows=2, cols=6, vertical_spacing=0.05, subplot_titles=('Arithmancy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying'))
 
    i = j = 1

    for col in df.columns:
        if df[col].dtype == float and col != 'Astronomy':
            if j == 7:
                j = 1
                i = 2
            fig.add_trace(go.Scatter(y=df['Astronomy'], x=df[col], mode='markers'), row=i, col=j)
            j += 1

    fig.update_layout(showlegend=False, title='Plot of Astronomy in function of each courses', title_x=0.5)
    fig.show()