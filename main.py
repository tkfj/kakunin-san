from fastapi import FastAPI, Request, Response

app = FastAPI(title="確認さん")

@app.get("/")
async def get_ua(request: Request, response: Response):
    """
    ブラウザの User-Agent と UA-CH (User-Agent Client Hints) ヘッダーを返します。
    """
    # サーバー側から「詳細な情報（High Entropy）を要求する」と宣言
    # これにより、ブラウザに対して追加のヘッダー送信を促す
    response.headers["Accept-CH"] = "sec-ch-ua-full-version-list, sec-ch-ua-arch, sec-ch-ua-model"
    # ユーザーに「次回のアクセスから送ってね」と伝えるための指示（重要）
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

    return {
        "message": "Browser User-Agent and Client Hints information",
        "ua_info": ua_info
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

