from typing import Callable, Literal, List, Dict, Any

from functools import wraps
import re
from webApi.constants import RequestMethod, ResponseMethod
from webApi.exceptionHandler import _exception_handlers
from webApi.responseHandler import response_handler
from webApi.interceptor import interceptor_manager
import traceback


class RouteNode:
    def __init__(self, route_str: str):
        self.route: str = route_str
        self.func: Dict[
            Literal[RequestMethod.POST, RequestMethod.PUT, RequestMethod.GET, RequestMethod.DELETE], Any] = {
            RequestMethod.POST: None,
            RequestMethod.PUT: None,
            RequestMethod.GET: None,
            RequestMethod.DELETE: None,
        }
        self.children: Dict[str, RouteNode] = {}

    def add_child(self, child):
        self.children[child.route] = child

    def find(self, route_str: str,
             method: Literal[RequestMethod.POST, RequestMethod.PUT, RequestMethod.GET, RequestMethod.DELETE]):

        node = self
        if route_str.startswith('/'):
            route_str = route_str[1:]
        route_list: List[str] = route_str.split("/")
        for x in route_list:
            new_node = node.children.get(x)
            if new_node is None:
                new_node = node.children.get('{}')
                if new_node is None:
                    return None
            node = new_node

        return node.func[method]

    def insert(self, route_str: str, handler,
               method: Literal[RequestMethod.POST, RequestMethod.PUT, RequestMethod.GET, RequestMethod.DELETE]) -> None:

        node = self
        if route_str.startswith('/'):
            route_str = route_str[1:]

        route_list: List[str] = route_str.split("/")
        for x in route_list:
            if x.startswith('{') and x.endswith('}'):
                x = '{}'
            new_node = node.children.get(x)
            if new_node is None:
                new_node = RouteNode(route_str)
                node.children[x] = new_node

            node = new_node

        if node.func[method]:
            print(f"注册路由失败:{handler}\n")
            return

        node.func[method] = handler


routes: RouteNode = RouteNode('/')


def extract_path_params(path: str, request_path: str):
    """使用正则表达式匹配 {variable} 的占位符并替换为捕获组 (.+)"""
    pattern = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', path)
    match = re.match(pattern, request_path)

    if match:
        return match.groupdict()
    else:
        return None


# 方法增强，识别请求方法和请求路径
def route(path: str, method: Literal[RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE],
          response_type=ResponseMethod.JSON):
    def decorator(func: Callable):

        @wraps(func)
        def wrapper(*args, response_method=response_type, **kwargs):
            status_code = 200
            response_method = response_method
            request_path = args[0]['path']
            path_values = extract_path_params(path, request_path)
            if path_values:
                args[0]['path_values'] = path_values
            try:
                interceptor_result = interceptor_manager.run_all()
                if interceptor_result:
                    return interceptor_result
                body = func(*args, **kwargs)
            except Exception as e:
                if type(e) in _exception_handlers:
                    response_method, body = _exception_handlers[type(e)]()
                else:
                    traceback.print_exc()
                    status_code, body = 500, None
            return response_handler(status_code, body, response_method)

        routes.insert(path, wrapper, method)
        return wrapper

    return decorator


def Get(path: str, response_type=ResponseMethod.JSON):
    return route(path, RequestMethod.GET, response_type)


def Post(path: str, response_type=ResponseMethod.JSON):
    return route(path, RequestMethod.POST, response_type)


def Put(path: str, response_type=ResponseMethod.JSON):
    return route(path, RequestMethod.PUT, response_type)


def Delete(path: str, response_type=ResponseMethod.JSON):
    return route(path, RequestMethod.DELETE, response_type)
