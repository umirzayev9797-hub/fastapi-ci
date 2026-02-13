from typing import Any, Dict, List, Optional

from fastapi import FastAPI

from app.models import Task

app: FastAPI = FastAPI()
# ... остальной код роутов