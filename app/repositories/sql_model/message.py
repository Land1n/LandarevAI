from app.repositories.base.message import MessageRepository,MessageModel

from sqlmodel import Session,select

from typing import List,Optional

class SqlModelMessageRepository(MessageRepository):
    def __init__(self, session:Session ):
        self.session = session

    def read_message_by_id(self, message_id: int) -> Optional[MessageModel]:
        statement = select(MessageModel).where(MessageModel.id == message_id)
        message = self.session.exec(statement).first()
        return message

    def read_messages_all(self) -> List[MessageModel]:
        return list(self.session.exec(select(MessageModel)).all())

    def read_messages_by_role(self, role_name: str) -> List[MessageModel]:
        return [] # TODO: Пока не готово

    def create_message(self, message: MessageModel) -> bool:
        try:
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)
            return True
        except Exception as e:
            return False

    def update_message(self, message_id: int, message: MessageModel) -> bool:
        try:
            new_message = self.read_message_by_id(message_id)
            if (new_message != None):
                new_message.text = message.text
                self.session.add(new_message)
                self.session.commit()
                self.session.refresh(new_message)
                return True
            return False
        except Exception as e:
            return False

    def delete_message(self, message_id: int) -> bool:
        try:
            message = self.read_message_by_id(message_id)
            if (message != None):
                self.session.delete(message)
                self.session.commit()
                return True
            return False
        except Exception as e:
            return False
