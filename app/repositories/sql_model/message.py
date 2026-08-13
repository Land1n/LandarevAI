from app.repositories.base.message import MessageRepository,MessageModel

from sqlmodel import Session,select

from typing import List,Optional

import logging

class SqlModelMessageRepository(MessageRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, session:Session ):
        self.session = session

    def read_by_id(self, message_id: int) -> Optional[MessageModel]:
        self.logger.debug("Reading message by id: {}".format(message_id))
        statement = select(MessageModel).where(MessageModel.id == message_id)
        message = self.session.exec(statement).first()
        self.logger.debug("Read message by id: {}".format(message))
        return message

    def read_all(self) -> List[MessageModel]:
        self.logger.debug("Reading all messages")
        data = self.session.exec(select(MessageModel)).all()
        self.logger.debug("Read all messages")
        return list(data)

    def read_by_role(self, role_name: str) -> List[MessageModel]:
        self.logger.warning("Reading messages by role: {}".format(role_name))
        return [] # TODO: Пока не готово

    def create(self, message: MessageModel) -> bool:
        try:
            self.logger.debug("Creating new message: {}".format(message))
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)
            self.logger.debug("Created new message: {}".format(message))
            return True
        except Exception as e:
            self.logger.error("Failed to create message: {}".format(e))
            return False

    def update(self, message_id: int, message: MessageModel) -> bool:
        try:
            self.logger.debug("Updating message: {}".format(message))
            new_message = self.read_by_id(message_id)
            if (new_message is not None):
                new_message.text = message.text
                self.session.add(new_message)
                self.session.commit()
                self.session.refresh(new_message)
                self.logger.debug("Updated message: {}".format(new_message))
                return True
            return False
        except Exception as e:
            self.logger.error("Failed to update message: {}".format(e))
            return False

    def delete(self, message_id: int) -> bool:
        try:
            self.logger.debug("Deleting message: {}".format(message_id))
            message = self.read_by_id(message_id)
            if (message != None):
                self.session.delete(message)
                self.session.commit()
                self.logger.debug("Deleted message: {}".format(message))
                return True
            return False
        except Exception as e:
            self.logger.error("Failed to delete message: {}".format(e))
            return False
