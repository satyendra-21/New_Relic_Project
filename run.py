import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

from crud_app.main import app as crud_app
from log_fetcher.main import app as log_fetcher_app

app = FastAPI(title="New Relic Unified Backend", docs_url=None, redoc_url=None)

app.mount("/crud", crud_app)
app.mount("/logs", log_fetcher_app)

@app.get("/docs", include_in_schema=False)
def redirect_docs():
    return RedirectResponse(url="/crud/docs")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>API Gateway</title>
            <style>
                body { font-family: -apple-system, sans-serif; padding: 40px; background: #f4f4f9; color: #333; }
                h1 { color: #2c3e50; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
                a { color: #3498db; text-decoration: none; font-weight: bold; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🚀 New Relic Unified Backend Running</h1>
            <div class="card">
                <h2>🎫 Ticketing CRUD API</h2>
                <p>Manage support tickets stored in the database.</p>
                <p>👉 <a href="/crud/docs">Swagger UI for Ticketing API</a></p>
            </div>
            <div class="card">
                <h2>📊 Log Fetcher API</h2>
                <p>Fetch and snapshot logs directly from New Relic NRDB.</p>
                <p>👉 <a href="/logs/docs">Swagger UI for Log Fetcher API</a></p>
            </div>
        </body>
    </html>
    """
