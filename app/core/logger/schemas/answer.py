from sqlmodel import SQLModel

from typing import Union,List,TypeVar,Generic

import logging

T = TypeVar('T', bound=SQLModel)

class Answer(SQLModel, Generic[T]):
    level: int = logging.DEBUG
    description: str = "Successful"
    result: Union[T,List[T],bool,None] = None