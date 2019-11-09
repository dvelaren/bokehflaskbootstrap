from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from utils.server_config import SERVER_IP
from bokeh_app.plots import *

def bk_worker():
    # server = Server({'/bkapp': modify_doc, '/test2': modify_doc2}, io_loop=IOLoop(), port=5006, allow_websocket_origin=['*'])
    # server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), port=5006, allow_websocket_origin=['*'])
    # kws = {'port': 5006, 'prefix': '/bkapp/test1', 'allow_websocket_origin': ['*']}
    # server = Server(modify_doc, io_loop=IOLoop(), **kws)
    kws = {'port': 5006, 'prefix': '/bkapp', 'allow_websocket_origin': ['*']}
    server = Server({'/todos': modify_doc_all, '/pieza': modify_doc_pieza, '/sala': modify_doc_sala}, io_loop=IOLoop(), **kws)
    server.start()
    server.io_loop.start()