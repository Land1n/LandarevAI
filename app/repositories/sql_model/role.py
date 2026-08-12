from app.repositories.base.role import RoleRepository,RoleModel

from sqlmodel import Session,select

from typing import List,Optional

import logging

class SqlModelRoleRepository(RoleRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, session:Session ):
        self.session = session

    def read_roles_all(self) -> List[RoleModel]:
        self.logger.debug("Reading all roles")
        data = self.session.exec(select(RoleModel)).all()
        self.logger.debug("Read all roles")
        return data

    def create_role(self, role: RoleModel) -> bool:
        try:
            self.logger.debug("Creating new role: {}".format(role))
            self.session.add(role)
            self.session.commit()
            self.session.refresh(role)
            self.logger.debug("Created new role: {}".format(role))
            return True
        except Exception as e:
            self.logger.error("Failed to create new role: {}".format(e))
            return False

    def read_role_by_id(self, role_id: int) -> Optional[RoleModel]:
        self.logger.debug("Reading role by id: {}".format(role_id))
        statement = select(RoleModel).where(RoleModel.id == role_id)
        role = self.session.exec(statement).first()
        self.logger.debug("Read role by id: {}".format(role))
        return role

    def read_role_by_name(self, role_name:str) -> Optional[RoleModel]:
        self.logger.debug("Reading role by name: {}".format(role_name))
        statement = select(RoleModel).where(RoleModel.name == role_name)
        role = self.session.exec(statement).first()
        self.logger.debug("Read role by name: {}".format(role))
        return role

    def update_role(self, role_id: int, role: RoleModel) -> bool:
        try:
            self.logger.debug("Updating role: {}".format(role))
            existing = self.read_role_by_id(role_id)
            if not existing:
                self.logger.error("Failed to update role: {}".format(role))
                return False
            existing.name = role.name
            self.session.add(existing)
            self.session.commit()
            self.session.refresh(existing)
            self.logger.debug("Updated role: {}".format(role))
            return True
        except Exception as e:
            self.logger.error("Failed to update role: {}".format(e))
            return False

    def delete_role(self, role_id:int) -> bool:
        try:
            self.logger.debug("Deleting role: {}".format(role))
            role = self.read_role_by_id(role_id)
            if (role != None):
                self.session.delete(role)
                self.session.commit()
                self.logger.debug("Deleted role: {}".format(role))
                return True
            self.logger.debug("Failed to delete role: {}".format(role))
            return False
        except Exception as e:
            self.logger.error("Failed to delete role: {}".format(e))
            return False