from fastapi import APIRouter
from open_ai_api import *
from routers.router_data import *
from app_config import AppProcessor

processor = AppProcessor

router = APIRouter(
    tags=["agent"],
    prefix="/agent",
)


@router.post("/daily_schedule")
async def daily_schedule(data: DailyPlanData):
    return await processor.get_daily_schedule(data)


@router.post("/hourly_schedule")
async def hourly_schedule(data: HourlyAgendaData):
    return await processor.get_hourly_schedule(data)


@router.post("/split_schedule")
async def split_schedule(data: SplitScheduleData):
    return await processor.get_split_schedule(data)


@router.post("/change_location")
async def change_location(data: ChangeLocationData):
    return await processor.change_location(data)


@router.post("/initialize_agent")
async def initialize_agent(data: InitializeAgentData):
    return await processor.initialize_agent(data)


@router.post("/plan_today")
async def plan_today(data: DailyPlanData):
    return await processor.plan_today(data)


@router.post("/memory_importance")
async def memory_importance(data: MemoryImportanceData):
    return await processor.get_memory_importance(data)


@router.post("/add_active_memory")
async def add_active_memory(data: AddActiveMemoryData):
    return await processor.add_active_memory(data)


@router.post("/retrieve_memories")
async def retrieve_memories(data: RetrieveMemoriesData):
    return await processor.retrieve_memories(data)


@router.post("/execute_activity")
async def execute_activity(data: ExecuteActivityData):
    return await processor.execute_activity(data)


@router.post("/what_to_do_now")
async def what_to_do_now(data: WhatToDoNowData):
    return await processor.what_to_do_now(data)


@router.post("/dump_memory")
async def dump_memory(data: DumpMemoryData):
    return await processor.dump_memory(data)


@router.post("/reset_instance")
async def reset_instance():
    return await processor.reset_instance()


@router.post("/observe")
async def reset_instance(data: ObserveData):
    return await processor.observe(data)

@router.post("/dump_actions")
async def dump_actions(data: DumpMemoryData):
    return await processor.dump_actions(data)

