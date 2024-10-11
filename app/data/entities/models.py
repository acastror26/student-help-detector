from sqlalchemy import Column, Integer, String, Date, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class StudentReport(Base):
    __tablename__ = "student_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, nullable=False)
    start_date_period = Column(Date, nullable=False)
    end_date_period = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    attendance_rate = Column(Float, nullable=False)
    study_hours_per_week = Column(Float, nullable=False)
    previous_grade = Column(Float, nullable=False)
    extracurricular_activities_count = Column(Integer, nullable=False)
    parental_support = Column(Integer, nullable=False)
    final_grade = Column(Float, nullable=True)
    prediction_final_grade = Column(Float, nullable=True)
    prediction_report_date = Column(Date, nullable=True)
