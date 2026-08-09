from abc import ABC,abstractmethod
from typing import List

from app.models.role import RoleModel

class RoleRepository(ABC):

    @abstractmethod
    def add_role(self, role: RoleModel):
        pass
    @abstractmethod
    def update_role(self, role_id:int ,role: RoleModel):
        pass
    @abstractmethod
    def delete_role(self, role_id:int, role: RoleModel):
        pass
    @abstractmethod
    def get_all_roles(self) -> List[RoleModel]:
        pass
    @abstractmethod
    def get_role_by_id(self, role_id: int) -> RoleModel:
        pass