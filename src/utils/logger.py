import logging
import os
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

import colorlog

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def get_logger(name: str):
    # Console log
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler.setFormatter(console_formatter)

    # 파일 로그 핸들러 (시간과 크기 단위로 로그를 롤링)
    file_handler = TimedRotatingFileHandler(
        filename=f"{log_dir}/my_app.log",
        when='midnight',
        interval=1,
        backupCount=7,  # 일주일간의 로그 유지
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 크기 단위로 롤링되는 핸들러 (200MB마다 롤링)
    size_handler = RotatingFileHandler(
        filename=f"{log_dir}/my_app.log",
        maxBytes=200 * 1024 * 1024,  # 200MB
        backupCount=5,  # 로그 파일 최대 5개
        encoding='utf-8'
    )
    size_handler.setLevel(logging.INFO)
    size_handler.setFormatter(file_formatter)

    # 루트 로거 설정
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 전체 로그 레벨 설정
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(size_handler)

    return logger
