from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="kakunin-san", description="A simple API to check User-Agent and Client Hints", version="1.0.0")

@app.get("/")
async def get_ua(request: Request, response: Response):
    """
    ブラウザの User-Agent と UA-CH (User-Agent Client Hints) ヘッダーを返します。
    """
    requested_hints = "sec-ch-ua-full-version-list, sec-ch-ua-arch, sec-ch-ua-model, sec-ch-ua-platform-version"
    response.headers["Accept-CH"] = requested_hints
    response.headers["Critical-CH"] = requested_hints
    response.headers["Permissions-Policy"] = "ch-ua-full-version-list=(self), ch-ua-arch=(self), ch-ua-model=(self), ch-ua-platform-version=(self)"

    target_headers = [
        "user-agent",
        "sec-ch-ua",
        "sec-ch-ua-full-version-list",
        "sec-ch-ua-mobile",
        "sec-ch-ua-platform",
        "sec-ch-ua-platform-version",
        "sec-ch-ua-model",
        "sec-ch-ua-arch",
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
        "message": "Hi, this is kakunin-san!",
        "ua_info": ua_info,
        "client_ip": client_ip
    }

@app.api_route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def catch_all(request: Request):
    raise HTTPException(status_code=405, detail="Method Not Allowed")

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def catch_all(request: Request):
    raise HTTPException(status_code=404, detail="Not Found")

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

