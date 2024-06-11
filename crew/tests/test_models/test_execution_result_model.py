from django.core.exceptions import ValidationError
from django.test import TestCase
from crew.models import ExecutionResultModel, CrewModel, AgentModel, TaskModel, ToolModel, ToolRegistryModel

class ExecutionResultModelTests(TestCase):

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
        
        self.execution_result = ExecutionResultModel.objects.create(
            crew=self.crew,
            status="Success",
            result_data="Some result data"
        )

    # Validation Tests
    def test_valid_execution_result(self):
        try:
            self.execution_result.full_clean()
        except ValidationError:
            self.fail("ExecutionResultModel raised ValidationError unexpectedly!")

    def test_missing_status(self):
        execution_result = ExecutionResultModel(
            crew=self.crew,
            result_data="Some result data"
        )
        with self.assertRaises(ValidationError):
            execution_result.full_clean()

    def test_missing_result_data(self):
        execution_result = ExecutionResultModel(
            crew=self.crew,
            status="Success"
        )
        with self.assertRaises(ValidationError):
            execution_result.full_clean()

    # Relationship Tests
    def test_crew_relationship(self):
        self.assertEqual(self.execution_result.crew, self.crew)

    # Edge Case Tests
    def test_long_strings_for_status_result_data(self):
        long_string = "a" * 1000
        execution_result = ExecutionResultModel.objects.create(
            crew=self.crew,
            status="a" * 50,
            result_data=long_string
        )
        try:
            execution_result.full_clean()
        except ValidationError:
            self.fail("ExecutionResultModel raised ValidationError unexpectedly!")

    # Integration Tests
    def test_create_execution_result(self):
        execution_result = ExecutionResultModel.objects.create(
            crew=self.crew,
            status="Failed",
            result_data="Detailed error report"
        )
        self.assertEqual(execution_result.crew, self.crew)
        self.assertEqual(execution_result.status, "Failed")
        self.assertEqual(execution_result.result_data, "Detailed error report")

    def test_update_execution_result(self):
        self.execution_result.status = "Failed"
        self.execution_result.result_data = "Updated result data"
        self.execution_result.save()
        updated_execution_result = ExecutionResultModel.objects.get(id=self.execution_result.id)
        self.assertEqual(updated_execution_result.status, "Failed")
        self.assertEqual(updated_execution_result.result_data, "Updated result data")
