from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from exception import OperatedException, ErrorCode

"""
출처: https://velog.io/@power0080/FastAPI-X-Python-실무에서-바로-쓰는-FastAPI-전역-에러-처리
"""


def set_error_handlers(app: FastAPI):

    # 클라이언트의 요청 처리에 따라 발생한 예외는 OperatedException로 처리
    @app.exception_handler(OperatedException)
    async def operated_exception_handler(
        request: Request, exc: OperatedException
    ) -> JSONResponse:
        # log service를 통해 error 발생 로그 적재
        log_service.insert_client_log(request=request)

        # error response
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code.value,
                "reason": exc.code.name,
                "message": exc.detail,
            },
        )

    # 그 외 요청을 처리하다가 서버에서 예상치 못한 예외가 발생한 예외 처리
    @app.exception_handler(Exception)
    async def server_side_exception_handler(request: Request, exc: Exception):
        # log 적재
        log_service.insert_server_log(request=request, exception=exc)

        # error response
        return JSONResponse(
            status_code=500, content={"code": ErrorCode.UNEXPECTED_ERROR.value}
        )
