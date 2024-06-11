from django.core.exceptions import ValidationError
from django.test import TestCase
from crew.models import AgentModel, ToolModel, ToolRegistryModel

class AgentModelTests(TestCase):

    def setUp(self):
        self.tool_registry = ToolRegistryModel.objects.create(
            name="ToolRegistry1",
            description="A tool registry description",
            module_path="allowed.module.path",
            method_name="method_name"
        )
        self.tool = ToolModel.objects.create(registry=self.tool_registry)
        self.agent = AgentModel.objects.create(
            role="Agent",
            goal="Goal",
            backstory="Backstory"
        )
        self.agent.tools.add(self.tool)

    # Validation Tests
    def test_valid_agent(self):
        try:
            self.agent.full_clean()
        except ValidationError:
            self.fail("Agent model raised ValidationError unexpectedly!")

    def test_missing_role(self):
        agent = AgentModel(
            goal="Goal",
            backstory="Backstory"
        )
        with self.assertRaises(ValidationError):
            agent.full_clean()

    def test_missing_goal(self):
        agent = AgentModel(
            role="Agent",
            backstory="Backstory"
        )
        with self.assertRaises(ValidationError):
            agent.full_clean()

    def test_missing_backstory(self):
        agent = AgentModel(
            role="Agent",
            goal="Goal"
        )
        with self.assertRaises(ValidationError):
            agent.full_clean()

    # Relationship Tests
    def test_add_tools_to_agent(self):
        tool_registry_2 = ToolRegistryModel.objects.create(
            name="ToolRegistry2",
            description="Another tool registry description",
            module_path="allowed.module.path",
            method_name="method_name"
        )
        tool_2 = ToolModel.objects.create(registry=tool_registry_2)
        self.agent.tools.add(tool_2)
        self.assertIn(tool_2, self.agent.tools.all())

    def test_remove_tool_from_agent(self):
        self.agent.tools.remove(self.tool)
        self.assertNotIn(self.tool, self.agent.tools.all())

    # Error Handling Tests
    def test_error_for_missing_fields(self):
        agent = AgentModel()
        with self.assertRaises(ValidationError):
            agent.full_clean()

    def test_duplicate_tool_entries(self):
        self.agent.tools.add(self.tool)
        self.assertEqual(self.agent.tools.count(), 1)

    # Edge Case Tests
    def test_long_strings_for_role_goal_backstory(self):
        long_string = "a" * 100  # Updated to match the max_length of role field
        agent = AgentModel.objects.create(
            role=long_string,
            goal=long_string,
            backstory=long_string
        )
        try:
            agent.full_clean()
        except ValidationError:
            self.fail("Agent model raised ValidationError unexpectedly!")

    def test_assign_empty_tools(self):
        agent = AgentModel.objects.create(
            role="Agent",
            goal="Goal",
            backstory="Backstory"
        )
        agent.tools.set([])
        self.assertEqual(agent.tools.count(), 0)

    # Integration Tests
    def test_create_agent_with_tools(self):
        tool_registry_2 = ToolRegistryModel.objects.create(
            name="ToolRegistry2",
            description="Another tool registry description",
            module_path="allowed.module.path",
            method_name="method_name"
        )
        tool_2 = ToolModel.objects.create(registry=tool_registry_2)
        agent = AgentModel.objects.create(
            role="Agent",
            goal="Goal",
            backstory="Backstory"
        )
        agent.tools.add(tool_2)
        self.assertEqual(agent.tools.count(), 1)
        self.assertIn(tool_2, agent.tools.all())

    def test_update_agent_to_add_remove_tools(self):
        tool_registry_2 = ToolRegistryModel.objects.create(
            name="ToolRegistry2",
            description="Another tool registry description",
            module_path="allowed.module.path",
            method_name="method_name"
        )
        tool_2 = ToolModel.objects.create(registry=tool_registry_2)
        self.agent.tools.add(tool_2)
        self.assertIn(tool_2, self.agent.tools.all())
        self.agent.tools.remove(tool_2)
        self.assertNotIn(tool_2, self.agent.tools.all())
