from app.database.database import create_db_and_tables

from app.core.dependencies import (
    get_message_service, MessageService,
    get_role_service, RoleService,
    get_chat_service, ChatService
)

from app.schemas.message import MessageShema
from app.schemas.role import RoleSchema
from app.schemas.chat import ChatShema, ChatResponse

from app.models.message import MessageModel
from app.models.role import RoleModel
from app.models.chat import ChatModel

from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v1/test",
    tags=["Test DataBase"],
)

router_message =APIRouter(
    prefix="/api/v1/test",
    tags=["Test DataBase Messages"],
)
router_role =APIRouter(
    prefix="/api/v1/test",
    tags=["Test DataBase Role"],
)
router_chat =APIRouter(
    prefix="/api/v1/test",
    tags=["Test DataBase Chat"],
)
router.include_router(router_role)
router.include_router(router_message)
router.include_router(router_chat)

# --- Message endpoints ---

@router_message.get("/message/{message_id}")
def get_message(message_id: int, service: MessageService = Depends(get_message_service)):
    create_db_and_tables()
    message = service.read_message(message_id)
    if message is None:
        return {"result": "Message not found"}
    return {"result": message}

@router_message.get("/message")
def get_messages(service: MessageService = Depends(get_message_service)):
    create_db_and_tables()
    return {"result": service.list_messages()}

@router_message.post("/message")
def create_message(message: MessageShema, service: MessageService = Depends(get_message_service)):
    create_db_and_tables()
    new_message = MessageModel(**message.model_dump())
    return {"result": service.create_message(new_message)}

@router_message.delete("/message/{message_id}")
def delete_message(message_id: int, service: MessageService = Depends(get_message_service)):
    create_db_and_tables()
    return {"result": service.delete_message(message_id)}

@router_message.put("/message/{message_id}")
def update_message(message_id: int, message: MessageShema, service: MessageService = Depends(get_message_service)):
    new_message = MessageModel(text=message.text)
    return {"result": service.update_message(message_id, new_message)}

# --- Role endpoints ---

@router_role.get("/role/{role_id}")
def get_role(role_id: int, service: RoleService = Depends(get_role_service)):
    create_db_and_tables()
    role = service.read_role_by_id(role_id)
    if role is None:
        return {"result": "Role not found"}
    return {"result": role}

@router_role.get("/role")
def get_roles(service: RoleService = Depends(get_role_service)):
    create_db_and_tables()
    return {"result": service.list_roles()}

@router_role.post("/role")
def create_role(role: RoleSchema, service: RoleService = Depends(get_role_service)):
    create_db_and_tables()
    new_role = RoleModel(name=role.name)
    return {"result": service.create_role(new_role)}

@router_role.delete("/role/{role_id}")
def delete_role(role_id: int, service: RoleService = Depends(get_role_service)):
    create_db_and_tables()
    return {"result": service.delete_role(role_id)}

@router_role.put("/role/{role_id}")
def update_role(role_id: int, role: RoleSchema, service: RoleService = Depends(get_role_service)):
    new_role = RoleModel(**role.model_dump())
    return {"result": service.update_role(role_id, new_role)}

# --- Chat endpoints ---

@router_chat.get("/chat")
def get_chats(service: ChatService = Depends(get_chat_service)):
    create_db_and_tables()
    return {"result": service.list_chats()}

@router_chat.get("/chat/{chat_id}")
def get_chat(chat_id: int, service: ChatService = Depends(get_chat_service)) -> dict:
    create_db_and_tables()
    chat = service.read_chat_by_id(chat_id)

    if chat is None:
        return {"result":"Not found"}
    return {"result": ChatResponse.model_validate(chat).model_dump()}

@router_chat.post("/chat")
def create_chat(chat: ChatShema, service: ChatService = Depends(get_chat_service)):
    create_db_and_tables()
    new_chat = ChatModel(**chat.model_dump())
    return {"result": service.create_chat(new_chat)}

@router_chat.put("/chat/{chat_id}")
def update_chat(chat_id: int, chat: ChatShema, service: ChatService = Depends(get_chat_service)):
    new_chat = ChatModel(**chat.model_dump())
    return {"result": service.update_chat(chat_id, new_chat)}

@router_chat.delete("/chat/{chat_id}")
def delete_chat(chat_id: int, service: ChatService = Depends(get_chat_service)):
    create_db_and_tables()
    return {"result": service.delete_chat(chat_id)}

@router_chat.post("/chat/{chat_id}/message")
def add_message_to_chat(
    chat_id: int,
    message: MessageShema,
    service: ChatService = Depends(get_chat_service)
):
    create_db_and_tables()
    new_message = MessageModel(**message.model_dump())
    result = service.add_message_to_chat(chat_id, new_message)
    return {"result": result}