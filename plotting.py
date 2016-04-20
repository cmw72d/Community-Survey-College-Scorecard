import sqlite3
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
from collections import defaultdict as dd

# Sign into plotly

df = pd.read_csv('aggregated.csv', delimiter='|', encoding="utf-8")

scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]


data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df['ST'],
        z = df['RATIO'].astype(float),
        locationmode = 'USA-states',
        #text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            )
        ),
        colorbar = dict(
            title = "Ratio"
        )
    ) ]

layout = dict(
        title = 'Median Debts to Average Income Ratio',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa'),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
        ),
    )
    
fig = dict(data=data, layout=layout)

url = py.plot(fig, filename='salaryincomeratio')