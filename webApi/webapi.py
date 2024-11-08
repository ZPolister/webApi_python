import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from webApi.constants import ResponseMethod, RequestMethod
import webApi.route as router
from webApi.requestHandler import parse_request
from webApi.responseHandler import response_handler
import webApi.localData as localData
import traceback

thread_pool = ThreadPoolExecutor(max_workers=10)


def client_handler(client_socket: socket, client_ip: str):

    with client_socket:
        request_data = client_socket.recv(1024).decode('utf-8')
        if not request_data:
            return

        try:
            localData.local_data = threading.local()
            localData.local_data.response_header = {}
            localData.local_data.client_ip = client_ip
            request = parse_request(request_data)
            localData.local_data.request = request
            handler = router.routes.find(request["path"], RequestMethod[request["method"]])
            if handler:
                response = handler(request)
            else:
                response = response_handler(404, {"error": "Not Found"}, ResponseMethod.JSON)
        except Exception as e:
            traceback.print_exc()
            response = response_handler(400, {"error": "Bad Request"}, ResponseMethod.JSON)

        client_socket.sendall(response.encode('utf-8'))


def run(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"服务已启动，地址：{host}:{port}")

        while True:
            client_socket, client_ip = server_socket.accept()
            thread_pool.submit(client_handler, client_socket, client_ip)
