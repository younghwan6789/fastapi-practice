import asyncio
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

# 각 사용자의 이벤트 스트림을 저장할 딕셔너리
user_streams: Dict[str, asyncio.Queue] = {}


# SSE 스트림을 사용자별로 구분하는 함수
async def event_stream(user_id: str):
    if user_id not in user_streams:
        user_streams[user_id] = asyncio.Queue()

    # 큐에서 데이터를 가져와 전송
    while True:
        data = await user_streams[user_id].get()
        yield f"data: {data}\n\n"


# SSE 엔드포인트: 사용자별로 SSE 연결
@app.get("/notifications/{user_id}")
async def notifications(user_id: str):
    return StreamingResponse(event_stream(user_id), media_type="text/event-stream")


# 특정 사용자에게 1회성 메시지 푸시
@app.post("/trigger_event/{user_id}")
async def trigger_event(user_id: str, request: Request):
    body = await request.json()
    message = body.get("message", "No message provided")

    # 해당 사용자의 큐에 메시지 넣기
    if user_id in user_streams:
        await user_streams[user_id].put(message)
        return {"message": "Event triggered for user", "user_id": user_id}
    else:
        return {"message": "User not connected", "user_id": user_id}
