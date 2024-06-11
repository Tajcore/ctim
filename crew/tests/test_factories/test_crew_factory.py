import unittest
from unittest.mock import patch, MagicMock
from crew.factories import CrewFactory
from crew.models import CrewModel, AgentModel, TaskModel, ToolModel, ToolRegistryModel
from factory.django import DjangoModelFactory
import factory

class ToolRegistryModelFactory(DjangoModelFactory):
    class Meta:
        model = ToolRegistryModel

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    module_path = "some_module"
    method_name = "some_method"

class ToolModelFactory(DjangoModelFactory):
    class Meta:
        model = ToolModel

    registry = factory.SubFactory(ToolRegistryModelFactory)

class AgentModelFactory(DjangoModelFactory):
    class Meta:
        model = AgentModel

    role = factory.Faker('word')
    goal = factory.Faker('sentence')
    backstory = factory.Faker('paragraph')

class TaskModelFactory(DjangoModelFactory):
    class Meta:
        model = TaskModel

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    expected_output = factory.Faker('sentence')
    status = "Pending"
    agent = factory.SubFactory(AgentModelFactory)

class CrewModelFactory(DjangoModelFactory):
    class Meta:
        model = CrewModel

    name = factory.Faker('word')
    status = "Active"

    @factory.post_generation
    def agents(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for agent in extracted:
                self.agents.add(agent)

    @factory.post_generation
    def tasks(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for task in extracted:
                self.tasks.add(task)

class CrewFactoryTests(unittest.TestCase):

    def setUp(self):
        self.tool_registry = ToolRegistryModelFactory.create()
        self.tool = ToolModelFactory.create(registry=self.tool_registry)
        
        self.agent = AgentModelFactory.create()
        self.agent.tools.add(self.tool)
        
        self.task = TaskModelFactory.create(agent=self.agent)
        self.task.tools.add(self.tool)
        
        self.crew = CrewModelFactory.create(agents=[self.agent], tasks=[self.task])

    # Validation Tests
    @patch('crew.factories.AgentFactory.create')
    @patch('crew.factories.TaskFactory.create')
    def test_create_crew_instance_from_valid_crew_model(self, mock_task_factory, mock_agent_factory):
        mock_agent = MagicMock()
        mock_task = MagicMock()
        mock_agent_factory.return_value = mock_agent
        mock_task_factory.return_value = mock_task
        
        crew_instance = CrewFactory.create(self.crew)
        self.assertEqual(crew_instance.agents, [mock_agent])
        self.assertEqual(crew_instance.tasks, [mock_task])

    # Relationship Tests
    @patch('crew.factories.AgentFactory.create')
    @patch('crew.factories.TaskFactory.create')
    def test_create_crew_with_multiple_agents_and_tasks(self, mock_task_factory, mock_agent_factory):
        agent2 = AgentModelFactory.create()
        task2 = TaskModelFactory.create(agent=agent2)
        self.crew.agents.add(agent2)
        self.crew.tasks.add(task2)

        mock_agent1 = MagicMock()
        mock_agent2 = MagicMock()
        mock_task1 = MagicMock()
        mock_task2 = MagicMock()
        
        mock_agent_factory.side_effect = [mock_agent1, mock_agent2]
        mock_task_factory.side_effect = [mock_task1, mock_task2]

        crew_instance = CrewFactory.create(self.crew)
        self.assertEqual(crew_instance.agents, [mock_agent1, mock_agent2])
        self.assertEqual(crew_instance.tasks, [mock_task1, mock_task2])

    # Error Handling Tests
    @patch('crew.factories.AgentFactory.create')
    @patch('crew.factories.TaskFactory.create')
    def test_create_crew_from_invalid_crew_model_raises_error(self, mock_task_factory, mock_agent_factory):
        self.crew.agents.clear()
        self.crew.tasks.clear()
        with self.assertRaises(ValueError):
            CrewFactory.create(self.crew)

if __name__ == "__main__":
    unittest.main()
