from enum import Enum


# 请求方法枚举
class RequestMethod(Enum):
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    GET = 'GET'


# 响应格式枚举
class ResponseMethod(Enum):
    JSON = {"Content-Type": "application/json"}
    HTML = {"Content-Type": "text/html"}
