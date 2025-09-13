from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

# Create metadata object
metadata = MetaData()

# Create Base class with metadata
Base = declarative_base(metadata=metadata)