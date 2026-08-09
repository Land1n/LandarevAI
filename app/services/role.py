from app.repositories.base.role import RoleRepository,RoleModel

from typing import Optional,List

class RoleService:
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    def read_role_by_id(self, role_id: int) -> Optional[RoleModel]:
        return self.repository.read_role_by_id(role_id)

    def create_role(self, role: RoleModel) -> bool:
        return self.repository.create_role(role)

    def update_role(self, role_id:int ,role: RoleModel) -> bool:
        return self.repository.update_role(role=role,role_id=role_id)

    def delete_role(self, role_id: int) -> bool:
        return self.repository.delete_role(role_id=role_id)

    def list_roles(self) -> List[RoleModel]:
        return self.repository.read_roles_all()
