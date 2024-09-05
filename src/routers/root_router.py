from fastapi import APIRouter

from src.utils.logger import get_logger

router = APIRouter()
log = get_logger(__name__)


@router.get("/healthcheck")
def health_check():
    log.info("health_check")
    return "healthy"
