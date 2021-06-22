from IocManager import IocManager
from rpc.ProcessService import ProcessService


def start():
    IocManager.set_process_service(process_service=ProcessService)
    IocManager.initialize()
    IocManager.process_info()
    IocManager.run()


if __name__ == "__main__":
    start()
