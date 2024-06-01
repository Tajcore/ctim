from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class ToolRegistryModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    module_path = models.CharField(max_length=255)
    method_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        allowed_paths = getattr(settings, "ALLOWED_TOOL_MODULE_PATHS", [])
        if not any(self.module_path.startswith(prefix) for prefix in allowed_paths):
            raise ValidationError(f"Module path {self.module_path} is not allowed.")

    def __str__(self):
        return self.name


class ToolModel(models.Model):
    registry = models.ForeignKey(ToolRegistryModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registry.name}"


class AgentModel(models.Model):
    role = models.CharField(max_length=100)
    goal = models.TextField()
    backstory = models.TextField()
    tools = models.ManyToManyField(ToolModel)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role


class TaskModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    expected_output = models.TextField()
    status = models.CharField(max_length=50, default="Pending")
    agent = models.ForeignKey(AgentModel, on_delete=models.CASCADE)
    tools = models.ManyToManyField(ToolModel)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CrewModel(models.Model):
    name = models.CharField(max_length=100)
    agents = models.ManyToManyField(AgentModel)
    tasks = models.ManyToManyField(TaskModel)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Crew {self.name}"


class ExecutionResultModel(models.Model):
    crew = models.ForeignKey(CrewModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    result_data = models.TextField()

    def __str__(self):
        return f"Result for Crew {self.crew.name}"
