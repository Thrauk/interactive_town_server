from abc import ABC, abstractmethod
from typing import Any

from routers.router_data import *


class TaskResolver(ABC):

    @abstractmethod
    async def initialize_agent(self, data: InitializeAgentData) -> Any:
        pass

    @abstractmethod
    async def get_daily_schedule(self, data: DailyPlanData) -> Any:
        pass

    @abstractmethod
    async def get_hourly_schedule(self, data: HourlyAgendaData) -> Any:
        pass

    @abstractmethod
    async def get_split_schedule(self, data: SplitScheduleData) -> Any:
        pass

    @abstractmethod
    async def change_location(self, data: ChangeLocationData) -> Any:
        pass

    @abstractmethod
    async def plan_today(self, data: DailyPlanData) -> Any:
        pass

    @abstractmethod
    async def get_memory_importance(self, data: MemoryImportanceData) -> Any:
        pass

    @abstractmethod
    async def add_active_memory(self, data: AddActiveMemoryData) -> Any:
        pass

    @abstractmethod
    async def retrieve_memories(self, data: RetrieveMemoriesData) -> Any:
        pass

    @abstractmethod
    async def execute_activity(self, data: ExecuteActivityData) -> Any:
        pass

    @abstractmethod
    async def what_to_do_now(self, data: WhatToDoNowData) -> Any:
        pass

    @abstractmethod
    async def dump_memory(self, data: DumpMemoryData) -> Any:
        pass

    @abstractmethod
    async def reset_instance(self) -> Any:
        pass

    @abstractmethod
    async def observe(self, data: ObserveData) -> Any:
        pass

    @abstractmethod
    async def dump_actions(self, data: DumpMemoryData) -> Any:
        pass
