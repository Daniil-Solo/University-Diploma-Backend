from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

FRONTEND_HOST = os.environ.get("FRONTEND_HOST")

ELECTIVES_FILENAME = os.environ.get("ELECTIVES_DATA")
PROFESSIONS_FILENAME = os.environ.get("PROFESSIONS_DATA")
