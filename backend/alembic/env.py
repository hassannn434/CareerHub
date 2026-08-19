"""
Alembic environment template for CareerHub AI.

Usage:
1. cd backend
2. pip install alembic
3. alembic init alembic
4. Replace the generated alembic/env.py with this file or merge the settings below.

Key points:
- Ensure your PYTHONPATH includes the repository root when running alembic commands, or set the SQLALCHEMY URL in alembic.ini using your DATABASE_URL.
- This template imports model metadata from backend.app.db.base
"""

from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
# for example from myapp import mymodel
# target_metadata = mymodel.Base.metadata
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.base import Base

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired: config.get_main_option("sqlalchemy.url")
# or through the config file.

def get_url():
    return os.environ.get('DATABASE_URL') or config.get_main_option('sqlalchemy.url')

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
