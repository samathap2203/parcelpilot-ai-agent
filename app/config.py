import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-4.1-mini",
)

APP_NAME = "ParcelPilot AI Support Agent"

SNAPSHOT_TIME = "2026-08-16 11:00 Asia/Kolkata"