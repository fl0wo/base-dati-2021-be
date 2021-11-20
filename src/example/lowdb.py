
import sqlalchemy
from . import config

from sqlalchemy import (
    create_engine, Column, Integer, String, Numeric,
    CheckConstraint, UniqueConstraint, ForeignKeyConstraint,
    Table, Column, Integer, String, DDL
)

engine = sqlalchemy.create_engine(config.DATABASE_CONNECTION_URI)


def create_schema(schema_name):
    engine.execute(DDL("CREATE SCHEMA IF NOT EXISTS " + schema_name))


def create_trigger():
    engine.execute(DDL("CREATE SCHEMA IF NOT EXISTS " + schema_name))

