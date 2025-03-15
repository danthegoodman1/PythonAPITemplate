from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
import logging, json
from logging import Formatter
import uvicorn


# https://www.sheshbabu.com/posts/fastapi-structured-json-logging/
class JsonFormatter(Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        json_record = {}
        json_record["message"] = record.getMessage()
        json_record["level"] = record.levelname.lower()
        return json.dumps(json_record)


logger = logging.root
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())  # use JSON formatting
logger.handlers = [handler]
logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.get("/hc")
async def hc(request: Request):
    return {"msg": "alive"}

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            websocket_data = await websocket.receive_text()
            print(websocket_data)
            await websocket.send_text("got it!")
    except WebSocketDisconnect:
        print("WebSocket connection closed")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None) # make it use the configured logger above (weird, ik)
