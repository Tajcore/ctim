import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
from crew.factories import TaskFactory, AgentFactory, ToolFactory
from crew.models import TaskModel, AgentModel, ToolModel, ToolRegistryModel
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

    description = factory.Faker('sentence')
    expected_output = factory.Faker('sentence')
    status = factory.Faker('word')
    agent = factory.SubFactory(AgentModelFactory)

class Task:
    def __init__(self, description, expected_output, agent, tools):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.tools = tools

class TaskFactoryTests(unittest.TestCase):

    def setUp(self):
        self.tool_registry = ToolRegistryModelFactory.create()
        self.tool = ToolModelFactory.create(registry=self.tool_registry)
        self.agent = AgentModelFactory.create()
        self.agent.tools.add(self.tool)
        self.task = TaskModelFactory.create(agent=self.agent)
        self.task.tools.add(self.tool)

    # Validation Tests
    @patch.object(ToolFactory, 'create')
    @patch.object(AgentFactory, 'create')
    def test_create_task_instance_from_valid_task_model(self, mock_agent_factory_create, mock_tool_factory_create):
        mock_agent = MagicMock()
        mock_tool = MagicMock()
        mock_agent_factory_create.return_value = mock_agent
        mock_tool_factory_create.return_value = mock_tool

        task_instance = TaskFactory.create(self.task)
        self.assertEqual(task_instance.description, self.task.description)
        self.assertEqual(task_instance.expected_output, self.task.expected_output)
        self.assertEqual(task_instance.agent, mock_agent)
        self.assertEqual(task_instance.tools, [mock_tool])

    # Relationship Tests
    @patch.object(ToolFactory, 'create')
    @patch.object(AgentFactory, 'create')
    def test_create_task_with_multiple_tools(self, mock_agent_factory_create, mock_tool_factory_create):
        mock_agent = MagicMock()
        mock_tool = MagicMock()
        mock_agent_factory_create.return_value = mock_agent
        mock_tool_factory_create.return_value = mock_tool

        tool2 = ToolModelFactory.create(registry=self.tool_registry)
        self.task.tools.add(tool2)

        task_instance = TaskFactory.create(self.task)
        self.assertEqual(task_instance.tools, [mock_tool, mock_tool])

    @patch.object(ToolFactory, 'create')
    @patch.object(AgentFactory, 'create')
    def test_create_task_without_tools(self, mock_agent_factory_create, mock_tool_factory_create):
        self.task.tools.clear()

        mock_agent = MagicMock()
        mock_agent_factory_create.return_value = mock_agent

        task_instance = TaskFactory.create(self.task)
        self.assertEqual(task_instance.tools, [])

    # Boundary Tests
    @patch.object(ToolFactory, 'create')
    @patch.object(AgentFactory, 'create')
    def test_create_task_with_long_strings(self, mock_agent_factory_create, mock_tool_factory_create):
        long_string = "a" * 1000
        self.task.description = long_string
        self.task.expected_output = long_string
        self.task.save()

        mock_agent = MagicMock()
        mock_tool = MagicMock()
        mock_agent_factory_create.return_value = mock_agent
        mock_tool_factory_create.return_value = mock_tool

        task_instance = TaskFactory.create(self.task)
        self.assertEqual(task_instance.description, long_string)
        self.assertEqual(task_instance.expected_output, long_string)

    # Error Handling Tests
    @patch.object(ToolFactory, 'create')
    @patch.object(AgentFactory, 'create')
    def test_create_task_from_invalid_task_model(self, mock_agent_factory_create, mock_tool_factory_create):
        invalid_task = MagicMock(spec=TaskModel)
        invalid_task.tools.all.return_value = []
        invalid_task.agent = None

        with self.assertRaises(AttributeError):
            TaskFactory.create(invalid_task)

    @patch.object(ToolFactory, 'create')
    @patch.object(AgentFactory, 'create')
    def test_create_task_with_invalid_tool_model(self, mock_agent_factory_create, mock_tool_factory_create):
        mock_tool_factory_create.side_effect = ValidationError("Invalid tool model")

        with self.assertRaises(ValidationError):
            TaskFactory.create(self.task)

    @patch.object(ToolFactory, 'create')
    @patch.object(AgentFactory, 'create')
    def test_create_task_with_invalid_agent_model(self, mock_agent_factory_create, mock_tool_factory_create):
        mock_agent_factory_create.side_effect = ValidationError("Invalid agent model")

        with self.assertRaises(ValidationError):
            TaskFactory.create(self.task)

if __name__ == "__main__":
    unittest.main()
