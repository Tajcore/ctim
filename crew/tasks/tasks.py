# tasks.py
import logging

from celery import shared_task

from crew.factories import CrewFactory
from crew.models import CrewModel, ExecutionResultModel
from crew.tasks.base import BaseTask


@shared_task(base=BaseTask, name="run_crew_task", soft_time_limit=60)
def run_crew_task(crew_id):
    logger = logging.getLogger(__name__)
    try:
        crew_model = CrewModel.objects.get(id=crew_id)
        crew_instance = CrewFactory.create(crew_model)
        result = crew_instance.kickoff(inputs={"topic": "Artificial Intelligence"})
        ExecutionResultModel.objects.create(crew=crew_model, status="Completed", result_data=result)
        logger.info(f"Execution of Crew {crew_id} completed successfully.")
        return result
    except CrewModel.DoesNotExist:
        logger.error(f"Crew with id {crew_id} does not exist.")
        raise
    except Exception as e:
        logger.error(f"Error occurred while executing Crew {crew_id}: {e}")
        raise
