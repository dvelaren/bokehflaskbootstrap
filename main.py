try:
    import asyncio
except ImportError:
    raise RuntimeError("This example requries Python3 / asyncio")

from flask import Flask, render_template, url_for

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from bokeh.themes import Theme


app = Flask(__name__)

def modify_doc(doc):
    import numpy as np
    import pandas as pd

    x = np.linspace(0,2*np.pi,1000)
    noise = np.random.normal(0,0.1,1000)
    y = np.sin(x) + noise
    df = pd.DataFrame({'x':x,'y':y})
    # df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    # plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
    #               title="Sea Surface Temperature at 43.18, -70.43")
    # plot.line('time', 'temperature', source=source)

    plot = figure(x_axis_label='Time',y_axis_label='Amplitude', y_range=(-1.5, 1.5))
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


# can't use shortcuts here, since we are passing to low level BokehTornado
bkapp = Application(FunctionHandler(modify_doc))

# This is so that if this app is run using something like "gunicorn -w 4" then
# each process will listen on its own port
sockets, port = bind_sockets("127.0.0.1", 0)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/graph')
def graph():
    # script = server_document('http://localhost:5006/bkapp')
    script = server_document('http://localhost:%d/bkapp' % port)
    return render_template("graph.html", script=script, template="Flask")

def bk_worker():
    # # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # # processes, see e.g. flask_gunicorn_embed.py
    # server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    # server.start()
    # server.io_loop.start()
    asyncio.set_event_loop(asyncio.new_event_loop())

    bokeh_tornado = BokehTornado({'/bkapp': bkapp}, extra_websocket_origins=["localhost:8000","0.0.0.0:8000","0.0.0.0:5000","localhost:5000"])
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)