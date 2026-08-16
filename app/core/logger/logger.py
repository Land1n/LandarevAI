from typing import Any

from app.core.config import settings
from app.core.logger.schemas.answer import Answer

from functools import wraps

import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)-9s %(white)s%(name)-15s - %(log_color)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={
        'name': {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
    }
)

handler.setFormatter(formatter)
logging.basicConfig(level=settings.LOGGING_LEVEL,handlers=[handler])

def convert_result(func):
    """Answer() -> Any, List[Any], Bool, None"""
    def wrapper(self,*args, **kwargs):
        answer:Answer = func(self, *args, **kwargs)
        return answer.result
    return wrapper

def logger(name:str):
    def decorator(func):
        @wraps(func)
        def wrapper(self,*args, **kwargs):
            logger = logging.getLogger(name)
            answer:Answer = func(self, *args, **kwargs)
            answer_string:str = f"{self.__class__.__name__:25} - {func.__name__:15} = [ {answer.description} ]"
            logger.log(answer.level, answer_string)
            return answer
        return wrapper
    return decorator