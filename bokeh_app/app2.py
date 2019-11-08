from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.themes import Theme

def modify_doc2(doc):
    import numpy as np
    import pandas as pd

    x = np.linspace(0,10*np.pi,1000)
    noise = np.random.normal(0,0.1,1000)
    y = 1-np.exp(-x) + noise
    df = pd.DataFrame({'x':x,'y':y})
    source = ColumnDataSource(data=df)
    plot = figure(x_axis_label='Time',y_axis_label='Amplitude')
    plot.line('x','y',source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            # data = df.rolling('{0}D'.format(new)).mean()
            data = df['y'].rolling(new,center=True,min_periods=1).mean()
            source.data['y'] = data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Samples")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(filename="theme.yaml")