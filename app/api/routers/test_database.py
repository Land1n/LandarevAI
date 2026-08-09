from app.core.dependencies import get_message_service,MessageService
from app.database.database import create_db_and_tables
from app.schemas.message import MessageShema
from app.models.message import MessageModel

from fastapi import APIRouter,Depends

router = APIRouter(
    prefix="/api/v1/test",
    tags=["Test DataBase"],
)

@router.get("/message/{message_id}", response_model=None)
def get_message(message_id: int, service: MessageService = Depends(get_message_service)) -> dict:
    create_db_and_tables()
    message = service.read_message(message_id)
    if message is None:
        return {"result": "Message not found"}
    return {"result":message}

@router.get("/message", response_model=None)
def get_messages(service: MessageService = Depends(get_message_service)) -> dict:
    create_db_and_tables()
    return {"result" :service.list_messages()}

@router.post("/message", response_model=None)
def create_message(message: MessageShema,service: MessageService = Depends(get_message_service)) -> dict:
    create_db_and_tables()
    new_message = MessageModel(**message.model_dump())
    return {"result" : service.create_message(new_message)}

@router.delete("/message/{message_id}", response_model=None)
def delete_message(message_id: int, service: MessageService = Depends(get_message_service)) -> dict:
    create_db_and_tables()
    return {"result" : service.delete_message(message_id)}

@router.put("/message/{message_id}", response_model=None)
def update_message(message_id: int, message: MessageShema, service: MessageService = Depends(get_message_service)) -> dict:
    new_message = MessageModel(**message.model_dump())
    return {"result" : service.update_message(message_id=message_id,message=new_message)}
