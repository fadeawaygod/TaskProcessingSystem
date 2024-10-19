"""
This base is for the connections between all tables.

All tables includes this base to create table.
"""

from sqlalchemy.orm import declarative_base

# to use uuid_generate_v4, you must install the extension first:
# CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
Base = declarative_base()
