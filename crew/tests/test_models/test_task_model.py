from django.core.exceptions import ValidationError
from django.test import TestCase
from crew.models import TaskModel, AgentModel, ToolModel, ToolRegistryModel

class TaskModelTests(TestCase):

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
        
        self.task = TaskModel.objects.create(
            name="Task1",
            description="Task description",
            expected_output="Expected output",
            status="Pending",
            agent=self.agent
        )
        self.task.tools.add(self.tool)

    # Validation Tests
    def test_valid_task(self):
        try:
            self.task.full_clean()
        except ValidationError:
            self.fail("Task model raised ValidationError unexpectedly!")

    def test_missing_name(self):
        task = TaskModel(
            description="Task description",
            expected_output="Expected output",
            status="Pending",
            agent=self.agent
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_missing_description(self):
        task = TaskModel(
            name="Task2",
            expected_output="Expected output",
            status="Pending",
            agent=self.agent
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_missing_expected_output(self):
        task = TaskModel(
            name="Task2",
            description="Task description",
            status="Pending",
            agent=self.agent
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    # Relationship Tests
    def test_add_tools_to_task(self):
        tool_registry_2 = ToolRegistryModel.objects.create(
            name="ToolRegistry2",
            description="Another tool registry description",
            module_path="allowed.module.path",
            method_name="method_name"
        )
        tool_2 = ToolModel.objects.create(registry=tool_registry_2)
        self.task.tools.add(tool_2)
        self.assertIn(tool_2, self.task.tools.all())

    def test_remove_tool_from_task(self):
        self.task.tools.remove(self.tool)
        self.assertNotIn(self.tool, self.task.tools.all())

    def test_change_agent_of_task(self):
        agent2 = AgentModel.objects.create(
            role="Agent2",
            goal="Goal2",
            backstory="Backstory2"
        )
        self.task.agent = agent2
        self.task.save()
        self.assertEqual(self.task.agent, agent2)

    # Edge Case Tests
    def test_long_strings_for_name_description_expected_output(self):
        long_string = "a" * 1000
        task = TaskModel.objects.create(
            name="a" * 100,
            description=long_string,
            expected_output=long_string,
            status="Pending",
            agent=self.agent
        )
        try:
            task.full_clean()
        except ValidationError:
            self.fail("Task model raised ValidationError unexpectedly!")

    def test_assign_empty_tools(self):
        task = TaskModel.objects.create(
            name="Task3",
            description="Task description",
            expected_output="Expected output",
            status="Pending",
            agent=self.agent
        )
        task.tools.set([])
        self.assertEqual(task.tools.count(), 0)

    # Integration Tests
    def test_create_task_with_tools(self):
        tool_registry_2 = ToolRegistryModel.objects.create(
            name="ToolRegistry2",
            description="Another tool registry description",
            module_path="allowed.module.path",
            method_name="method_name"
        )
        tool_2 = ToolModel.objects.create(registry=tool_registry_2)
        task = TaskModel.objects.create(
            name="Task4",
            description="Task description",
            expected_output="Expected output",
            status="Pending",
            agent=self.agent
        )
        task.tools.add(tool_2)
        self.assertEqual(task.tools.count(), 1)
        self.assertIn(tool_2, task.tools.all())

    def test_update_task_to_add_remove_tools(self):
        tool_registry_2 = ToolRegistryModel.objects.create(
            name="ToolRegistry2",
            description="Another tool registry description",
            module_path="allowed.module.path",
            method_name="method_name"
        )
        tool_2 = ToolModel.objects.create(registry=tool_registry_2)
        self.task.tools.add(tool_2)
        self.assertIn(tool_2, self.task.tools.all())
        self.task.tools.remove(tool_2)
        self.assertNotIn(tool_2, self.task.tools.all())
