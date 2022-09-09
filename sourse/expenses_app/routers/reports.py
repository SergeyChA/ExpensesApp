from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    UploadFile,
    Depends
)
from fastapi.responses import StreamingResponse

from ..schemas.auth import User
from ..services.auth import get_current_user
from ..services.reports import ReportsService

router = APIRouter(
    prefix='/report',
    tags=['import_export_csv'],
)


@router.post('/import')
def import_csv(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        user: User = Depends(get_current_user),
        report_service: ReportsService = Depends(),
):
    background_tasks.add_task(
            report_service.import_csv,
            user.id,
            file.file,
    )



@router.post('/export')
def export_csv(
        user: User = Depends(get_current_user),
        report_service: ReportsService = Depends(),
):
    report = report_service.export_csv(user.id)
    return StreamingResponse(
        report,
        media_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=report.csv'
        },
    )