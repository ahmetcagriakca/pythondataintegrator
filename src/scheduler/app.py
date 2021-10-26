if __name__ == "__main__":
    from pdip.base import Pdi

    from scheduler.application.scheduler.JobScheduler import JobScheduler
    from scheduler.rpc.SchedulerService import SchedulerService

    pdi = Pdi()
    job_scheduler = pdi.get(JobScheduler)
    job_scheduler.run()
    scheduler_service = pdi.get(SchedulerService)
    scheduler_service.run()
