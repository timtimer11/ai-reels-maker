from typing import Dict, Optional
from enum import Enum
from datetime import datetime
import uuid

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    FETCHING_REDDIT_POST = "fetching_reddit_post"
    GENERATING_SCRIPT = "generating_script"
    GENERATING_VOICEOVER = "generating_voiceover"
    FETCHING_BACKGROUND_VIDEO = "fetching_background_video"
    PROCESSING_VIDEO = "processing_video"
    GETTING_VIDEO_URL = "getting_video_url"

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
            "error": None,
            "video_url": None
        }
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: TaskStatus, result: Optional[bytes] = None, error: Optional[str] = None, video_url: Optional[str] = None):
        if task_id in self.tasks:
            print(f"Updating task {task_id} status to: {status.value}")
            self.tasks[task_id].update({
                "status": status,
                "updated_at": datetime.now(),
                "result": result,
                "error": error,
                "video_url": video_url
            })
            print(f"Updated task data: {self.tasks[task_id]}")

# Global task queue instance
task_queue = TaskQueue()