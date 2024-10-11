import csv
from io import StringIO

class StudentReportService:
    def __init__(self, repository):
        self.repository = repository

    def process_csv(self, csv_data, start_date_period, end_date_period):
        # Logic to process the CSV and upsert the reports
        csv_reader = csv.DictReader(StringIO(csv_data.decode('utf-8')))
        for row in csv_reader:
            student_report_data = {
                "user_id": row["user_id"],
                "start_date_period": start_date_period,
                "end_date_period": end_date_period,
                "gender": row["gender"],
                "attendance_rate": float(row["attendance_rate"]),
                "study_hours_per_week": float(row["study_hours_per_week"]),
                "previous_grade": float(row["previous_grade"]),
                "extracurricular_activities_count": int(row["extracurricular_activities_count"]),
                "parental_support": int(row["parental_support"]),
                # Optional fields will be None if not present
                "final_grade": float(row.get("final_grade")) if row.get("final_grade") else None,
                "prediction_final_grade": float(row.get("prediction_final_grade")) if row.get("prediction_final_grade") else None,
                "prediction_report_date": row.get("prediction_report_date"),
            }
            self.repository.upsert_student_report(student_report_data)

    def get_report(self, start_date, end_date):
        reports = self.repository.get_reports_by_period(start_date, end_date)
        if not reports:
            raise ValueError("Report for the given period is not ready")
        return reports
