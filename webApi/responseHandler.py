import json
from typing import Dict, Any, Literal

from webApi.constants import ResponseMethod
from webApi.localData import setResponseHeader, local_data
import webApi.localData as localData


# http返回信息状态枚举
status_messages = {200: 'OK', 400: 'Bad Request', 404: 'Not Found', 500: 'Internal Server Error'}


# 响应处理
def response_handler(status_code: int, body: Any, response_type: Literal[ResponseMethod.JSON]):
    setResponseHeader(response_type.value)
    return build_response(status_code, localData.local_data.response_header, body)


# 构建响应报文
def build_response(status_code: int, headers: Dict[str, str], body: Any) -> str:
    status_line = f"HTTP/1.1 {status_code} {status_messages.get(status_code, '')}"
    headers = "\r\n".join([f"{k}: {v}" for k, v in headers.items()])
    body = json.dumps(body) if isinstance(body, (dict, list)) else str(body)
    return f"{status_line}\r\n{headers}\r\n\r\n{body}"
