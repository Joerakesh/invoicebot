from app.database.db import engine
from app.database.db import Base

from app.models.invoice import Invoice


print("CREATING TABLES...")

Base.metadata.create_all(bind=engine)

print("DATABASE READY")