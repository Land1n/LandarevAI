from app.repositories.base.message import MessageRepository,MessageModel

from sqlalchemy

class SqlAlchemyMessageRepository(MessageRepository):
    def __init__(self, session):
        self.session = session

