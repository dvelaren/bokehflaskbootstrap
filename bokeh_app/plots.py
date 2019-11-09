
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button
from bokeh.layouts import layout, row
from bokeh.themes import Theme
from utils.modules import call_webservice, create_df, create_last_div, update_last_div, create_th_plot
from utils.secrets import channel_sala, channel_pieza, api_sala, api_pieza

def modify_doc_all(doc):
    """Subroutine to create a Bokeh document

    Parameters:
    doc (Bokeh doc): Bokeh current document
    
    """
    df_sala = create_df(channel_sala, api_sala)
    plot_sala, source_sala = create_th_plot(df_sala, title="Sala DHT22")
    df_pieza = create_df(channel_pieza, api_pieza)
    plot_pieza, source_pieza = create_th_plot(df_pieza, title="Pieza Sonoff AM2301")
    
    button = Button(label="Refrescar", button_type="success")
    
    def update():
        """Subroutine to update the Bokeh plot with new values

        """
        df_sala = create_df(channel_sala, api_sala)
        source_sala.data = ColumnDataSource(df_sala).data
        df_pieza = create_df(channel_pieza, api_pieza)
        source_pieza.data = ColumnDataSource(df_pieza).data
        update_last_div(df_sala, last_sala, "Sala")
        update_last_div(df_pieza, last_pieza, "Pieza")
    button.on_click(update)
    last_sala = create_last_div(df_sala, "Sala")
    last_pieza = create_last_div(df_pieza, "Pieza")
    l = layout([
        [plot_sala, plot_pieza],
        [last_sala],
        [last_pieza],
        [button]
    ], sizing_mode='stretch_width')
    # l = row([plot_sala, plot_pieza], sizing_mode='stretch_width')
    doc.add_root(l)
    doc.add_periodic_callback(update, 15000)
    doc.theme = Theme(filename="theme.yaml")

def modify_doc_pieza(doc):
    """Subroutine to create a Bokeh document

    Parameters:
    doc (Bokeh doc): Bokeh current document
    
    """
    df_pieza = create_df(channel_pieza, api_pieza)
    plot_pieza, source_pieza = create_th_plot(df_pieza, title="Pieza Sonoff AM2301")
    
    button = Button(label="Refrescar", button_type="success")
    
    def update():
        """Subroutine to update the Bokeh plot with new values

        """
        df_pieza = create_df(channel_pieza, api_pieza)
        source_pieza.data = ColumnDataSource(df_pieza).data
        update_last_div(df_pieza, last_pieza, "Pieza")
    button.on_click(update)
    last_pieza = create_last_div(df_pieza, "Pieza")
    l = layout([
        [plot_pieza],
        [last_pieza],
        [button]
    ], sizing_mode='stretch_width')
    doc.add_root(l)
    doc.add_periodic_callback(update, 15000)
    doc.theme = Theme(filename="theme.yaml")

def modify_doc_sala(doc):
    """Subroutine to create a Bokeh document

    Parameters:
    doc (Bokeh doc): Bokeh current document
    
    """
    df_sala = create_df(channel_sala, api_sala)
    plot_sala, source_sala = create_th_plot(df_sala, title="Sala DHT22")
    
    button = Button(label="Refrescar", button_type="success")
    
    def update():
        """Subroutine to update the Bokeh plot with new values

        """
        df_sala = create_df(channel_sala, api_sala)
        source_sala.data = ColumnDataSource(df_sala).data
        update_last_div(df_sala, last_sala, "Sala")
    button.on_click(update)
    last_sala = create_last_div(df_sala, "Sala")
    l = layout([
        [plot_sala],
        [last_sala],
        [button]
    ], sizing_mode='stretch_width')
    doc.add_root(l)
    doc.add_periodic_callback(update, 15000)
    doc.theme = Theme(filename="theme.yaml")

# def modify_doc_old(doc):
#     from bokeh.models import ColumnDataSource, Slider
#     from bokeh.plotting import figure
#     from bokeh.layouts import column
#     from bokeh.themes import Theme
#     import numpy as np
#     import pandas as pd

#     x = np.linspace(0,10*np.pi,1000)
#     noise = np.random.normal(0,0.1,1000)
#     y = 2*np.sin(x) + noise
#     df = pd.DataFrame({'x':x,'y':y})
#     source = ColumnDataSource(data=df)
#     plot = figure(x_axis_label='Time',y_axis_label='Amplitude', y_range=(-0.5, 2.5))
#     plot.line('x','y',source=source)

#     def callback(attr, old, new):
#         if new == 0:
#             data = df
#         else:
#             # data = df.rolling('{0}D'.format(new)).mean()
#             data = df['y'].rolling(new,center=True,min_periods=1).mean()
#             source.data['y'] = data

#     slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Samples")
#     slider.on_change('value', callback)

#     doc.add_root(column(slider, plot))

#     doc.theme = Theme(filename="theme.yaml")