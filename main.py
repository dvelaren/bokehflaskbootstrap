import logging

from flask import Flask, render_template, url_for

from bokeh_app.server import bk_worker

from tornado.ioloop import IOLoop
from bokeh.embed import server_document
from threading import Thread

app = Flask(__name__)

Thread(target=bk_worker).start()

@app.route('/')
@app.route('/home')
def home():
    script = server_document(url=r'/bkapp/todos', relative_urls=True)
    # script = server_document('http://localhost:5006/bkapp')
    # script = server_document('http://siseflask.dis.eafit.edu.co:%d/bkapp' % port) # flask_gunicorn_embed.py
    return render_template("graph.html", script=script, template="Flask")
    # return render_template("index.html")

@app.route('/pieza', methods=['GET'])
def graph1():
    script = server_document(url=r'/bkapp/pieza', relative_urls=True)
    # script = server_document('http://localhost:5006/bkapp')
    # script = server_document('http://siseflask.dis.eafit.edu.co:%d/bkapp' % port) # flask_gunicorn_embed.py
    return render_template("graph.html", script=script, template="Flask")

@app.route('/sala', methods=['GET'])
def graph2():
    script = server_document(url=r'/bkapp/sala', relative_urls=True)
    # script = server_document('http://localhost:5006/bkapp')
    # script = server_document('http://siseflask.dis.eafit.edu.co:%d/bkapp' % port) # flask_gunicorn_embed.py
    return render_template("graph.html", script=script, template="Flask")

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:5000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(host='0.0.0.0', port=5000, debug=False)