from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os
import uvicorn

app = FastAPI()

players = set()

@app.get("/")
async def root():
    return {"status": "online"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    players.add(websocket)

    try:
        while True:
            message = await websocket.receive_text()

            for player in players:
                if player != websocket:
                    await player.send_text(message)

    except WebSocketDisconnect:
        players.discard(websocket)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
