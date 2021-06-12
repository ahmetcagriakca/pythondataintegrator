

def start():
    from IocManager import IocManager

    from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
    from infrastructor.scheduler.JobScheduler import JobScheduler
    from infrastructor.rpc.SchedulerService import SchedulerService

    IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
    IocManager.set_job_scheduler(job_scheduler=JobScheduler)
    IocManager.set_scheduler_service(scheduler_service=SchedulerService())
    IocManager.initialize()
    IocManager.run()


if __name__ == "__main__":
    start()
