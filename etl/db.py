from sqlalchemy import create_engine

DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "marketdb"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)