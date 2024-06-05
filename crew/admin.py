from django.contrib import admin

from crew.tasks.tasks import run_crew_task

from .models import AgentModel, CrewModel, ExecutionResultModel, TaskModel, ToolModel, ToolRegistryModel


@admin.register(ToolRegistryModel)
class ToolRegistryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "module_path", "method_name")
    search_fields = ("name", "module_path", "method_name")
    readonly_fields = ("created_at", "updated_at")

    # Optional: Customize the form display
    fieldsets = ((None, {"fields": ("name", "description", "module_path", "method_name")}),)


@admin.register(ToolModel)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("registry", "created_at", "updated_at")
    search_fields = ("registry__name",)
    readonly_fields = ("created_at", "updated_at")

    # Optional: Customize the form display
    fieldsets = ((None, {"fields": ("registry",)}),)


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
