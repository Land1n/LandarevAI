from app.repositories.base.generic import abstractmethod,GenericRepository

from app.models.role import RoleModel

from typing import List,Optional

class RoleRepository(GenericRepository[RoleModel]):
    @abstractmethod
    def read_by_name(self, role_name:str) -> Optional[RoleModel]:
        pass

    def _model_class(self) -> type:
        return RoleModel