import logging

from flask import Flask, render_template

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop

app = Flask(__name__)

def modify_doc(doc):
    import numpy as np
    import pandas as pd

    x = np.linspace(0,10*np.pi,1000)
    noise = np.random.normal(0,0.1,1000)
    y = 2*np.sin(x) + noise
    df = pd.DataFrame({'x':x,'y':y})
    # df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    # plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
    #               title="Sea Surface Temperature at 43.18, -70.43")
    # plot.line('time', 'temperature', source=source)

    plot = figure(x_axis_label='Time',y_axis_label='Amplitude', y_range=(-0.5, 2.5))
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

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/graph', methods=['GET'])
def graph():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("graph.html", script=script, template="Flask")

def bk_worker():
    # # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["0.0.0.0","localhost","127.0.0.1:5000","siseflask.dis.eafit.edu.co","192.168.10.130:5000","sise.dis.eafit.edu.co"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:5000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(host='0.0.0.0', port=5000, debug=False)
# else:
	# gunicorn_logger = logging.getLogger('gunicorn.error')
	# gunicorn_logger.setLevel(logging.INFO)
	
	# tornado_access_logger = logging.getLogger('tornado.access')
	# tornado_access_logger.setLevel(logging.INFO)
	# tornado_access_handler = logging.FileHandler('logs/error_log.log')
	# tornado_access_logger.addHandler(tornado_access_handler)

	# tornado_application_logger = logging.getLogger('tornado.application')
	# tornado_application_logger.setLevel(logging.INFO)
	# tornado_application_handler = logging.FileHandler('logs/error_log.log')
	# tornado_application_logger.addHandler(tornado_application_handler)

	# app.logger.addHandler(gunicorn_logger.handlers)
	# app.logger.addHandler(tornado_access_logger.handlers)
	# app.logger.addHandler(tornado_application_logger.handlers)
	# app.logger.setLevel(logging.INFO)
