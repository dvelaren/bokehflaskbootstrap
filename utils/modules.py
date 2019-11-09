import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

import requests
import json

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool, Range1d, LinearAxis
from bokeh.layouts import row
from bokeh.models.widgets import Div


def call_webservice(channel, api_key):
    """Function to call ThingSpeak webservice

    Parameters:
    channel (str): Corresponding channel to call in ThingSpeak
    api_key (str): API Key to read from corresponding ThingSpeak channel

    Returns:
    json_doc: Returns a JSON document with all the variables from the channel

   """
    
    url = f'https://api.thingspeak.com/channels/{channel}/feeds.json?'
    params = {'api_key': api_key, 'results': 8000}
    r = requests.get(url, params=params)
    json_doc = json.loads(r.text)
    
    return json_doc

def create_df(channel, api):
    """Function to create a DataFrame from a ThingSpeak Channel

    Parameters:
    channel (str): Corresponding channel to call in ThingSpeak
    api (str): API Key to read from corresponding ThingSpeak channel

    Returns:
    df: Returns a DataFrame with the Temperature and Humidity (including smooth values)

   """
    
    json_doc = call_webservice(channel, api)
    df = json_normalize(json_doc['feeds'])
    df.drop(['entry_id'], axis=1, inplace=True)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')
    df['created_at'] = df['created_at'].dt.tz_convert('Europe/Madrid')
    df.rename(columns={"created_at": "Fecha", "field1": "Temperatura", "field2": "Humedad", "field3": "Heat index"}, inplace=True)
    df.set_index('Fecha', inplace=True)
    df = df.apply(pd.to_numeric)
    df['T_smooth'] = df['Temperatura'].rolling(10, min_periods=1).mean()
    df['H_smooth'] = df['Humedad'].rolling(10, min_periods=1).mean()
    
    return df

def create_last_div(df, title):
    """Function to create a Div with new DataFrame (df) values

    Parameters:
    df (DataFrame): Pandas DataFrame with new values to create the Div
    title (str): String with the title of the Div to be created

    Returns:
    row: Returns a Bokeh row with the created Div including last_date, last_temp and last_hum

   """
    
    last_date_div = Div(text=f"Último valor ({title}): {pd.to_datetime(df.index.max()).strftime('%Y-%m-%d %H:%M:%S')}")
    last_temp_div = Div(text=f"Temperatura: {df['Temperatura'][-1]} ºC")
    last_hum_div = Div(text=f"Humedad: {df['Humedad'][-1]} %")
    return row(last_date_div, last_temp_div, last_hum_div, name="title")

def update_last_div(df, div, title):
    """Subroutine to update a Div with new DataFrame (df) values

    Parameters:
    df (DataFrame): Pandas DataFrame with new values to update Div
    div (Bokeh row): Bokeh row to be udpdated
    title (str): String with the title of the Div to be updated

   """
    
    div.children[0].text = f"Último valor ({title}): {pd.to_datetime(df.index.max()).strftime('%Y-%m-%d %H:%M:%S')}"
    div.children[1].text = f"Temperatura: {df['Temperatura'][-1]} ºC"
    div.children[2].text = f"Humedad: {df['Humedad'][-1]} %"

def create_th_plot(df, title):
    """Function to create a Bokeh plot using the DataFrame (df) values

    Parameters:
    df (DataFrame): Pandas DataFrame with new values to create the plot
    title (str): String with the title of the plots
    
    Returns:
    plot: Bokeh plot with Temperature and Humidity plots
    source: Bokeh ColumnDataSource if it's required to be updated later

   """
    
    source = ColumnDataSource(df)
    plot = figure(title=title, x_axis_type='datetime', y_axis_label='Temperatura (ºC)', y_range=[15, 22])

    plot.extra_y_ranges = {'y_hum': Range1d(start=50, end=80)}
    plot.add_layout(LinearAxis(y_range_name='y_hum', axis_label='Humedad (%)'), 'right')

    temp_line = plot.line(x='Fecha', y='Temperatura', source=source, line_color='red', line_alpha=0.1, legend_label='Temp')
    temp_smooth_line = plot.line(x='Fecha', y='T_smooth', source=source, line_color='red', line_width=1, legend_label='Temp(media)')
    hum_line = plot.line(x='Fecha', y='Humedad', source=source, line_color='blue', line_alpha=0.1, legend_label='Hum',y_range_name='y_hum')
    hum_smooth_line = plot.line(x='Fecha', y='H_smooth', source=source, line_color='blue', line_width=1, legend_label='Hum(media)',y_range_name='y_hum')

    hover1 = HoverTool(
        tooltips=[
            ('Fecha', '@Fecha{%T %F}'),
            ('Temperatura', '@Temperatura'),
            ('Temp(media)', '@T_smooth')
        ],

        formatters={
            'Fecha': 'datetime', # use 'datetime' formatter for 'date' field
        },
        renderers = [temp_line, temp_smooth_line]
    )
    hover2 = HoverTool(
        tooltips=[
            ('Fecha', '@Fecha{%T %F}'),
            ('Humedad', '@Humedad'),
            ('Hum(media)', '@H_smooth')
        ],

        formatters={
            'Fecha': 'datetime', # use 'datetime' formatter for 'date' field
        },
        renderers = [hum_line, hum_smooth_line]
    )

    plot.add_tools(hover1)
    plot.add_tools(hover2)
    plot.xaxis.major_label_orientation = np.pi/4
    plot.xaxis.formatter = DatetimeTickFormatter(days=["%m/%d"],
                                                months=["%m/%d %H:%M"],
                                                hours=["%H:%M"],
                                                minutes=["%H:%M"],
                                                seconds=["%H:%M"])
    plot.xaxis[0].ticker.desired_num_ticks = 15
    plot.legend.location = "top_left"
    plot.legend.orientation = "horizontal"
    plot.legend.click_policy="hide"
    plot.legend.label_text_font_size = '8pt'
    plot.toolbar.logo = None
    plot.toolbar_location = None
    return plot, source