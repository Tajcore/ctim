import logging
import time

import sentry_sdk
from celery import Task
from django.conf import settings

from crew.models import ExecutionResultModel


class BaseTask(Task):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure"""
        self.logger.error(f"Task {self.name} [{task_id}] failed: {exc}", exc_info=True)
        if "crew_id" in kwargs:
            self.update_execution_result(kwargs["crew_id"], "Failed", str(exc))
        if settings.SENTRY_DSN:
            sentry_sdk.capture_exception(exc)

    def on_success(self, retval, task_id, args, kwargs):
        """Handle task success"""
        self.logger.info(f"Task {self.name} [{task_id}] succeeded")
        if "crew_id" in kwargs:
            self.update_execution_result(kwargs["crew_id"], "Succeeded", retval)

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        try:
            result = super().__call__(*args, **kwargs)
            return result
        finally:
            total_time = time.time() - start_time
            self.logger.info(f"Task {self.name} [{self.request.id}] took {total_time:.2f} seconds")
            if getattr(settings, "TASK_SEND_TIME_TO_SENTRY", False):
                sentry_sdk.capture_message(f"Task {self.name} [{self.request.id}] took {total_time:.2f} seconds")
            self.logger.info(f"Task {self.name} [{self.request.id}] retries: {self.request.retries}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Handle task retry"""
        self.logger.warning(f"Task {self.name} [{task_id}] retry {self.request.retries} due to: {exc}")
        if "crew_id" in kwargs:
            self.update_execution_result(kwargs["crew_id"], "Retrying", str(exc))
        if settings.SENTRY_DSN:
            sentry_sdk.capture_exception(exc)

    def update_execution_result(self, crew_id, status, result_data):
        """Update the ExecutionResultModel with the task status and result"""
        try:
            execution_result, created = ExecutionResultModel.objects.update_or_create(
                crew_id=crew_id, defaults={"status": status, "result_data": result_data, "timestamp": time.time()}
            )
            self.logger.info(f"Updated ExecutionResultModel for Crew {crew_id} with status {status}")
        except Exception as e:
            self.logger.error(f"Failed to update ExecutionResultModel for Crew {crew_id}: {e}", exc_info=True)
            if settings.SENTRY_DSN:
                sentry_sdk.capture_exception(e)
