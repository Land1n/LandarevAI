from app.repositories.base.role import RoleRepository, RoleModel
from app.core.logger.logger import logger, convert_result
from app.core.logger.schemas.answer import Answer
from typing import Optional, List
import logging


class RoleService:
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    @convert_result
    @logger("RoleService")
    def read_role_by_id(self, id: int) -> Optional[RoleModel]:
        try:
            role = self.repository.read_by_id(id)
            if role:
                return Answer[RoleModel](result=role, level=logging.INFO)
            return Answer[RoleModel](result=None, level=logging.WARNING, description=f"Role with id={id} not found")
        except Exception as e:
            return Answer[RoleModel](result=None, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("RoleService")
    def read_role_by_name(self, name: str) -> Optional[RoleModel]:
        try:
            role = self.repository.read_by_name(name)
            if role:
                return Answer[RoleModel](result=role, level=logging.INFO)
            return Answer[RoleModel](result=None, level=logging.WARNING, description=f"Role with name='{name}' not found")
        except Exception as e:
            return Answer[RoleModel](result=None, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("RoleService")
    def list_roles(self) -> List[RoleModel]:
        try:
            roles = self.repository.read_all()
            return Answer[RoleModel](result=roles, level=logging.INFO)
        except Exception as e:
            return Answer[RoleModel](result=[], level=logging.ERROR, description=str(e))

    @convert_result
    @logger("RoleService")
    def create_role(self, role: RoleModel) -> bool:
        try:
            existing = self.repository.read_by_name(role.name)
            if existing is not None:
                return Answer[RoleModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Role with name '{role.name}' already exists"
                )
            is_created = self.repository.create(role)
            return Answer[RoleModel](result=is_created, level=logging.INFO)
        except Exception as e:
            return Answer[RoleModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("RoleService")
    def update_role(self, id: int, role: RoleModel) -> bool:
        try:
            old_role = self.repository.read_by_id(id)
            if old_role is None:
                return Answer[RoleModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Role with id={id} not found"
                )
            if old_role.name != role.name:
                existing = self.repository.read_by_name(role.name)
                if existing is not None and existing.id != id:
                    return Answer[RoleModel](
                        result=False,
                        level=logging.ERROR,
                        description=f"Another role with name '{role.name}' already exists"
                    )
            is_updated = self.repository.update(id, role)
            if not is_updated:
                return Answer[RoleModel](result=is_updated, level=logging.WARNING, description=f"Update returned False")
            return Answer[RoleModel](result=is_updated, level=logging.INFO)
        except Exception as e:
            return Answer[RoleModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("RoleService")
    def delete_role(self, id: int) -> bool:
        try:
            # Проверяем, существует ли роль
            old_role = self.repository.read_by_id(id)
            if old_role is None:
                return Answer[RoleModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Role with id={id} not found"
                )
            is_deleted = self.repository.delete(id)
            if not is_deleted:
                return Answer[RoleModel](result=is_deleted, level=logging.WARNING, description=f"Delete returned False")
            return Answer[RoleModel](result=is_deleted, level=logging.INFO)
        except Exception as e:
            return Answer[RoleModel](result=False, level=logging.ERROR, description=str(e))