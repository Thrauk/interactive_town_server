import ast
import json
from abc import ABC

from agent import AgentManager
from open_ai_api import HourlyAgenda
from open_ai_api.api_requests.actions.do_something import DoSomething
from open_ai_api.api_requests.actions.execute_activity import ExecuteActivity
from open_ai_api.api_requests.memory.memory_importance import MemoryImportance
from open_ai_api.api_requests.recursive_hour import RecursiveHour
from open_ai_api.api_requests.relevant_memory_summary import RelevantMemorySummary
from resolver.output.gpt_output_formatter import GptOutputFormatter
from task_resolver import TaskResolver
from open_ai_api import *
from routers.router_data import *
from typing import Any


def string_to_list(string_input):
    try:
        # Convert the string to a list using ast.literal_eval
        return ast.literal_eval(string_input)
    except ValueError as e:
        # Handle the case where the string is not a valid Python literal
        print(f"Error converting string to list: {e}")
        return None
    except SyntaxError as e:
        # Handle syntax error which could occur with malformed strings
        print(f"Syntax error: {e}")
        return None


async def retrieve_relevant_mem(agent, data, query):
    mem = await agent.memory_storage.retrieve_relevant_memories_str(
        context=query,
        seconds_from_start=data.time_data.seconds_from_start,
        min_score=0.5,
    )

    mem_str = '' if len(mem) == 0 else '\n'.join(mem)

    summary = await RelevantMemorySummary.request(
        agent_name=agent.name,
        agent_summary=agent.summary,
        relevant_memories=mem_str,
        world_nodes=agent.world_nodes,
        query=query
    )

    print(f'Relevant memory summary: {summary}')
    return summary


