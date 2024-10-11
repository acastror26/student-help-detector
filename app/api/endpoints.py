from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.core.student_report_service import StudentReportService
from dependency_injector.wiring import inject, Provide
from app.config.container import Container
from fastapi.responses import StreamingResponse
import io
import csv

router = APIRouter()

@router.post("/update-csv")
@inject
def update_csv(
    start_date_period: str,
    end_date_period: str,
    file: UploadFile = File(...),
    service: StudentReportService = Depends(Provide[Container.student_report_service])
):
    try:
        service.process_csv(file.file.read(), start_date_period, end_date_period)
        return {"message": "CSV processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get-report")
@inject
def get_report(
    start_date_period: str,
    end_date_period: str,
    service: StudentReportService = Depends(Provide[Container.student_report_service])
):
    try:
        reports = service.get_report(start_date_period, end_date_period)
        output = io.StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerow([
            "user_id", "start_date_period", "end_date_period", "gender", 
            "attendance_rate", "study_hours_per_week", "previous_grade", 
            "extracurricular_activities_count", "parental_support", 
            "final_grade", "prediction_final_grade", "prediction_report_date"
        ])
        for report in reports:
            csv_writer.writerow([
                report.user_id, report.start_date_period, report.end_date_period, report.gender,
                report.attendance_rate, report.study_hours_per_week, report.previous_grade,
                report.extracurricular_activities_count, report.parental_support,
                report.final_grade, report.prediction_final_grade, report.prediction_report_date
            ])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
