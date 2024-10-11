from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/student_reports"
    LOGSTASH_HOST: str = "logstash"
    LOGSTASH_PORT: int = 5000
    ELASTICSEARCH_HOST: str = "elasticsearch"

    class Config:
        env_file = ".env"

settings = Settings()