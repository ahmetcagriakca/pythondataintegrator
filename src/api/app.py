

if __name__ == "__main__":
    from pdip.base import Pdi
    from pdip.api.app import FlaskAppWrapper
    from pdi.domain.aps.ApSchedulerSeed import ApSchedulerSeed
    pdi = Pdi(excluded_modules=["alembic", "tests","venv"])
    ApSchedulerSeed().seed()
    pdi.get(FlaskAppWrapper).run()
