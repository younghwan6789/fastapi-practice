import asyncio
import time

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from src.utils.logger import get_logger

router = APIRouter()
log = get_logger(__name__)

event_queue = asyncio.Queue()


@router.get("/healthcheck")
def health_check():
    log.info("health_check")
    return "healthy"


# SSE 엔드포인트
@router.get("/notifications")
async def notifications():
    return StreamingResponse(event_stream(), media_type="text/event-stream")


async def event_stream():
    # while True:
    #     yield f"data: Notification at {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    #     await asyncio.sleep(5)  # 5초 간격으로 알림 전송
    while True:
        # 큐에서 새로운 데이터가 들어올 때까지 기다림
        data = await event_queue.get()
        yield f"data: {data}\n\n"


# 1회성으로 알림을 트리거하는 엔드포인트
@router.post("/trigger_event")
async def trigger_event():
    # body = await request.json()
    # message = body.get("message", "No message provided")

    message = f"data: Notification at {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    # 큐에 새로운 메시지 넣기
    await event_queue.put(message)
    return {"message": "Event triggered!"}
