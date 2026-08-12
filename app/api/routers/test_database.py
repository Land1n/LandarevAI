from app.database.database import create_db_and_tables

from app.core.dependencies import get_message_service,MessageService,get_role_service,RoleService

from app.schemas.message import MessageShema
from app.schemas.role import RoleSchema

from app.models.message import MessageModel
from app.models.role import RoleModel

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
    new_message = MessageModel(
        text=message.text,
        role_id=message.role_id
    )
    return {"result" : service.update_message(message_id=message_id,message=new_message)}


@router.get("/role/{role_id}", response_model=None)
def get_role(message_id: int, service: RoleService = Depends(get_role_service)) -> dict:
    create_db_and_tables()
    role = service.read_role_by_id(message_id)
    if role is None:
        return {"result": "Role not found"}
    return {"result":role}

@router.get("/role", response_model=None)
def get_roles(service: RoleService = Depends(get_role_service)) -> dict:
    create_db_and_tables()
    return {"result" :service.list_roles()}

@router.post("/role", response_model=None)
def create_role(role: RoleSchema,service: RoleService = Depends(get_role_service)) -> dict:
    create_db_and_tables()
    new_role = RoleModel(name=role.name)
    return {"result" : service.create_role(new_role)}

@router.delete("/role/{role_id}", response_model=None)
def delete_role(role_id: int, service: RoleService = Depends(get_role_service)) -> dict:
    create_db_and_tables()
    return {"result" : service.delete_role(role_id)}

@router.put("/role/{role_id}", response_model=None)
def update_message(role_id: int, message: MessageShema, service: RoleService = Depends(get_role_service)) -> dict:
    new_role = RoleModel(**message.model_dump())
    return {"result" : service.update_role(role_id=role_id,role=new_role)}
