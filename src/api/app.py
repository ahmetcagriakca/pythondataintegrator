if __name__ == "__main__":
    from pdip.base import Pdi
    from pdip.api.app import FlaskAppWrapper
    from pdip.data.seed import SeedRunner

    pdi = Pdi(excluded_modules=["alembic", "tests", "venv"])

    pdi.get(SeedRunner).run()
    pdi.get(FlaskAppWrapper).run()
