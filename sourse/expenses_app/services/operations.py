from fastapi import (
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session
from typing import (
    Optional,
    List,
)

from ..database import get_session
from .. import models
from ..schemas.operations import (
    OperationKind,
    OperationCreate,
    OperationUpdate,
)


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, id_user: int, operation_id: int):
        operation = (
            self.session
            .query(models.Operation)
            .filter_by(
                id=operation_id,
                user_id=id_user,
            )
            .first())
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, user_id: int, kind: Optional[OperationKind] = None):
        query = (
            self.session
            .query(models.Operation)
            .filter_by(user_id=user_id)
        )
        if kind:
            query = query.filter_by(kind=kind)
        operations = query.all()
        return operations

    def get(self, user_id: int, operation_id: int):
        return self._get(user_id, operation_id)

    def create_many(self, user_id: int, operations_data: List[OperationCreate]) -> List[models.Operation]:
        operations = [
            models.Operation(
                **operation_data.dict(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()
        return operations


    def create(self, user_id: int, operation_data: OperationCreate):
        operation = models.Operation(
            **operation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, user_id: int, operation_id: int,  operation_data: OperationUpdate):
        operation = self._get(user_id, operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(self, user_id: int, operation_id: int):
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()



