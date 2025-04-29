import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import logging
from pathlib import Path


REDIRECT_TARGET = "http://127.0.0.1:8000"
print(f"REDIRECT_TARGET: {REDIRECT_TARGET}\nCHANGE TARGET? [y/n]")
if input().lower() == "y":
    REDIRECT_TARGET = input("REDIRECT_TARGET: ")


log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "redirect.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

app = FastAPI()

@app.middleware("http")
async def log_and_redirect(request: Request, call_next):
    client_ip = request.client.host
    path = request.url.path
    full_url = str(request.url)
    target_url = f"{REDIRECT_TARGET}{path}"

    logging.info(f"{client_ip} -> {full_url} => {target_url}")

    return RedirectResponse(url=target_url)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)