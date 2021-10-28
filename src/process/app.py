if __name__ == "__main__":
    from pdip.base import Pdi
    from rpc.ProcessService import ProcessService

    pdi = Pdi()
    process_service = pdi.get(ProcessService)
    process_service.run()
