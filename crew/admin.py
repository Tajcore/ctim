from django.contrib import admin

from crew.tasks.tasks import run_crew_task

from .models import AgentModel, CrewModel, ExecutionResultModel, TaskModel


@admin.register(AgentModel)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("role", "goal", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("description", "status", "agent", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CrewModel)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    actions = ["kickoff_crew"]

    @admin.action(description="Kick off selected crew tasks")
    def kickoff_crew(self, request, queryset):
        for crew in queryset:
            run_crew_task.delay(crew.id)
        self.message_user(request, "Crew task has been started.")


@admin.register(ExecutionResultModel)
class ExecutionResultAdmin(admin.ModelAdmin):
    list_display = ("crew", "timestamp", "status")
    readonly_fields = ("timestamp",)
