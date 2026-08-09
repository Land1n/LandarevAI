from abc import ABC,abstractmethod
from typing import List,Optional

from app.models.role import RoleModel

class RoleRepository(ABC):

    @abstractmethod
    def read_roles_all(self) -> List[RoleModel]:
        pass
    @abstractmethod
    def create_role(self, role: RoleModel) -> bool:
        pass
    @abstractmethod
    def read_role_by_id(self, role_id: int) -> Optional[RoleModel]:
        pass
    @abstractmethod
    def read_role_by_name(self, role_name:str) -> Optional[RoleModel]:
        pass
    @abstractmethod
    def update_role(self, role_id:int ,role: RoleModel) -> bool:
        pass
    @abstractmethod
    def delete_role(self, role_id:int) -> bool:
        pass