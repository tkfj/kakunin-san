from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="確認さん")

@app.get("/")
async def get_ua(request: Request, response: Response):
    """
    ブラウザの User-Agent と UA-CH (User-Agent Client Hints) ヘッダーを返します。
    """
    response.headers["Accept-CH"] = "sec-ch-ua-full-version-list, sec-ch-ua-arch, sec-ch-ua-model"
    response.headers["Permissions-Policy"] = "ch-ua-full-version-list=(self)"

    # 取得したいヘッダーのリスト
    target_headers = [
        "user-agent",
        "web-agent",
        "sec-ch-ua",
        "sec-ch-ua-mobile",
        "sec-ch-ua-platform",
        "sec-ch-ua-model",
        "sec-ch-ua-arch",
        "sec-ch-ua-platform-version",
    ]

    # レスポンス用の辞書を構築
    ua_info = {}
    for header in target_headers:
        value = request.headers.get(header)
        if value:
            ua_info[header] = value

    # クライアントIPの取得
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # Comma-separated list の最初のIPが、真のクライアントIP
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host
        
    return {
        "status":"OK",
        "ua_info": ua_info,
        "client_ip": client_ip
    }

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request):
    return JSONResponse(
        status_code=404,
        content={
            "status": "Error",
            "message": "404 Not Found",
        }
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "Error",
            "message": f"{exc.status_code} {exc.detail}"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

