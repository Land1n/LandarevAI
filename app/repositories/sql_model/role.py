from app.repositories.base.role import RoleRepository,RoleModel

from sqlmodel import Session,select

from typing import List,Optional

class SqlModelRoleRepository(RoleRepository):
    def __init__(self, session:Session ):
        self.session = session

    def read_roles_all(self) -> List[RoleModel]:
        return list(self.session.exec(select(RoleModel)).all())

    def create_role(self, role: RoleModel) -> bool:
        try:
            self.session.add(role)
            self.session.commit()
            self.session.refresh(role)
            return True
        except Exception as e:
            return False

    def read_role_by_id(self, role_id: int) -> Optional[RoleModel]:
        statement = select(RoleModel).where(RoleModel.id == role_id)
        role = self.session.exec(statement).first()
        return role

    def read_role_by_name(self, role_name:str) -> Optional[RoleModel]:
        statement = select(RoleModel).where(RoleModel.name == role_name)
        role = self.session.exec(statement).first()
        return role

    def update_role(self, role_id: int, role: RoleModel) -> bool:
        try:
            existing = self.read_role_by_id(role_id)
            if not existing:
                return False
            existing.name = role.name
            self.session.add(existing)
            self.session.commit()
            self.session.refresh(existing)
            return True
        except Exception as e:
            return False

    def delete_role(self, role_id:int) -> bool:
        try:
            role = self.read_role_by_id(role_id)
            if (role != None):
                self.session.delete(role)
                self.session.commit()
                return True
            return False
        except Exception as e:
            return False