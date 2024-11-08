from webApi.route import Get, Post, Put, Delete
from webApi.constants import ResponseMethod
import webApi


@Post('/hello/{id}', response_type=ResponseMethod.JSON)
def index(request):
    print(request['query']['test'])
    print(request['body'])
    print(request['path_values']['id'])
    return {"message": "Hello World"}


@Post('/hello', ResponseMethod.HTML)
def handle(request):
    return "<h1>hello world</h1>"


@Delete('/hello')
def handle(request):
    return {"message": "Hello World"}


@Put('/hello')
def handle(request):
    return {"message": "Hello World"}


if __name__ == '__main__':
    webApi.run('localhost', 8003)  # 监听地址，端口号
