import threading
from typing import Dict

# 创建一个线程局部变量对象
local_data: threading.local = threading.local()


def setResponseHeader(header: Dict[str, str]):
    local_data.response_header.update(header)

