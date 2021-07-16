from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class ApSchedulerJobsTableBase:
    def __init__(self,
                 id: str = None,
                 next_run_time: float = None,
                 job_state=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id: str = id
        self.next_run_time: float = next_run_time
        self.job_state = job_state
