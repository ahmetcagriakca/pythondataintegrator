from sqlalchemy import Column, Float, TEXT, LargeBinary, Unicode
from IocManager import IocManager
from models.base.aps.ApSchedulerJobsTable import ApSchedulerJobsTableBase


class ApSchedulerJobsTable(ApSchedulerJobsTableBase,IocManager.Base):
    # TODO: This feels bad man
    __tablename__ = "ApSchedulerJobsTable"
    __table_args__ = {"schema": "Aps"}

    Id = Column('id', Unicode(191, _warn_on_bytestring=False), primary_key=True)
    NextRunTime = Column('next_run_time', Float(25), index=True)
    JobState = Column('job_state', LargeBinary, nullable=False)