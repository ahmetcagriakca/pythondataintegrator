def start():
    from infrastructor.IocManager import IocManager

    import os
    root_directory = os.path.dirname(os.path.abspath(__file__))
    from infrastructor.scheduler.JobScheduler import JobScheduler

    IocManager.configure_startup(root_directory=root_directory, job_scheduler=JobScheduler)
    IocManager.run()


if __name__ == "__main__":
    start()
