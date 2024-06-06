# factories.py
import importlib

from crewai import Agent, Crew, Task


class ToolFactory:
    @staticmethod
    def create(tool_model):
        tool_registry = tool_model.registry
        module = importlib.import_module(tool_registry.module_path)
        tool_method = getattr(module, tool_registry.method_name)
        return tool_method


class AgentFactory:
    @staticmethod
    def create(agent_model):
        tools = [ToolFactory.create(tool) for tool in agent_model.tools.all()]
        return Agent(role=agent_model.role, goal=agent_model.goal, backstory=agent_model.backstory, tools=tools)


class TaskFactory:
    @staticmethod
    def create(task_model):
        agent_instance = AgentFactory.create(task_model.agent)
        tools = [ToolFactory.create(tool) for tool in task_model.tools.all()]
        return Task(
            description=task_model.description,
            expected_output=task_model.expected_output,
            agent=agent_instance,
            tools=tools,
        )


class CrewFactory:
    @staticmethod
    def create(crew_model):
        agents = [AgentFactory.create(agent) for agent in crew_model.agents.all()]
        tasks = [TaskFactory.create(task) for task in crew_model.tasks.all()]
        return Crew(agents=agents, tasks=tasks, verbose=2)
