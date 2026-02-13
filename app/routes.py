from typing import Any, Dict, List, Optional

from fastapi import FastAPI

from app.models import Task

app: FastAPI = FastAPI()

# Имитация базы данных
tasks_db: List[Task] = [
    Task(id_num=1, title="Изучить CI/CD", description="Настроить пайплайны")
]


@app.get("/tasks", response_model=List[Dict[str, Any]])
async def get_tasks() -> List[Dict[str, Any]]:
    """Возвращает список всех задач."""
    return [task.to_dict() for task in tasks_db]


@app.post("/tasks")
async def create_task(title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Создает новую задачу."""
    new_id: int = len(tasks_db) + 1
    new_task: Task = Task(id_num=new_id, title=title, description=description)
    tasks_db.append(new_task)
    return new_task.to_dict()
