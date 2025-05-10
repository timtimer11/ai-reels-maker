from typing import Dict, Optional
from enum import Enum
from datetime import datetime
import uuid

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskQueue:
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
    
    def create_task(self) -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "status": TaskStatus.PENDING,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "result": None,
            "error": None
        }
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: TaskStatus, result: Optional[bytes] = None, error: Optional[str] = None):
        if task_id in self.tasks:
            self.tasks[task_id].update({
                "status": status,
                "updated_at": datetime.now(),
                "result": result,
                "error": error
            })

# Global task queue instance
task_queue = TaskQueue()