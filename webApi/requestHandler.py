from typing import Dict, Any, Literal, List
import json
from urllib.parse import urlparse, parse_qs
from webApi.constants import RequestMethod, ResponseMethod


# 解析请求行、请求头和 JSON 请求体
def parse_request(request: str) -> Dict[str, Any]:
    lines = request.splitlines()
    method, path, _ = lines[0].split()
    parse_url = urlparse(path)
    query_params = {key: value[0] if len(value) == 1 else value for key, value in parse_qs(parse_url.query).items()}
    headers = {}
    body = ''

    # 解析请求头
    header_end_index = lines.index('')
    for line in lines[1:header_end_index]:
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()

    # 解析请求体（只做了json）
    if header_end_index + 1 < len(lines) and headers["Content-Type"] == "application/json":
        body = "\n".join(lines[header_end_index + 1:])
    json_body = json.loads(body) if body else {}

    return {
        "method": method,
        "path": parse_url.path,
        "query": query_params,
        "headers": headers,
        "body": json_body
    }


if __name__ == '__main__':
    pass