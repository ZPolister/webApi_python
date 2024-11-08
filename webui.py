import webApi
from webApi.route import route, Get, Post
from webApi.constants import RequestMethod
from webApi.constants import ResponseMethod
from webApi.exceptionHandler import exception_handler
import webApi.interceptor as interceptor
from webApi.responseHandler import response_handler
import traceback


class interc(interceptor.Interceptor):
    def __init__(self):
        interceptor.Interceptor.__init__(self)

    def run(self):
        self.set_allow_request_method(RequestMethod.GET.value)
        if self.check_method():
            return

        return response_handler(200, {"inter_e": "拦截器拦截了"}, ResponseMethod.JSON)


interceptor.interceptor_manager.add_interceptor(interc())


@Get('/hello')
def index(request):
    return {"message": "Hello World"}


@Post('/hi/2')
def index2(request):
    return {"message": 'hi'}


@Post('/hi/{id}')
def index3(request):
    id = request['path_values']['id']
    return {"message": id}


@exception_handler(Exception, ResponseMethod.JSON)
def error_handler():
    return {'error': traceback.format_exc()}


if __name__ == '__main__':
    webApi.run('localhost', 8003)
