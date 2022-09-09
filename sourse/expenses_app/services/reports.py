import csv
from io import StringIO
from fastapi import Depends
from typing import Any

from .operations import OperationsService
from ..schemas.operations import (
    OperationCreate,
    Operation,
)


class ReportsService:
    report_fields = [
        'date',
        'kind',
        'amount',
        'description',
    ]


    def __init__(self, operation_service: OperationsService = Depends()):
        self.operation_service = operation_service

    def import_csv(self, user_id: int, file: Any):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=self.report_fields)
        next(reader, None)
        operations = []
        for row in reader:
            operation_data = OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations.append(operation_data)

        self.operation_service.create_many(
            user_id,
            operations,
        )

    def export_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=self.report_fields,
            extrasaction='ignore',
        )

        operations = self.operation_service.get_list(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = Operation.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)
        return output
