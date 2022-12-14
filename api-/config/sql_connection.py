import sqlalchemy as alch
import os
from dotenv import load_dotenv

load_dotenv()

dbName = "twin_peaks"
password=os.getenv("SQL")


connectionData = f"mysql+pymysql://root:{password}@localhost/{dbName}"
engine = alch.create_engine(connectionData)