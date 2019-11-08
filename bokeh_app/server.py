from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from utils.server_config import SERVER_IP
from bokeh_app.app1 import modify_doc
from bokeh_app.app2 import modify_doc2

def bk_worker():
    # server = Server({'/bkapp': modify_doc, '/test2': modify_doc2}, io_loop=IOLoop(), port=5006, allow_websocket_origin=['*'])
    # server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), port=5006, allow_websocket_origin=['*'])
    # kws = {'port': 5006, 'prefix': '/bkapp/test1', 'allow_websocket_origin': ['*']}
    # server = Server(modify_doc, io_loop=IOLoop(), **kws)
    kws = {'port': 5006, 'prefix': '/bkapp', 'allow_websocket_origin': ['*']}
    server = Server({'/app1': modify_doc, '/app2': modify_doc2}, io_loop=IOLoop(), **kws)
    server.start()
    server.io_loop.start()