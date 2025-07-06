from datetime import datetime
import uuid
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskQueue:
    def __init__(self):
        self.tasks = {}

    def create_media_processing_task(self) -> str:
        task_id = str(uuid.uuid4()) + "_" + str(datetime.now().timestamp())
        self.tasks[task_id] = {
            "status": TaskStatus.PENDING,
            "video_url": None,
            "error": None
        }
        return task_id

    def update_task_status(self, task_id: str, status: TaskStatus, video_url: str = None, error: str = None):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            if status == TaskStatus.COMPLETED:
                self.tasks[task_id]["video_url"] = video_url
            if status == TaskStatus.FAILED and error:
                self.tasks[task_id]["error"] = error

    def get_task_status(self, task_id: str) -> dict:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            return {
                "status": task["status"].value, 
                "video_url": task["video_url"],
                "error": task.get("error")
            }
        return {"status": "not_found"}

# Global task queue instance
task_queue = TaskQueue()