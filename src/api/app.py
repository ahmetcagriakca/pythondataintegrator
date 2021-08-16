



def start():
    from IocManager import IocManager

    from infrastructure.api.FlaskAppWrapper import FlaskAppWrapper

    IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
    IocManager.initialize()
    IocManager.run()


if __name__ == "__main__":
    start()
