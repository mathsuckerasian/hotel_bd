from sqlmodel import create_engine

DATABASE_URL = "postgresql+psycopg2://student:mis2025!@176.108.247.125:5432/mis2025"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"options": "-csearch_path=LiSasha"}  
)
