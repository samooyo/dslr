# import plotly.offline
from describe import Describe
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import sys

houses = ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']

def get_color(house: str) -> str:
    if house == 'Ravenclaw'     : return ( 'red' )
    if house == 'Slytherin'     : return ( 'blue' )
    if house == 'Gryffindor'    : return ( 'yellow' )
    if house == 'Hufflepuff'    : return ( 'green' )

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage : histogram.py PathToDatasetFile\n')
        exit(1)

    describe = Describe(sys.argv[1])

    df = describe.df

    fig = make_subplots(rows=2, cols=7, vertical_spacing=0.05, subplot_titles=('Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying'))
 
    i = j = 1

    for col in df.columns:
        if df[col].dtype == float:
            if j == 8:
                j = 1
                i = 2
            for house in houses:
                tmp_df = df.loc[df['Hogwarts House'] == house]
                fig.add_trace(go.Histogram(x=tmp_df[col], marker_color=get_color(house), name=house), row=i, col=j)
            j += 1
    
    fig.update_layout(barmode='overlay', showlegend=False)
    fig.update_traces(opacity=0.50)

    fig.show()

    # To save html :
    # plotly.offline.plot(fig, filename='graphs/histogram.html', auto_open=False)
