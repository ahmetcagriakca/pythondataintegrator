if __name__ == "__main__":
    from pdip.base import Pdi

    from src.application.scheduler.JobScheduler import JobScheduler
    from src.rpc.SchedulerService import SchedulerService

    pdi = Pdi(excluded_modules=["tests", "venv"])
    job_scheduler = pdi.get(JobScheduler)
    job_scheduler.run()
    scheduler_service = pdi.get(SchedulerService)
    scheduler_service.run()
