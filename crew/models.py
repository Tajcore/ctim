from django.db import models


class AgentModel(models.Model):
    role = models.CharField(max_length=100)
    goal = models.TextField()
    backstory = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role


class TaskModel(models.Model):
    description = models.TextField()
    expected_output = models.TextField()
    status = models.CharField(max_length=50, default="Pending")
    agent = models.ForeignKey(AgentModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class CrewModel(models.Model):
    agents = models.ManyToManyField(AgentModel)
    tasks = models.ManyToManyField(TaskModel)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Crew {self.id}"


class ExecutionResultModel(models.Model):
    crew = models.ForeignKey(CrewModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    result_data = models.TextField()

    def __str__(self):
        return f"Result for Crew {self.crew.id}"
