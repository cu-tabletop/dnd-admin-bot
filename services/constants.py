import os

DEFAULT_ICON_ID = os.getenv("DEFAULT_ICON_ID")
BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    raise Exception("no BACKEND_URL provided")
