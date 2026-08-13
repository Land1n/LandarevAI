from app.repositories.base.role import RoleRepository,RoleModel

from typing import Optional,List

class RoleService:
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    def read_role_by_id(self, role_id: int) -> Optional[RoleModel]:
        return self.repository.read_by_id(role_id)

    def read_role_by_name(self, name: str) -> Optional[RoleModel]:
        return self.repository.read_by_name(name)

    def create_role(self, role: RoleModel) -> bool:
        if (self.read_role_by_name(role.name) is None):
            return self.repository.create(role)
        return False

    def update_role(self, role_id:int ,role: RoleModel) -> bool:
        return self.repository.update(role_id=role_id, role=role)

    def delete_role(self, role_id: int) -> bool:
        return self.repository.delete(role_id=role_id)

    def list_roles(self) -> List[RoleModel]:
        return self.repository.read_all()
