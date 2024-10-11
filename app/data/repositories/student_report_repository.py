from app.data.entities.models import StudentReport

class StudentReportRepository:
    def __init__(self, session):
        self.session = session()

    def upsert_student_report(self, student_report_data):
        # Check if the report exists in the DB and either insert or update
        report = (self.session.query(StudentReport)
                  .filter_by(user_id=student_report_data['user_id'], 
                             start_date_period=student_report_data['start_date_period'], 
                             end_date_period=student_report_data['end_date_period'])
                  .first())
        if report:
            for key, value in student_report_data.items():
                setattr(report, key, value)
        else:
            report = StudentReport(**student_report_data)
            self.session.add(report)
        self.session.commit()

    def get_reports_by_period(self, start_date, end_date):
        return (self.session.query(StudentReport)
                .filter(StudentReport.start_date_period == start_date)
                .filter(StudentReport.end_date_period == end_date)
                .filter(StudentReport.prediction_final_grade != None)
                .filter(StudentReport.final_grade == None)
                .all())