class GptTaskResolver(TaskResolver, ABC):
    async def get_daily_schedule(self, data: DailyPlanData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)
        memories_str = await retrieve_relevant_mem(
            agent=agent,
            data=data,
            query=f'What is {agent.name} planning today? What are the things to look forward to?',
        )

        if agent is None:
            raise ValueError(f"Invalid agent {data.agent_id}")
        plan = await DailyAgenda.request(
            agent_name=agent.name,
            agent_summary=agent.summary,
            agent_wake_up_hour=agent.wake_up_hour,
            world_nodes=agent.world_nodes,
            relevant_memories=memories_str
        )

        mem_data = AddAnyMemoryData(
            agent_id=data.agent_id,
            memory=f'{agent.name} plan for today is: {plan}',
            time_data=data.time_data
        )

        await self.add_any_memory(mem_data)

        return plan

    async def initialize_agent(self, data: InitializeAgentData) -> None:
        AgentManager().initialize_agent(
            data=data
        )
        # daily_data = DailyPlanData(
        #     agent_id=data.agent_id,
        #     time_data=data.time_data
        # )
        # await self.get_daily_schedule(data=daily_data)
        return

    async def what_to_do_now(self, data: WhatToDoNowData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)

        if agent.current_plan.get('hour') is None or agent.current_plan.get('hour') != data.time_data.current_hour:
            time_data = data.time_data
            hourly_mem = await retrieve_relevant_mem(
                agent=agent,
                data=data,
                # query=f'It is{time_data.current_hour}:{time_data.current_minute}.'
                #       f'What actions is {agent.name} looking forward to do for the next hour, taking into account previous '
                #       f'actions,'
                #       f'plans and interactions?',
                query=f'What is {agent.name} looking to do next, taking into account previous actions and plans?'
            )

            plan = await RecursiveHour.request(
                agent_name=agent.name,
                agent_summary=agent.summary,
                day_number=data.time_data.day_number,
                current_hour=data.time_data.current_hour,
                world_nodes=agent.world_nodes,
                relevant_memories=hourly_mem,
                agent_wake_up_hour=agent.wake_up_hour,
                recent_actions=str(agent.action_history)
            )

            actions_str = await SplitSchedule.request(
                action_description=plan,
                agent_name=agent.name,
                agent_summary=agent.summary,
                world_nodes=agent.world_nodes,
            )

            print(f'Plan: {plan}')
            print(f'Actions: {actions_str}')

            actions_list = string_to_list(actions_str)

            agent.current_plan['hour'] = data.time_data.current_hour
            agent.current_plan['plan'] = plan
            agent.current_plan['actions'] = actions_list

        total_min = 0
        current_minute = data.time_data.current_minute
        current_hour = data.time_data.current_hour
        for action in agent.current_plan['actions']:

            total_min += action[1]
            if current_minute < total_min:
                action_desc = action[0]
                period = total_min - current_minute

                final_hour = current_hour if total_min < 60 else current_hour + 1
                final_minute = total_min if total_min < 60 else 0

                await self.insert_memory(
                    data=data,
                    memory=f'{action_desc}',
                )

                # agent.action_history.insert(0, action_desc)
                agent.action_history.append(action_desc)

                res = await DoSomething.request(
                    action=action_desc,
                    agent_name=agent.name,
                    agent_summary=agent.summary,
                    world_nodes=agent.world_nodes,
                    current_location=data.current_location,
                    duration=period,
                )

                print(res)

                return json.loads(res)

        return {
            'action': 'empty',
            'minutes': 0,
            'action_type': 'move_to'
        }

    async def insert_memory(self, data, memory):
        mem_data = AddAnyMemoryData(
            agent_id=data.agent_id,
            memory=memory,
            time_data=data.time_data
        )
        await self.add_any_memory(mem_data)

    async def get_hourly_schedule(self, data: HourlyAgendaData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)
        if agent is None:
            raise ValueError(f"Invalid agent {data.agent_id}")
        response = await HourlyAgenda.request(
            daily_agenda=data.daily_agenda,
            agent_name=agent.name,
            agent_summary=agent.summary,
            world_nodes=agent.world_nodes,
        )
        return string_to_list(response)

    async def get_split_schedule(self, data: SplitScheduleData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)
        if agent is None:
            raise ValueError(f"Invalid agent {data.agent_id}")
        return await SplitSchedule.request(
            action_description=data.action_description,
            agent_name=agent.name,
            agent_summary=agent.summary,
            world_nodes=agent.world_nodes,
        )

    async def change_location(self, data: ChangeLocationData) -> Any:
        AgentManager().update_location(
            agent_id=data.agent_id,
            new_location=data.new_location,
        )

    async def plan_today(self, data: DailyPlanData) -> Any:
        daily_schedule_response = await self.get_daily_schedule(
            data=data
        )
        hourly_data = HourlyAgendaData(
            agent_id=data.agent_id,
            daily_agenda=daily_schedule_response
        )
        hourly_schedule_list = (await self.get_hourly_schedule(data=hourly_data))
        sorted_list = sorted(hourly_schedule_list, key=lambda x: x[1])

        return GptOutputFormatter.plan_today_format(sorted_list)

    async def get_memory_importance(self, data: MemoryImportanceData) -> int:
        importance = await MemoryImportance.request(
            memory=data.memory
        )
        return int(importance)

    async def add_active_memory(self, data: AddActiveMemoryData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)

        importance_data = MemoryImportanceData(
            memory=data.memory
        )

        importance = await self.get_memory_importance(importance_data)

        await agent.memory_storage.add_memory(
            description=data.memory,
            importance=importance,
            seconds_since_game_started=data.seconds_from_start,
        )

        return True

    async def add_any_memory(self, data: AddAnyMemoryData) -> Any:
        time_data = data.time_data
        # combined_mem = f'Day {time_data.day_number}, Time: {time_data.current_hour}:{time_data.current_minute} -> {data.memory}'
        combined_mem = f'{data.memory}'

        mem_data = AddActiveMemoryData(
            agent_id=data.agent_id,
            memory=combined_mem,
            seconds_from_start=time_data.seconds_from_start
        )

        await self.add_active_memory(data=mem_data)

    async def retrieve_memories(self, data: RetrieveMemoriesData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)

        return await agent.memory_storage.retrieve_relevant_memories_debug(
            context=data.query,
            seconds_from_start=data.seconds_from_start,
        )

    async def execute_activity(self, data: ExecuteActivityData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)

        tool_calls = await ExecuteActivity.request(
            action=data.action,
            agent_name=agent.name,
            agent_summary=agent.summary,
            world_nodes=agent.world_nodes,
            current_location=data.current_location,
            duration=data.duration,
            action_type=data.action_type,
        )

        return {'functions': tool_calls}

    async def dump_memory(self, data: DumpMemoryData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)

        ret = []

        memories = agent.memory_storage.memories

        for memory in memories:
            ret.append(memory.description)
        return ret

    async def reset_instance(self) -> Any:
        AgentManager().reset_instance()

    async def observe(self, data: ObserveData) -> Any:
        await self.insert_memory(
            data=data,
            memory=f'{data.observed_entity} {data.observation}',
        )

    async def dump_actions(self, data: DumpMemoryData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)

        return agent.action_history
