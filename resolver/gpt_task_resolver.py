import ast
import json
from abc import ABC

from agent import AgentManager
from open_ai_api import HourlyAgenda
from open_ai_api.api_requests.actions.do_something import DoSomething, NextAction
from open_ai_api.api_requests.actions.execute_activity import ExecuteActivity
from open_ai_api.api_requests.memory.memory_importance import MemoryImportance
from open_ai_api.api_requests.recent_action_summary import RecentActionSummary
from open_ai_api.api_requests.recursive_hour import RecursiveHour
from open_ai_api.api_requests.relevant_memory_summary import RelevantMemorySummary
from open_ai_api.api_requests.smart_object_planner.planner import Planner
from resolver.output.gpt_output_formatter import GptOutputFormatter
from task_resolver import TaskResolver
from open_ai_api import *
from routers.router_data import *
from typing import Any

from tasks.tasks import TaskModel, Tasks


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
        min_score=0.01,
    )

    mem_str = '' if len(mem) == 0 else '\n'.join(mem)
    if mem_str == '':
        return mem_str

    summary = await RelevantMemorySummary.request(
        agent_name=agent.name,
        agent_summary=agent.summary,
        relevant_memories=mem_str,
        world_nodes=agent.world_nodes,
        current_time=f'{data.time_data.current_hour}:{data.time_data.current_minute}',
        query=query
    )

    print(f'Relevant memory summary: {summary}')
    return summary


