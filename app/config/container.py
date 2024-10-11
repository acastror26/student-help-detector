from dependency_injector import containers, providers
from app.data.repositories.student_report_repository import StudentReportRepository
from app.core.student_report_service import StudentReportService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.api.endpoints"])

    db_engine = providers.Singleton(
        create_engine,
        settings.DATABASE_URL
    )

    db_session = providers.Singleton(
        sessionmaker,
        bind=db_engine
    )

    student_report_repository = providers.Factory(
        StudentReportRepository,
        session=db_session
    )

    student_report_service = providers.Factory(
        StudentReportService,
        repository=student_report_repository
    )