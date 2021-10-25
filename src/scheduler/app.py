
if __name__ == "__main__":
    import os

    from pdip.base import Pdi

    from scheduler.application.scheduler.JobScheduler import JobScheduler
    from scheduler.rpc.SchedulerService import SchedulerService

    dao_path = os.path.join('scheduler', 'domain','dao', 'aps', 'ApSchedulerJobsTable')
    pdi = Pdi(excluded_modules=[dao_path])
    job_scheduler = pdi.get(JobScheduler)
    job_scheduler.run()
    scheduler_service = pdi.get(SchedulerService)
    scheduler_service.run()


