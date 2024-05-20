from pydantic import BaseModel
from typing import List


class ActionModel(BaseModel):
    action: str
    duration: int


class TaskModel(BaseModel):
    location: str
    task: str
    # reason:str
    actions: List[ActionModel]


class Tasks(BaseModel):
    target:str
    tasks: List[TaskModel]
