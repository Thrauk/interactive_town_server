from pydantic import BaseModel
from routers.default_data import *


class TimeData(BaseModel):
    current_hour: int = DEFAULT_CURRENT_HOUR
    current_minute: int = DEFAULT_CURRENT_MINUTE
    seconds_from_start: int = DEFAULT_SECONDS_FROM_START
    day_number: int = DEFAULT_DAY_NUMBER


class InitializeAgentData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    agent_name: str = DEFAULT_AGENT_NAME
    agent_summary: str = DEFAULT_AGENT_SUMMARY
    agent_wake_up_hour: int = DEFAULT_AGENT_WAKE_UP_HOUR
    world_nodes: str = DEFAULT_WORLD_NODES
    current_location: str = DEFAULT_CURRENT_LOCATION
    time_data: TimeData = TimeData()


class DailyPlanData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    time_data: TimeData = TimeData()


class ChangeLocationData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    new_location: str
    time_data: TimeData = TimeData()


class HourlyAgendaData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    daily_agenda: str
    time_data: TimeData = TimeData()


class SplitScheduleData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    action_description: str
    time_data: TimeData = TimeData()


class MemoryImportanceData(BaseModel):
    memory: str = DEFAULT_MEMORY_IMPORTANCE


class AddActiveMemoryData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    memory: str = DEFAULT_MEMORY_IMPORTANCE
    seconds_from_start: int = DEFAULT_SECONDS_FROM_START


class RetrieveMemoriesData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    query: str = DEFAULT_MEMORY_IMPORTANCE
    seconds_from_start: int = DEFAULT_SECONDS_FROM_START


class ExecuteActivityData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    action: str = DEFAULT_EXECUTE_ACTION
    current_location: str = DEFAULT_CURRENT_LOCATION
    duration: int = DEFAULT_ACTIVITY_DURATION
    action_type: str = DEFAULT_ACTION_TYPE


class AddAnyMemoryData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    memory: str = DEFAULT_MEMORY_IMPORTANCE
    time_data: TimeData = TimeData()


class WhatToDoNowData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    current_location: str = DEFAULT_CURRENT_LOCATION
    time_data: TimeData = TimeData()


class DumpMemoryData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID


class ObserveData(BaseModel):
    agent_id: str = DEFAULT_AGENT_ID
    observed_entity: str = DEFAULT_OBSERVED_ENTITY
    observation: str = DEFAULT_OBSERVATION
    time_data: TimeData = TimeData()
