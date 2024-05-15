from agent.agent import Agent
from routers.router_data import InitializeAgentData


class AgentManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
            cls._instance.agents = {}
        return cls._instance

    def reset_instance(self):
        self._instance.agents = {}

    def add_agent(self, agent):
        """Add an Agent to the manager. Assumes that each agent's ID is unique."""
        if agent.id in self.agents:
            raise ValueError("An agent with this ID already exists.")
        self.agents[agent.id] = agent

    def initialize_agent(self, data: InitializeAgentData):
        agent = Agent(
            agent_id=data.agent_id,
            name=data.agent_name,
            summary=data.agent_summary,
            wake_up_hour=data.agent_wake_up_hour,
            world_nodes=data.world_nodes,
            current_location=data.current_location
        )
        try:
            self.add_agent(agent)
            print(f'Agent manager: initialized agent {agent}')
        except:
            print('Agent could not be initialized')

    def update_location(self, agent_id: str, new_location: str):
        if agent_id not in self.agents:
            raise ValueError(f"Agent with id {agent_id} doesn't exist.")
        self.agents[agent_id].current_location = new_location

    def get_agent(self, agent_id) -> Agent:
        """Retrieve an Agent by name."""
        return self.agents.get(agent_id, None)

    def __str__(self):
        return f"AgentManager currently managing {len(self.agents)} agents."
