# factories.py
import importlib
import logging

from asgiref.sync import sync_to_async
from crewai import Agent, Crew, Task

logger = logging.getLogger(__name__)


class ToolFactory:
    @staticmethod
    def create(tool_model):
        logger.debug(f"Creating tool from model: {tool_model}")

        tool_registry = tool_model.registry
        module = importlib.import_module(tool_registry.module_path)

        cls = getattr(module, tool_registry.method_name, None)
        object = cls()

        logger.debug(f"Created tool method: {object}")

        return object


class AgentFactory:
    @staticmethod
    def create(agent_model):
        logger.debug(f"Creating agent from model: {agent_model}")
        tools = [ToolFactory.create(tool) for tool in agent_model.tools.all()]
        logger.debug(f"Tools created for agent: {tools}")

        if tools:
            agent = Agent(role=agent_model.role, goal=agent_model.goal, backstory=agent_model.backstory, tools=tools)
        else:
            agent = Agent(role=agent_model.role, goal=agent_model.goal, backstory=agent_model.backstory)

        logger.debug(f"Created agent: {agent}")
        return agent

    async def create_async(agent_model):
        logger.debug(f"Creating agent from model: {agent_model}")

        # Use sync_to_async to fetch tools
        tools = await sync_to_async(lambda: [ToolFactory.create(tool) for tool in agent_model.tools.all()])()
        logger.debug(f"Tools created for agent: {tools}")

        if tools:
            agent = Agent(role=agent_model.role, goal=agent_model.goal, backstory=agent_model.backstory, tools=tools)
        else:
            agent = Agent(role=agent_model.role, goal=agent_model.goal, backstory=agent_model.backstory)

        logger.debug(f"Created agent: {agent}")
        return agent


class TaskFactory:
    @staticmethod
    def create(task_model):
        logger.debug(f"Creating task from model: {task_model}")
        agent_instance = AgentFactory.create(task_model.agent)
        tools = [ToolFactory.create(tool) for tool in task_model.tools.all()]
        logger.debug(f"Tools created for task: {tools}")
        task = Task(
            description=task_model.description,
            expected_output=task_model.expected_output,
            agent=agent_instance,
            tools=tools,
        )
        logger.debug(f"Created task: {task}")
        return task


class CrewFactory:
    @staticmethod
    def create(crew_model):
        logger.debug(f"Creating crew from model: {crew_model}")
        agents = [AgentFactory.create(agent) for agent in crew_model.agents.all()]
        logger.debug(f"Agents created for crew: {agents}")
        tasks = [TaskFactory.create(task) for task in crew_model.tasks.all()]
        logger.debug(f"Tasks created for crew: {tasks}")

        crew = Crew(agents=agents, tasks=tasks, verbose=2)
        logger.debug(f"Created crew: {crew}")
        return crew
