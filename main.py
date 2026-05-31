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

    ua_keys = [
        "user-agent",
        "sec-ch-ua",
        "sec-ch-ua-full-version-list",
        "sec-ch-ua-mobile",
        "sec-ch-ua-platform",
        "sec-ch-ua-platform-version",
        "sec-ch-ua-model",
        "sec-ch-ua-arch",
    ]
    other_keys = [
        "accept",
        "accept-language",
        "accept-encoding",
        "referer",
        "dnt", # Do Not Track
        "upgrade-insecure-requests",
        "sec-fetch-site",
        "sec-fetch-mode",
        "sec-fetch-dest",
        "sec-fetch-user",
    ]

    # レスポンス用の辞書を構築
    ua_headers = {}
    other_headers = {}
    for header in request.headers.keys():
        h = header.lower()
        if h in ua_keys:
            ua_headers[header] = request.headers.get(header)
        elif h in other_keys:
            other_headers[header] = request.headers.get(header)
        
    # クライアントIPの取得
    # x_forwarded_for = request.headers.get("x-forwarded-for")
    # if x_forwarded_for:
    #     # Comma-separated list の最初のIPが、真のクライアントIP
    #     client_ip = x_forwarded_for.split(",")[0].strip()
    cf_connecting_ip = request.headers.get("cf-connecting-ip")
    if cf_connecting_ip:
        client_ip = cf_connecting_ip
    else:
        client_ip = request.client.host
    detected_country = request.headers.get("cf-ipcountry")
    detected_city = request.headers.get("cf-city")
    detected_continent = request.headers.get("cf-ipcontinent")
    detected_asn = request.headers.get("cf-asn")
    detected_as_org = request.headers.get("cf-as-organization")
    network_info = {
        "ip": client_ip,
    }
    if detected_country:
        network_info["country"] = detected_country
    if detected_city:
        network_info["city"] = detected_city
    if detected_continent:
        network_info["continent"] = detected_continent
    if detected_asn:
        network_info["as_number"] = detected_asn
    if detected_as_org:
        network_info["as_organization"] = detected_as_org

    ret_values = {
        "status":"OK",
        "message": "Hi, this is kakunin-san!"
    }
    if ua_headers:
        ret_values["ua"] = ua_headers
    if network_info:
        ret_values["network_info"] = network_info
    if other_headers:
        ret_values["headers"] = other_headers
    return JSONResponse(content=ret_values)


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

