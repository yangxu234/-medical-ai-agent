from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "success") -> dict:
    """成功响应"""
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error_response(message: str = "error", code: int = 400) -> dict:
    """错误响应"""
    return {
        "code": code,
        "message": message,
        "data": None
    }
