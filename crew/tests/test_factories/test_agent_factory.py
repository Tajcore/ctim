import unittest
from unittest.mock import patch, MagicMock
from crew.factories import AgentFactory, ToolFactory
from crew.models import AgentModel, ToolModel, ToolRegistryModel
from django.core.exceptions import ValidationError
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

class Agent:
    def __init__(self, role, goal, backstory, tools):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools

class AgentFactoryTests(unittest.TestCase):

    def setUp(self):
        self.tool_registry = ToolRegistryModelFactory.create()
        self.tool = ToolModelFactory.create(registry=self.tool_registry)
        self.agent = AgentModelFactory.create()
        self.agent.tools.add(self.tool)

    # Validation Tests
    @patch.object(ToolFactory, 'create')
    def test_create_agent_instance_from_valid_agent_model(self, mock_tool_factory_create):
        mock_tool = MagicMock()
        mock_tool_factory_create.return_value = mock_tool

        agent_instance = AgentFactory.create(self.agent)
        self.assertEqual(agent_instance.role, self.agent.role)
        self.assertEqual(agent_instance.goal, self.agent.goal)
        self.assertEqual(agent_instance.backstory, self.agent.backstory)
        self.assertEqual(agent_instance.tools, [mock_tool])

    # Relationship Tests
    @patch.object(ToolFactory, 'create')
    def test_create_agent_with_multiple_tools(self, mock_tool_factory_create):
        mock_tool = MagicMock()
        mock_tool_factory_create.return_value = mock_tool

        tool2 = ToolModelFactory.create(registry=self.tool_registry)
        self.agent.tools.add(tool2)

        agent_instance = AgentFactory.create(self.agent)
        self.assertEqual(agent_instance.tools, [mock_tool, mock_tool])

    @patch.object(ToolFactory, 'create')
    def test_create_agent_without_tools(self, mock_tool_factory_create):
        self.agent.tools.clear()

        agent_instance = AgentFactory.create(self.agent)
        self.assertEqual(agent_instance.tools, [])

    # Boundary Tests
    @patch.object(ToolFactory, 'create')
    def test_create_agent_with_long_strings(self, mock_tool_factory_create):
        long_string = "a" * 1000
        self.agent.role = long_string
        self.agent.goal = long_string
        self.agent.backstory = long_string
        self.agent.save()

        mock_tool = MagicMock()
        mock_tool_factory_create.return_value = mock_tool

        agent_instance = AgentFactory.create(self.agent)
        self.assertEqual(agent_instance.role, long_string)
        self.assertEqual(agent_instance.goal, long_string)
        self.assertEqual(agent_instance.backstory, long_string)

    # Error Handling Tests
    @patch.object(ToolFactory, 'create')
    def test_create_agent_from_invalid_agent_model(self, mock_tool_factory_create):
        invalid_agent = MagicMock(spec=AgentModel)
        invalid_agent.tools.all.return_value = []

        with self.assertRaises(AttributeError):
            AgentFactory.create(invalid_agent)

    @patch.object(ToolFactory, 'create')
    def test_create_agent_with_invalid_tool_model(self, mock_tool_factory_create):
        mock_tool_factory_create.side_effect = ValidationError("Invalid tool model")

        with self.assertRaises(ValidationError):
            AgentFactory.create(self.agent)

if __name__ == "__main__":
    unittest.main()
