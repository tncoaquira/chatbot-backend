import os
from dotenv import load_dotenv


class Config:
    load_dotenv()

    PG_RECORD_MANAGER= f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@" \
                 f"{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME_PROYECTO")}"
