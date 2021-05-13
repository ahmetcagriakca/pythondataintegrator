from sqlalchemy import Column, String, Boolean, Float, TEXT, REAL, Integer, LargeBinary, Unicode
from infrastructor.IocManager import IocManager


class ApSchedulerJobsTable(IocManager.Base):
    # TODO: This feels bad man
    __tablename__ = "ApSchedulerJobsTable"
    __table_args__ = {"schema": "Aps"}

    Id = Column('id', Unicode(191, _warn_on_bytestring=False), primary_key=True)
    NextRunTime = Column('next_run_time', Float(25), index=True)
    JobState = Column('job_state', LargeBinary, nullable=False)

    def __init__(self,
                 id: TEXT = None,
                 next_run_time: float = None,
                 job_state=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id: TEXT = id
        self.next_run_time: float = next_run_time
        self.job_state = job_state
