from typing import Literal
from webApi.constants import ResponseMethod
from functools import wraps

# 全局异常处理列表
_exception_handlers = {}


def exception_handler(exc_type, response_method: Literal[ResponseMethod.JSON] = ResponseMethod.JSON):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 执行处理异常的函数并返回
            return response_method, func(*args, **kwargs)

        _exception_handlers[exc_type] = wrapper
        return wrapper

    return decorator
