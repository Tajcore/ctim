from django.core.exceptions import ValidationError
from django.test import TestCase
from crew.models import CrewModel, AgentModel, TaskModel, ToolModel, ToolRegistryModel

class CrewModelTests(TestCase):

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
        
        self.crew = CrewModel.objects.create(
            name="Crew1",
            status="Active"
        )
        self.crew.agents.add(self.agent)
        self.crew.tasks.add(self.task)

    # Validation Tests
    def test_valid_crew(self):
        try:
            self.crew.full_clean()
        except ValidationError:
            self.fail("Crew model raised ValidationError unexpectedly!")

    def test_missing_name(self):
        crew = CrewModel(
            status="Active"
        )
        with self.assertRaises(ValidationError):
            crew.full_clean()

    def test_default_status(self):
        crew = CrewModel.objects.create(
            name="Crew2"
        )
        self.assertEqual(crew.status, "Pending")

    # Relationship Tests
    def test_add_agents_to_crew(self):
        agent2 = AgentModel.objects.create(
            role="Agent2",
            goal="Goal2",
            backstory="Backstory2"
        )
        self.crew.agents.add(agent2)
        self.assertIn(agent2, self.crew.agents.all())

    def test_remove_agent_from_crew(self):
        self.crew.agents.remove(self.agent)
        self.assertNotIn(self.agent, self.crew.agents.all())

    def test_add_tasks_to_crew(self):
        task2 = TaskModel.objects.create(
            name="Task2",
            description="Task description2",
            expected_output="Expected output2",
            status="Pending",
            agent=self.agent
        )
        self.crew.tasks.add(task2)
        self.assertIn(task2, self.crew.tasks.all())

    def test_remove_task_from_crew(self):
        self.crew.tasks.remove(self.task)
        self.assertNotIn(self.task, self.crew.tasks.all())

    # Edge Case Tests
    def test_long_strings_for_name_status(self):
        long_string = "a" * 100
        crew = CrewModel.objects.create(
            name=long_string,
            status=long_string[:50]
        )
        try:
            crew.full_clean()
        except ValidationError:
            self.fail("Crew model raised ValidationError unexpectedly!")

    def test_assign_empty_agents_and_tasks(self):
        crew = CrewModel.objects.create(
            name="Crew3",
            status="Active"
        )
        crew.agents.set([])
        crew.tasks.set([])
        self.assertEqual(crew.agents.count(), 0)
        self.assertEqual(crew.tasks.count(), 0)

    # Integration Tests
    def test_create_crew_with_agents_and_tasks(self):
        agent2 = AgentModel.objects.create(
            role="Agent2",
            goal="Goal2",
            backstory="Backstory2"
        )
        task2 = TaskModel.objects.create(
            name="Task2",
            description="Task description2",
            expected_output="Expected output2",
            status="Pending",
            agent=agent2
        )
        crew = CrewModel.objects.create(
            name="Crew4",
            status="Active"
        )
        crew.agents.add(agent2)
        crew.tasks.add(task2)
        self.assertEqual(crew.agents.count(), 1)
        self.assertEqual(crew.tasks.count(), 1)
        self.assertIn(agent2, crew.agents.all())
        self.assertIn(task2, crew.tasks.all())

    def test_update_crew_to_add_remove_agents_and_tasks(self):
        agent2 = AgentModel.objects.create(
            role="Agent2",
            goal="Goal2",
            backstory="Backstory2"
        )
        task2 = TaskModel.objects.create(
            name="Task2",
            description="Task description2",
            expected_output="Expected output2",
            status="Pending",
            agent=agent2
        )
        self.crew.agents.add(agent2)
        self.crew.tasks.add(task2)
        self.assertIn(agent2, self.crew.agents.all())
        self.assertIn(task2, self.crew.tasks.all())
        self.crew.agents.remove(agent2)
        self.crew.tasks.remove(task2)
        self.assertNotIn(agent2, self.crew.agents.all())
        self.assertNotIn(task2, self.crew.tasks.all())
