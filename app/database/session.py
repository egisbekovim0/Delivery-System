from sqlalchemy import create_engine

create_engine(
    url ="sqlite:///sqlite.db",
    echo=True
)