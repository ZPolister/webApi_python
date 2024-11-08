import re
from typing import List


class Interceptor:
    def __init__(self):
        # 允许的条件
        self.allow_methods = []
        self.allow_routes = []
        self.allow_ips = []

        self.request_route_path = ''
        self.request_method = ''
        self.request_headers = ''
        self.request_body = ''
        self.request_query = ''
        self.request_ip = ''

    def invoke_info(self):
        import webApi.localData as localData
        request = localData.local_data.request
        self.request_route_path = request['path']
        self.request_method = request['method']
        self.request_headers = request['headers']
        self.request_body = request['body']
        self.request_query = request['query']
        self.request_ip, _ = localData.local_data.client_ip

    def set_allow_request_method(self, methods: List[str]):
        """设置允许的请求方法列表"""
        self.allow_methods = methods
        return self

    def set_allow_request_route(self, routes: List[str]):
        """设置允许的请求路由列表"""
        self.allow_routes = [re.compile(route.replace('*', '.*')) for route in routes]
        return self

    def set_allow_request_ip(self, ip_list: List[str]):
        """设置允许的 IP 列表"""
        self.allow_ips = [re.compile(ip.replace('*', '.*')) for ip in ip_list]
        return self

    def check_method(self):
        """检查请求方法是否允许"""
        return not self.allow_methods or self.request_method in self.allow_methods

    def check_route(self):
        """检查请求路径是否符合"""
        return not self.allow_routes or any(pattern.match(self.request_route_path) for pattern in self.allow_routes)

    def check_ip(self):
        """检查请求 IP 是否允许"""
        return not self.allow_ips or any(pattern.match(self.request_ip) for pattern in self.allow_ips)

    def run(self):
        return None


class InterceptorManager:
    def __init__(self):
        self.interceptor_list: List[Interceptor] = []
        self.allow_request_list: List[str] = []

    def add_interceptor(self, interceptor: Interceptor):
        """添加一个拦截器到列表中"""
        self.interceptor_list.append(interceptor)
        return self

    def add_allow_request_ip(self, allow_request_ip: str):
        """添加一个允许的 IP 地址"""
        self.allow_request_list.append(allow_request_ip)
        return self

    def run_all(self):
        """运行所有拦截器"""
        for interceptor in self.interceptor_list:
            interceptor.invoke_info()
            result = interceptor.run()
            if result is not None:
                return result
        return None


interceptor_manager = InterceptorManager()
