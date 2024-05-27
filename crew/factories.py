# factories.py
from crewai import Agent, Crew, Task


class AgentFactory:
    @staticmethod
    def create(agent_model):
        return Agent(role=agent_model.role, goal=agent_model.goal, backstory=agent_model.backstory)


class TaskFactory:
    @staticmethod
    def create(task_model):
        agent_instance = AgentFactory.create(task_model.agent)
        return Task(
            description=task_model.description, expected_output=task_model.expected_output, agent=agent_instance
        )


class CrewFactory:
    @staticmethod
    def create(crew_model):
        agents = [AgentFactory.create(agent) for agent in crew_model.agents.all()]
        tasks = [TaskFactory.create(task) for task in crew_model.tasks.all()]
        return Crew(agents=agents, tasks=tasks, verbose=2)
