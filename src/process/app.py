if __name__ == "__main__":
    from pdip.base import Pdi
    from process.rpc.ProcessService import ProcessService

    pdi = Pdi(excluded_modules=["tests", "venv"])
    process_service = pdi.get(ProcessService)
    process_service.run()