async def recent_action_summary(agent, data):
    action_str = '' if len(agent.action_history) == 0 else '\n'.join(agent.action_history)

    if action_str == '':
        return action_str

    # summary = await RecentActionSummary.request(
    #     agent_name=agent.name,
    #     agent_summary=agent.summary,
    #     recent_actions=action_str,
    #     current_time=f'{data.time_data.current_hour}:{data.time_data.current_minute}',
    #     world_nodes=agent.world_nodes,
    # )

    # print(f'Recent actions summary: {summary}')

    # return summary
    return action_str


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

        # mem_data = AddAnyMemoryData(
        #     agent_id=data.agent_id,
        #     memory=f'{agent.name} daily plan for today is: {plan}.',
        #     time_data=data.time_data
        # )
        #
        # await self.add_any_memory(mem_data)

        agent.daily_schedule = plan

        return plan

    async def initialize_agent(self, data: InitializeAgentData) -> None:
        AgentManager().initialize_agent(
            data=data
        )

        await self.insert_memory(
            data=data,
            memory=f'{data.agent_name} just woke up',
        )
        # daily_data = DailyPlanData(
        #     agent_id=data.agent_id,
        #     time_data=data.time_data
        # )
        # await self.get_daily_schedule(data=daily_data)
        return

    # async def what_to_do_now(self, data: WhatToDoNowData) -> Any:
    #     agent = AgentManager().get_agent(agent_id=data.agent_id)
    #
    #     if agent.current_plan.get('hour') is None or agent.current_plan.get('hour') != data.time_data.current_hour:
    #         time_data = data.time_data
    #         hourly_mem = await retrieve_relevant_mem(
    #             agent=agent,
    #             data=data,
    #             # query=f'It is{time_data.current_hour}:{time_data.current_minute}.'
    #             #       f'What actions is {agent.name} looking forward to do for the next hour, taking into account previous '
    #             #       f'actions,'
    #             #       f'plans and interactions?',
    #             query=f'What is {agent.name} looking to do next, taking into account previous actions and plans?'
    #         )
    #
    #         plan = await RecursiveHour.request(
    #             agent_name=agent.name,
    #             agent_summary=agent.summary,
    #             day_number=data.time_data.day_number,
    #             current_hour=data.time_data.current_hour,
    #             world_nodes=agent.world_nodes,
    #             relevant_memories=hourly_mem,
    #             agent_wake_up_hour=agent.wake_up_hour,
    #             recent_actions=str(agent.action_history)
    #         )
    #
    #         await self.insert_memory(
    #             data=data,
    #             memory=plan,
    #         )
    #
    #     # actions_str = await SplitSchedule.request(
    #     #     action_description=plan,
    #     #     agent_name=agent.name,
    #     #     agent_summary=agent.summary,
    #     #     world_nodes=agent.world_nodes,
    #     # )
    #
    #     relevant_mem = await retrieve_relevant_mem(
    #         agent=agent,
    #         data=data,
    #         query=f'What is {agent.name} looking to do next, taking into account previous actions and plans?'
    #     )
    #
    #     next_action = await NextAction.request(
    #         agent_name=agent.name,
    #         agent_summary=agent.summary,
    #         world_nodes=agent.world_nodes,
    #         current_location=data.current_location,
    #         relevant_mem=relevant_mem,
    #         past_actions=str(agent.action_history),
    #     )
    #
    #     await self.insert_memory(
    #         data=data,
    #         memory=next_action,
    #     )
    #
    #     print(f'Plan: {next_action}')
    #
    #     # relevant_mem = await retrieve_relevant_mem(
    #     #     agent=agent,
    #     #     data=data,
    #     #     query=next_action
    #     # )
    #
    #     res = await DoSomething.request(
    #         action=next_action,
    #         agent_name=agent.name,
    #         agent_summary=agent.summary,
    #         world_nodes=agent.world_nodes,
    #         current_location=data.current_location,
    #         # relevant_mem=relevant_mem,
    #         past_actions=str(agent.action_history),
    #     )
    #
    #     dct = json.loads(res)
    #
    #     agent.action_history.append(dct['action'])
    #
    #     return dct
    #
    #     # print(f'Actions: {actions_str}')
    #
    #     # actions_list = string_to_list(actions_str)
    #
    #     # agent.current_plan['hour'] = data.time_data.current_hour
    #     # agent.current_plan['plan'] = plan
    #     # agent.current_plan['actions'] = actions_list
    #
    #     # total_min = 0
    #     # current_minute = data.time_data.current_minute
    #     # current_hour = data.time_data.current_hour
    #     # for action in agent.current_plan['actions']:
    #     #
    #     #     total_min += action[1]
    #     #     if current_minute < total_min:
    #     #         action_desc = action[0]
    #     #         period = total_min - current_minute
    #     #
    #     #         final_hour = current_hour if total_min < 60 else current_hour + 1
    #     #         final_minute = total_min if total_min < 60 else 0
    #     #
    #     #         await self.insert_memory(
    #     #             data=data,
    #     #             memory=f'{action_desc}',
    #     #         )
    #     #
    #     #         # agent.action_history.insert(0, action_desc)
    #     #         agent.action_history.append(action_desc)
    #     #
    #     #         res = await DoSomething.request(
    #     #             action=action_desc,
    #     #             agent_name=agent.name,
    #     #             agent_summary=agent.summary,
    #     #             world_nodes=agent.world_nodes,
    #     #             current_location=data.current_location,
    #     #         )
    #     #
    #     #         print(res)
    #     #
    #     #         return json.loads(res)
    #     #
    #     # return {
    #     #     'action': 'empty',
    #     #     'minutes': 0,
    #     #     'action_type': 'move_to'
    #     # }

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
                # query=f'What is {agent.name} looking to do next, taking into account previous actions and plans?'
                query=f'What did {agent.name} do today?'
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
                    memory=f'{agent.name} did {action_desc}',
                )

                # agent.action_history.insert(0, action_desc)
                agent.action_history.append(f'{action_desc} : {current_hour}:{current_minute}')

                res = await DoSomething.request(
                    action=action_desc,
                    agent_name=agent.name,
                    agent_summary=agent.summary,
                    world_nodes=agent.world_nodes,
                    past_actions=str(agent.action_history),
                    current_location=data.current_location,
                    duration=period,
                )

                print(res)

                return json.loads(res)

        return {
            "destination": "TownCentre:JohnHouse:Bathroom:Shower",
            "speed": 4,
            "duration": 1,
            "reason": "Agent wants to take a shower",
            "action": "shower"
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
        combined_mem = f'Time: {time_data.current_hour}:{time_data.current_minute} -> {data.memory}'
        # combined_mem = f'{data.memory}'

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

    async def what_to_do_now_v2(self, data: WhatToDoNowData) -> TaskModel:
        agent = AgentManager().get_agent(agent_id=data.agent_id)
        current_hour = data.time_data.current_hour
        current_minute = data.time_data.current_minute

        recent_actions = await recent_action_summary(agent, data)

        relevant_mem_summary = await retrieve_relevant_mem(
            agent=agent,
            data=data,
            query=f'What did {agent.name} do today?',
        )

        next_plan_raw = await Planner.request(
            agent=agent,
            day_number=data.time_data.day_number,
            current_hour=data.time_data.current_hour,
            relevant_memories=relevant_mem_summary,
            recent_actions=recent_actions,
            today_plan=agent.daily_schedule,
        )

        print(next_plan_raw)

        next_plan_json = json.loads(next_plan_raw)

        task = TaskModel(**next_plan_json)
        await self.insert_memory(
            data=data,
            memory=f'{agent.name} did {task.task} starting with {current_hour}:{current_minute}',
        )

        agent.action_history.append(f'{task.task} done at hour: {current_hour}:{current_minute}')

        for action in task.actions:
            agent.action_history.append(f'{action.action} done at hour: {current_hour}:{current_minute}')

        return task

        # tasks = Tasks(**next_plan_json)
        #
        # for task in tasks.tasks:
        #
        #     await self.insert_memory(
        #         data=data,
        #         memory=f'{agent.name} did {task.task} starting with {current_hour}:{current_minute}',
        #     )
        #
        #     agent.action_history.append(f'{task.task} : {current_hour}:{current_minute}')
        #
        # return tasks

    async def emulate_day(self, data: WhatToDoNowData) -> Any:
        agent = AgentManager().get_agent(agent_id=data.agent_id)
        current_hour = data.time_data.current_hour
        current_minute = data.time_data.current_minute

        while current_hour < 24:
            model = await self.what_to_do_now_v2(data)
            total_minutes = 0
            for x in model.actions:
                total_minutes += x.duration

            current_minute += total_minutes
            if current_minute > 60:
                current_hour += current_minute // 60
                current_minute = current_minute % 60

            data.time_data.current_hour = current_hour
            data.time_data.current_minute = current_minute

        return True
