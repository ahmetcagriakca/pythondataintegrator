if __name__ == "__main__":
    from pdip.base import Pdi
    from pdip.api.app import FlaskAppWrapper

    pdi = Pdi(excluded_modules=["alembic", "tests"])
    pdi.get(FlaskAppWrapper).run()
