def start():
    from IocManager import IocManager

    from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
    from infrastructor.scheduler.JobScheduler import JobScheduler

    IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper, job_scheduler=JobScheduler)
    IocManager.initialize()
    IocManager.run()


if __name__ == "__main__":
    start()
