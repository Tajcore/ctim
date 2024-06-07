import logging

from django.contrib import admin
from unfold.admin import ModelAdmin

from crew.tasks.tasks import run_crew_task

from .models import AgentModel, CrewModel, ExecutionResultModel, TaskModel, ToolModel, ToolRegistryModel

logger = logging.getLogger(__name__)


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
class AgentAdmin(ModelAdmin):
    list_display = ("role", "goal", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(TaskModel)
class TaskAdmin(ModelAdmin):
    list_display = ("name", "description", "status", "agent", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CrewModel)
class CrewAdmin(ModelAdmin):
    list_display = ("name", "status", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    actions = ["kickoff_crew"]

    @admin.action(description="Kick off selected crew tasks")
    def kickoff_crew(self, request, queryset):
        # Get the logger
        logger = logging.getLogger("crew.factories")

        # Store the original logging level
        original_logging_level = logger.level
        logger.info(f"Original logging level: {logging.getLevelName(original_logging_level)}")

        # Set the logging level to DEBUG
        logger.setLevel(logging.DEBUG)
        logger.debug("Logging level set to DEBUG for detailed logging during task execution")

        try:
            for crew in queryset:
                logger.debug(f"Initiating task for crew ID: {crew.id}")
                run_crew_task.delay(crew.id)
                logger.info(f"Crew task for ID {crew.id} has been started.")
            self.message_user(request, "Crew task has been started.")
        finally:
            # Restore the original logging level
            logger.setLevel(original_logging_level)
            logger.info(f"Logging level restored to: {logging.getLevelName(original_logging_level)}")


@admin.register(ExecutionResultModel)
class ExecutionResultAdmin(ModelAdmin):
    list_display = ("crew", "timestamp", "status")
    readonly_fields = ("crew", "timestamp", "status")
