__author__ = 'zhangxa'

'''
用来将不同的request分发给对应的handler.
'''
class Dispatcher:
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.handler = {}

    def add_handler(self,req,handler):
        self.handler[req] = handler

    def revmove_handler(self,req,handler):
        self.handler.pop(req)

    def dispatch(self,req):
        handler = self.handler[req]
        handler.process_request(req)


class HttpRequestDispatcher(Dispatcher):
    pass