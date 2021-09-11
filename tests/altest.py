# from app.config import settings
# import pytest
from alembic import command
from alembic.config import Config

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password123@localhost:5432/fastapi_test'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


alembic_cfg = Config('alembic.ini')
# alembic_cfg.set_main_option('script_location', 'alembic.ini')
alembic_cfg.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

command.upgrade(alembic_cfg, "head")
