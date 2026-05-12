from app.database.db import engine
from app.database.db import Base

from app.models.invoice import Invoice

Base.metadata.create_all(bind=engine)

print("DATABASE TABLES CREATED")